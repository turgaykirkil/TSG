"""
Authentication endpoints
"""
from datetime import timedelta
import logging
from typing import Any, Optional
from datetime import datetime
import secrets

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.schemas import user as user_schema, token as token_schema, msg as msg_schema
from pydantic import BaseModel, EmailStr, Field
import re
import hashlib
import httpx
from app.models.app_setting import AppSetting
from app.services import email_service
from app.core.rate_limit import limiter

logger = logging.getLogger(__name__)

router = APIRouter()

# --- Helpers to read app settings stored in app_settings ---
def _get_app_settings(db: Session, key: str) -> dict:
    row = db.query(AppSetting).filter(AppSetting.key == key).first()
    return row.value if row and isinstance(row.value, dict) else {}

def _get_user_settings(db: Session) -> dict:
    return _get_app_settings(db, "user_settings")

def _get_security_settings(db: Session) -> dict:
    return _get_app_settings(db, "security_settings")

def _validate_password_policy(new_password: str, policy: Optional[dict]) -> None:
    if not policy:
        return
    # Minimum length
    min_len = int(policy.get("password_min_length", 8) or 8)
    if len(new_password) < min_len:
        raise HTTPException(status_code=400, detail=f"Password must be at least {min_len} characters")
    # Character class requirements
    if policy.get("password_require_upper", True) and not re.search(r"[A-Z]", new_password):
        raise HTTPException(status_code=400, detail="Password must include an uppercase letter")
    if policy.get("password_require_number", True) and not re.search(r"[0-9]", new_password):
        raise HTTPException(status_code=400, detail="Password must include a number")
    if policy.get("password_require_symbol", True) and not re.search(r"[^A-Za-z0-9]", new_password):
        raise HTTPException(status_code=400, detail="Password must include a symbol")

@router.post("/login/access-token", response_model=token_schema.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Yerel kullanıcı doğrulaması yaparak erişim token'ı üretir."""
    logger.info("[login/access-token] email=%s", form_data.username)
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        logger.warning("[login/access-token] user_not_found_or_bad_password email=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    if not crud.user.is_active(user):
        logger.warning("[login/access-token] inactive_user email=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    if getattr(user, "is_banned", False):
        logger.warning("[login/access-token] banned_user email=%s", form_data.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is banned")

    # Role-based token expiry: Admin 24h, normal user 10min
    is_admin = crud.user.is_superuser(user)
    token_minutes = settings.ADMIN_TOKEN_EXPIRE_MINUTES if is_admin else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=token_minutes)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    logger.info("[login/access-token] success email=%s", form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
@limiter.limit("10/minute")  # Max 10 login attempts per minute per IP
async def login(
    response: Response,
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """Yerel kullanıcı girişini yapar ve HTTPOnly cookie içinde JWT döner."""
    logger.info("[login] email=%s", form_data.username)
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        logger.warning("[login] user_not_found_or_bad_password email=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not crud.user.is_active(user):
        logger.warning("[login] inactive_user email=%s", form_data.username)
        raise HTTPException(status_code=400, detail="Inactive user")
    if getattr(user, "is_banned", False):
        logger.warning("[login] banned_user email=%s", form_data.username)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is banned")

    # Role-based token expiry: Admin 24h, normal user 10min
    is_admin = crud.user.is_superuser(user)
    token_minutes = settings.ADMIN_TOKEN_EXPIRE_MINUTES if is_admin else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=token_minutes)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    _origin = request.headers.get("origin") or ""
    try:
        from urllib.parse import urlparse

        host = urlparse(_origin).hostname or ""
    except Exception:
        host = ""
    if host.endswith("sicilius.com.tr") or host in {"localhost", "127.0.0.1"}:
        _samesite = "lax"
    else:
        _samesite = "none"
    logger.info("[login] origin=%s samesite=%s cookie_domain=%s secure=%s", _origin, _samesite, getattr(settings, "COOKIE_DOMAIN", None), settings.SECURE_COOKIE)
    if _samesite == "none":
        # Use CHIPS-style cookie for third-party context (localhost dev)
        max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        parts = [
            f"auth_token={access_token}",
            "Path=/",
            f"Max-Age={max_age}",
            "HttpOnly",
            "SameSite=None",
        ]
        if settings.SECURE_COOKIE:
            parts.append("Secure")
            parts.append("Partitioned")
        domain = getattr(settings, "COOKIE_DOMAIN", None)
        if domain:
            parts.append(f"Domain={domain}")
        response.headers.append("Set-Cookie", "; ".join(parts))
        logger.info("[login] set-cookie header appended secure=%s", settings.SECURE_COOKIE)
    else:
        response.set_cookie(
            "auth_token",
            value=access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
            samesite=_samesite,
            secure=settings.SECURE_COOKIE,
            domain=getattr(settings, "COOKIE_DOMAIN", None),
        )
        logger.info("[login] set-cookie via response.set_cookie samesite=%s", _samesite)

    return {"msg": "Login successful"}


@router.post("/logout")
def logout(response: Response):
    """
    Logout user by deleting the auth cookie.
    """
    # Delete standard cookie
    response.delete_cookie(
        "auth_token",
        path="/",
        samesite="lax",
        secure=settings.SECURE_COOKIE,
        domain=getattr(settings, "COOKIE_DOMAIN", None),
        httponly=True,
    )
    # Also delete possible Partitioned variant
    domain_attr = f"; Domain={getattr(settings, 'COOKIE_DOMAIN', '')}" if getattr(settings, "COOKIE_DOMAIN", None) else ""
    response.headers.append(
        "Set-Cookie",
        f"auth_token=deleted; Path=/; Max-Age=0; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; Secure; SameSite=None; Partitioned" + domain_attr,
    )
    return {"msg": "Successfully logged out"}


# --- Admin-only guard endpoint ---
@router.get("/require-admin", status_code=status.HTTP_204_NO_CONTENT)
def require_admin(
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Backend-enforced admin check. Returns 204 if the current user is an admin (superuser).
    Logs the user's email and role in all cases for debugging.
    """
    try:
        import sys
        print(f"DEBUG: require-admin entered for {current_user.email}", file=sys.stderr)
        try:
            role = getattr(current_user.role, "value", str(current_user.role))
        except Exception:
            role = str(getattr(current_user, "role", None))
        
        is_admin = bool(crud.user.is_superuser(current_user))
        print(f"DEBUG: require-admin check: is_admin={is_admin}", file=sys.stderr)
        
        logger.warning(
            "[require-admin] user=%s role=%s is_admin=%s",
            (current_user.email or "").lower(),
            role,
            is_admin,
        )
        if not is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not admin")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        import sys
        print(f"CRITICAL ERROR in require-admin: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"Internal Server Error in require-admin: {e}")


@router.post("/login/test-token", response_model=user_schema.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/register", response_model=user_schema.User)
def register_user(
    *, 
    db: Session = Depends(deps.get_db), 
    user_in: user_schema.UserCreate
) -> Any:
    """Yeni kullanıcıyı yerel veritabanında oluşturur."""
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/change-password", response_model=msg_schema.Msg)
def change_password(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    body: user_schema.PasswordChange,
) -> Any:
    """Kullanıcının mevcut parolasını doğrulayıp yenisiyle günceller."""
    # Basic policy: disallow same password
    if body.current_password == body.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    # Enforce security settings policy (length/complexity)
    sec = _get_security_settings(db)
    _validate_password_policy(body.new_password, sec)

    if not crud.user.authenticate(db, email=current_user.email, password=body.current_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    crud.user.update(db, db_obj=current_user, obj_in={"password": body.new_password})
    return {"msg": "Password changed successfully"}

@router.post("/password-recovery/{email}", response_model=msg_schema.Msg)
@limiter.limit("5/hour")  # Max 5 password recovery attempts per hour per IP
async def recover_password(email: str, db: Session = Depends(deps.get_db),request: Request = None) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    
    password_reset_token = security.generate_password_reset_token(email=email)
    # TODO: Send email with password reset token
    
    return {"msg": "Password recovery email sent"}

@router.post("/reset-password/", response_model=msg_schema.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = security.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    
    return {"msg": "Password updated successfully"}


# --- Invite-based onboarding ---

class InviteRequest(BaseModel):
    email: EmailStr

class InviteToken(BaseModel):
    token: str

class InviteComplete(BaseModel):
    token: str
    password: str = Field(..., min_length=8, max_length=40)


@router.post("/invite", summary="Create a monthly invitation for a new user")
@limiter.limit("5/hour")  # Max 5 invites per hour per IP
async def invite_user(
    req: InviteRequest,
    request: Request,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    # Enforce settings
    us = _get_user_settings(db)
    if not us.get("invite_enabled", True):
        raise HTTPException(status_code=403, detail="Davet oluşturma şu an kapalı")

    # Domain allow/deny
    email_domain = str(req.email).split("@")[-1].lower().strip()
    allow = [d.lower().strip() for d in (us.get("allowed_email_domains") or []) if d]
    block = [d.lower().strip() for d in (us.get("blocked_email_domains") or []) if d]
    if allow and email_domain not in allow:
        raise HTTPException(status_code=400, detail="Bu e-posta alan adı davete uygun değil")
    if block and email_domain in block:
        raise HTTPException(status_code=400, detail="Bu e-posta alan adı engellenmiş")

    # Existing user check: do not allow invites to already-registered emails
    # 1) Bekleyen davet kontrolü (aynı e-posta için henüz kabul edilmemiş bir davet varsa engelle)
    pending = (
        db.query(models.UserInvite)
        .filter(
            models.UserInvite.invited_email == str(req.email).lower(),
            models.UserInvite.accepted_at.is_(None),
        )
        .first()
    )
    if pending:
        raise HTTPException(status_code=409, detail="Bu e-posta için bekleyen bir davet zaten var")

    # 2) Var olan kullanıcı kontrolü (banlı kullanıcıya davet de engellenir)
    existing_user = crud.user.get_by_email(db, email=str(req.email).lower())
    if existing_user:
        if getattr(existing_user, "is_banned", False):
            raise HTTPException(status_code=403, detail="Banlanmış kullanıcıya davet gönderilemez")
        raise HTTPException(status_code=409, detail="Bu e-posta ile zaten bir hesap mevcut")

    # Monthly invite limit per user (admins have higher/unlimited limit)
    month_key = datetime.utcnow().strftime("%Y-%m")
    
    used_count = (
        db.query(models.UserInvite)
        .filter(
            models.UserInvite.inviter_user_id == current_user.id,
            models.UserInvite.invited_month_key == month_key,
        )
        .count()
    )
    
    if crud.user.is_superuser(current_user):
        # Admin user - effectively unlimited
        monthly_limit = int(us.get("monthly_invite_limit_per_admin", 999999) or 999999)
    else:
        # Regular user - limited to 1 per month by default
        monthly_limit = int(us.get("monthly_invite_limit_per_user", 1) or 1)
    
    if used_count >= monthly_limit:
        raise HTTPException(status_code=400, detail=f"Aylık davet limitine ulaşıldı ({monthly_limit}).")

    token = secrets.token_urlsafe(32)
    invite = models.UserInvite(
        inviter_user_id=current_user.id,
        invited_email=str(req.email).lower(),
        invited_month_key=month_key,
        token=token,
    )
    db.add(invite)
    db.commit()
    db.refresh(invite)

    # Davetiye e-postasını gönder (no-reply). Hata halinde logla ve uyarı mesajı dön.
    email_sent = True
    email_error = None
    try:
        email_service.send_invite_email(db, to=str(req.email), token=token)
    except Exception as e:
        email_sent = False
        email_error = str(e)
        logger.warning(f"Failed to send invite email to {req.email}: {e}")

    # Frontend'in davet linki oluşturabilmesi için token'ı da döndür.
    return {
        "token": token,
        "email_sent": email_sent,
        "email_error": email_error,
        "msg": "Davet oluşturuldu ve e-posta gönderildi" if email_sent else f"Davet oluşturuldu fakat e-posta gönderilemedi: {email_error}"
    }


@router.post("/invite/accept", summary="Validate invite token and return invited email")
def invite_accept(body: InviteToken, db: Session = Depends(deps.get_db)):
    invite = (
        db.query(models.UserInvite)
        .filter(models.UserInvite.token == body.token)
        .first()
    )
    if not invite:
        raise HTTPException(status_code=404, detail="Geçersiz davet bağlantısı")
    if invite.accepted_at is not None:
        raise HTTPException(status_code=400, detail="Davet zaten kullanılmış")
    return {"email": invite.invited_email}


@router.post("/invite/complete", summary="Complete invite by setting password and creating account")
def invite_complete(
    response: Response,
    body: InviteComplete,
    request: Request,
    db: Session = Depends(deps.get_db),
):
    invite = (
        db.query(models.UserInvite)
        .filter(models.UserInvite.token == body.token)
        .first()
    )
    if not invite:
        raise HTTPException(status_code=404, detail="Geçersiz davet bağlantısı")
    if invite.accepted_at is not None:
        raise HTTPException(status_code=400, detail="Davet zaten kullanılmış")
    # auth_mode'a göre kullanıcı oluşturma ve oturum açma
    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        # Local mod: kullanıcıyı yerel DB'de oluştur
        existing_user = crud.user.get_by_email(db, email=invite.invited_email)
        if existing_user:
            raise HTTPException(status_code=409, detail="Bu e-posta ile zaten bir hesap mevcut")

        user_in = user_schema.UserCreate(
            email=invite.invited_email,
            password=body.password,
            full_name=invite.invited_email,
        )
        user = crud.user.create(db, obj_in=user_in)

        # Daveti kabul edildi olarak işaretle
        invite.accepted_at = datetime.utcnow()
        db.add(invite)
        db.commit()

        # Auto-login: yerel JWT ile cookie ayarla
        access_token = security.create_access_token(
            user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        _origin = request.headers.get("origin") or ""
        _samesite = "lax" if _origin.endswith("sicilius.com.tr") else "none"
        response.set_cookie(
            "auth_token",
            value=access_token,
            httponly=True,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/",
            samesite=_samesite,
            secure=settings.SECURE_COOKIE,
            domain=getattr(settings, "COOKIE_DOMAIN", None),
        )

        return {"msg": "Davet tamamlandı ve giriş yapıldı"}

    # Supabase mod: Admin API ile kullanıcıyı oluştur ve Supabase token'ı ile giriş yap
    admin_key = settings.supabase_service_role_key
    if not admin_key:
        raise HTTPException(status_code=500, detail="Supabase service role key is not configured")

    # Şifre politikası (security_settings) uygula
    try:
        sec = _get_security_settings(db)
        _validate_password_policy(body.password, sec)
    except HTTPException:
        raise
    except Exception:
        # Beklenmeyen durumda politikayı atlama
        pass

    # 1) Supabase Admin API ile kullanıcı oluştur (email doğrulanmış kabul edilsin)
    create_url = f"{settings.supabase_url}/auth/v1/admin/users"
    headers = {
        "apikey": admin_key,
        "Authorization": f"Bearer {admin_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": invite.invited_email,
        "password": body.password,
        "email_confirm": True,
    }
    try:
        with httpx.Client(timeout=15.0) as http:
            resp = http.post(create_url, headers=headers, json=payload)
            # 409 veya 422 (already registered) durumda devam edip giriş deneyeceğiz
            proceed = resp.status_code in (200, 201, 409)
            detail = resp.text
            try:
                data = resp.json()
                if isinstance(data, dict) and data.get("msg"):
                    detail = data.get("msg")
                elif isinstance(data, dict) and data.get("message"):
                    detail = data.get("message")
            except Exception:
                pass
            if resp.status_code == 422 and isinstance(detail, str) and "already been registered" in detail.lower():
                proceed = True
            if not proceed:
                raise HTTPException(status_code=400, detail=f"Kullanıcı oluşturulamadı (Supabase {resp.status_code}): {detail}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Kullanıcı oluşturulamadı (Supabase): {e}")

    # 2) Supabase ile parola ile giriş yap ve access_token al
    try:
        from supabase import create_client
        client = create_client(settings.supabase_url, settings.supabase_key)
        res = client.auth.sign_in_with_password(
            {
                "email": invite.invited_email,
                "password": body.password,
            }
        )
        if not res or not getattr(res, "session", None) or not res.session:
            raise HTTPException(status_code=400, detail="Giriş yapılamadı (Supabase): session yok")
        access_token = getattr(res.session, "access_token", None)
        if not access_token:
            raise HTTPException(status_code=400, detail="Giriş yapılamadı (Supabase): access_token yok")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Giriş yapılamadı (Supabase): {e}")

    # 3) Daveti kabul edildi olarak işaretle (yerel kayıt)
    invite.accepted_at = datetime.utcnow()
    db.add(invite)
    db.commit()

    # 4) Supabase access_token'ını cookie olarak ayarla
    response.set_cookie(
        "auth_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        samesite="lax",
        secure=settings.SECURE_COOKIE,
        domain=getattr(settings, "COOKIE_DOMAIN", None),
    )

    return {"msg": "Davet tamamlandı ve giriş yapıldı"}


@router.get("/invite/my", summary="List invites created by current user")
def invite_list_my(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    invites = (
        db.query(models.UserInvite)
        .filter(models.UserInvite.inviter_user_id == current_user.id)
        .all()
    )
    return [
        {
            "token": inv.token,
            "invited_email": inv.invited_email,
            "invited_month_key": inv.invited_month_key,
            "accepted_at": inv.accepted_at,
        }
        for inv in invites
    ]


@router.delete("/invite/{token}", summary="Revoke an invite created by current user")
def invite_revoke(
    token: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    inv = (
        db.query(models.UserInvite)
        .filter(models.UserInvite.token == token)
        .first()
    )
    if not inv:
        raise HTTPException(status_code=404, detail="Davet bulunamadı")
    if str(inv.inviter_user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Bu daveti iptal etme yetkiniz yok")
    if inv.accepted_at is not None:
        raise HTTPException(status_code=400, detail="Zaten kabul edilmiş davet iptal edilemez")
    db.delete(inv)
    db.commit()
    return {"msg": "Davet iptal edildi"}




class SignupProxyRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = None
    auto_login: bool = True


@router.post("/signup-proxy")
def signup_proxy(
    response: Response,
    body: SignupProxyRequest,
    request: Request,
    db: Session = Depends(deps.get_db),
):
    sec = _get_security_settings(db)
    _validate_password_policy(body.password, sec)

    try:
        sha1 = hashlib.sha1(body.password.encode("utf-8")).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        with httpx.Client(timeout=10.0) as http:
            r = http.get(url, headers={"Add-Padding": "true"})
            if r.status_code // 100 == 2:
                for line in r.text.splitlines():
                    parts = line.split(":")
                    if len(parts) == 2 and parts[0].strip().upper() == suffix:
                        cnt = int(parts[1].strip() or "0")
                        if cnt > 0:
                            raise HTTPException(status_code=400, detail="Password found in breach database")
    except HTTPException:
        raise
    except Exception:
        pass

    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        user = crud.user.get_by_email(db, email=str(body.email).lower())
        if user:
            raise HTTPException(status_code=409, detail="This email is already registered")
        user_in = user_schema.UserCreate(
            email=str(body.email).lower(),
            password=body.password,
            full_name=body.full_name or str(body.email).lower(),
        )
        user = crud.user.create(db, obj_in=user_in)
        if body.auto_login:
            access_token = security.create_access_token(
                user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            _origin = request.headers.get("origin") or ""
            _samesite = "lax" if _origin.endswith("sicilius.com.tr") else "none"
            if _samesite == "none":
                max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                domain_attr = f"; Domain={getattr(settings, 'COOKIE_DOMAIN', '')}" if getattr(settings, "COOKIE_DOMAIN", None) else ""
                cookie_val = (
                    f"auth_token={access_token}; Path=/; Max-Age={max_age}; HttpOnly; Secure; SameSite=None; Partitioned" + domain_attr
                )
                response.headers.append("Set-Cookie", cookie_val)
            else:
                response.set_cookie(
                    "auth_token",
                    value=access_token,
                    httponly=True,
                    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                    path="/",
                    samesite=_samesite,
                    secure=settings.SECURE_COOKIE,
                    domain=getattr(settings, "COOKIE_DOMAIN", None),
                )
        return {"msg": "User created"}

    admin_key = settings.supabase_service_role_key
    if not admin_key:
        raise HTTPException(status_code=500, detail="Supabase service role key is not configured")

    create_url = f"{settings.supabase_url}/auth/v1/admin/users"
    headers = {
        "apikey": admin_key,
        "Authorization": f"Bearer {admin_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": str(body.email).lower(),
        "password": body.password,
        "email_confirm": True,
    }
    try:
        with httpx.Client(timeout=15.0) as http:
            resp = http.post(create_url, headers=headers, json=payload)
            proceed = resp.status_code in (200, 201, 409)
            if not proceed:
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise HTTPException(status_code=400, detail=f"Could not sign up user: {detail}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not sign up user: {e}")

    if body.auto_login:
        try:
            from supabase import create_client
            client = create_client(settings.supabase_url, settings.supabase_key)
            res = client.auth.sign_in_with_password({
                "email": str(body.email).lower(),
                "password": body.password,
            })
            if not res or not getattr(res, "session", None) or not res.session:
                raise HTTPException(status_code=400, detail="Could not sign in after signup")
            access_token = getattr(res.session, "access_token", None)
            if not access_token:
                raise HTTPException(status_code=400, detail="Could not sign in after signup")
            response.set_cookie(
                "auth_token",
                value=access_token,
                httponly=True,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                path="/",
                samesite="lax",
                secure=settings.SECURE_COOKIE,
                domain=getattr(settings, "COOKIE_DOMAIN", None),
            )
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=400, detail="Could not sign in after signup")

    return {"msg": "User created"}

