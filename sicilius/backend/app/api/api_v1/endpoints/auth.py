"""
Authentication endpoints
"""
from datetime import timedelta
import logging
from typing import Any
from datetime import datetime
import secrets

from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.schemas import user as user_schema, token as token_schema, msg as msg_schema
from pydantic import BaseModel, EmailStr, Field
from supabase import create_client
import httpx
import re
from app.models.app_setting import AppSetting
from app.services import email_service

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

def _validate_password_policy(new_password: str, policy: dict | None) -> None:
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
    """
    Issue an access token for future requests.
    - local mode: legacy DB user auth
    - supabase mode: proxy to Supabase Auth and return Supabase access_token
    """
    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        user = crud.user.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
        elif not crud.user.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        # Ban enforcement
        if getattr(user, "is_banned", False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is banned")
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    # Supabase Auth mode
    try:
        client = create_client(settings.supabase_url, settings.supabase_key)
        res = client.auth.sign_in_with_password({
            "email": form_data.username,
            "password": form_data.password,
        })
        if not res or not getattr(res, "session", None) or not res.session:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        access_token = getattr(res.session, "access_token", None)
        if not access_token:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        # Ban enforcement against local user record (if exists)
        try:
            db_user = crud.user.get_by_email(db, email=form_data.username)
            if db_user and getattr(db_user, "is_banned", False):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is banned")
        except HTTPException:
            raise
        except Exception:
            # If lookup fails, do not leak internal errors; allow sign-in to continue
            pass
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

@router.post("/login")
def login(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Get access token and set it in an HTTPOnly cookie.
    - local mode: issue our own JWT
    - supabase mode: sign in via Supabase and set its access_token
    """
    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        user = crud.user.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif not crud.user.is_active(user):
            raise HTTPException(status_code=400, detail="Inactive user")
        # Ban enforcement
        if getattr(user, "is_banned", False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is banned")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    else:
        try:
            client = create_client(settings.supabase_url, settings.supabase_key)
            res = client.auth.sign_in_with_password({
                "email": form_data.username,
                "password": form_data.password,
            })
            if not res or not getattr(res, "session", None) or not res.session:
                raise HTTPException(status_code=401, detail="Incorrect email or password")
            access_token = getattr(res.session, "access_token", None)
            if not access_token:
                raise HTTPException(status_code=401, detail="Incorrect email or password")
            # Ban enforcement against local user record (if exists)
            try:
                db_user = crud.user.get_by_email(db, email=form_data.username)
                if db_user and getattr(db_user, "is_banned", False):
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is banned")
            except HTTPException:
                raise
            except Exception:
                pass
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(status_code=401, detail="Incorrect email or password")

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

    return {"msg": "Login successful"}


@router.post("/logout")
def logout(response: Response):
    """
    Logout user by deleting the auth cookie.
    """
    response.delete_cookie(
        "auth_token",
        path="/",
        samesite="lax",
        secure=settings.SECURE_COOKIE,
        domain=getattr(settings, "COOKIE_DOMAIN", None),
        httponly=True,
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
        role = getattr(current_user.role, "value", str(current_user.role))
    except Exception:
        role = str(getattr(current_user, "role", None))
    is_admin = bool(crud.user.is_superuser(current_user))
    logger.warning(
        "[require-admin] user=%s role=%s is_admin=%s",
        (current_user.email or "").lower(),
        role,
        is_admin,
    )
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not admin")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
    """
    Create new user.
    - local mode: create row in our DB
    - supabase mode: sign up via Supabase, then return a projection compatible with User schema
    """
    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        user = crud.user.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
        user = crud.user.create(db, obj_in=user_in)
        return user

    # Supabase mode
    client = create_client(settings.supabase_url, settings.supabase_key)
    try:
        res = client.auth.sign_up({
            "email": str(user_in.email),
            "password": user_in.password,
        })
        if not res or not getattr(res, "user", None):
            raise HTTPException(status_code=400, detail="Could not sign up user")
        # Build a lightweight response matching User schema
        supa_user = res.user
        from uuid import UUID
        return user_schema.User(
            id=UUID(str(supa_user.id)),
            email=str(user_in.email),
            full_name=user_in.full_name,
            is_active=True,
            role="user",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Could not sign up user")

@router.post("/change-password", response_model=msg_schema.Msg)
def change_password(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
    body: user_schema.PasswordChange,
) -> Any:
    """
    Change current user's password.
    - local mode: verify current password against local DB, then update hash
    - supabase mode: verify by sign_in_with_password, then update via Admin API (service role)
    """
    # Basic policy: disallow same password
    if body.current_password == body.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from current password")
    # Enforce security settings policy (length/complexity)
    sec = _get_security_settings(db)
    _validate_password_policy(body.new_password, sec)

    if getattr(settings, "auth_mode", "local").lower() != "supabase":
        # Local mode: verify and update
        if not crud.user.authenticate(db, email=current_user.email, password=body.current_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        crud.user.update(db, db_obj=current_user, obj_in={"password": body.new_password})
        return {"msg": "Password changed successfully"}

    # Supabase mode
    client = create_client(settings.supabase_url, settings.supabase_key)
    # 1) Verify current password at Supabase
    try:
        res = client.auth.sign_in_with_password({
            "email": current_user.email,
            "password": body.current_password,
        })
        if not res or not getattr(res, "session", None):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
    except HTTPException:
        raise
    except Exception:
        # Hide internals
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # 2) Update password via Admin API (service role)
    admin_key = settings.supabase_service_role_key
    if not admin_key:
        raise HTTPException(status_code=500, detail="Supabase service role key is not configured")

    url = f"{settings.supabase_url}/auth/v1/admin/users/{current_user.id}"
    headers = {
        "apikey": admin_key,
        "Authorization": f"Bearer {admin_key}",
        "Content-Type": "application/json",
    }
    payload = {"password": body.new_password}
    try:
        with httpx.Client(timeout=15.0) as http:
            resp = http.put(url, headers=headers, json=payload)
            if resp.status_code // 100 != 2:
                raise HTTPException(status_code=400, detail="Could not change password")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Could not change password")

    return {"msg": "Password changed successfully"}

@router.post("/password-recovery/{email}", response_model=msg_schema.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
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
def invite_user(
    req: InviteRequest,
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

    # Monthly invite limit per user (admins are exempt)
    month_key = datetime.utcnow().strftime("%Y-%m")
    # Admin muafiyeti enum tabanlı kontrol ile sağlanır
    if not crud.user.is_superuser(current_user):
        used_count = (
            db.query(models.UserInvite)
            .filter(
                models.UserInvite.inviter_user_id == current_user.id,
                models.UserInvite.invited_month_key == month_key,
            )
            .count()
        )
        monthly_limit = int(us.get("monthly_invite_limit_per_admin", 1) or 1)
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

    # Davetiye e-postasını gönder (no-reply). Hata halinde daveti geri al.
    try:
        email_service.send_invite_email(db, to=str(req.email), token=token)
    except Exception as e:
        try:
            db.delete(invite)
            db.commit()
        except Exception:
            db.rollback()
        raise HTTPException(status_code=400, detail=f"Davet e-postası gönderilemedi: {e}")

    # Frontend'in davet linki oluşturabilmesi için token'ı da döndür.
    return {"token": token, "msg": "Davet oluşturuldu ve e-posta gönderildi"}


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



