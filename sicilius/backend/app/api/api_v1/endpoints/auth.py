"""
Authentication endpoints
"""
from datetime import timedelta
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

router = APIRouter()

@router.post("/login/access-token", response_model=token_schema.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
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
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/login")
def login(
    response: Response,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    Get the access token for the user and set it in an HTTPOnly cookie.
    """
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

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
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
        httponly=True,
    )
    return {"msg": "Successfully logged out"}


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
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user

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
    month_key = datetime.utcnow().strftime("%Y-%m")
    # Enforce one invite per inviter per month
    existing = (
        db.query(models.UserInvite)
        .filter(
            models.UserInvite.inviter_user_id == current_user.id,
            models.UserInvite.invited_month_key == month_key,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Bu ay için davet hakkınız zaten kullanılmış.")

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

    # TODO: E-posta gönderimi entegre edilecek. Şimdilik token döndürülür.
    return {"msg": "Davet oluşturuldu", "token": token}


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

    # Email zaten varsa yeni hesap oluşturma
    existing_user = crud.user.get_by_email(db, email=invite.invited_email)
    if existing_user:
        raise HTTPException(status_code=409, detail="Bu e-posta ile zaten bir hesap mevcut")

    # Create user with minimal fields
    user_in = user_schema.UserCreate(email=invite.invited_email, password=body.password, full_name=invite.invited_email)
    user = crud.user.create(db, obj_in=user_in)

    # Mark invite as accepted
    invite.accepted_at = datetime.utcnow()
    db.add(invite)
    db.commit()

    # Auto-login: issue cookie
    access_token = security.create_access_token(user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    response.set_cookie(
        "auth_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        samesite="lax",
        secure=settings.SECURE_COOKIE,
    )

    return {"msg": "Davet tamamlandı ve giriş yapıldı"}


@router.post("/change-password", response_model=msg_schema.Msg)
def change_password(
    *, 
    db: Session = Depends(deps.get_db),
    password_data: user_schema.PasswordChange,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Change password for the current user.
    """
    if not crud.user.authenticate(
        db, email=current_user.email, password=password_data.current_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    hashed_password = get_password_hash(password_data.new_password)
    current_user.hashed_password = hashed_password
    db.add(current_user)
    db.commit()
    
    return {"msg": "Password updated successfully"}
