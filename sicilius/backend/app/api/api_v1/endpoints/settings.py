from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Any, Optional
import smtplib
from email.message import EmailMessage

from app.api import deps
from app.db.session import SessionLocal
from app.models.app_setting import AppSetting
from app.schemas.settings import EmailSettings, EmailSettingsOut, UserSettings, UserSettingsOut

router = APIRouter()

SETTINGS_EMAIL_KEY = "email_settings"
SETTINGS_USER_KEY = "user_settings"


def _get_email_settings(db: Session) -> Optional[dict]:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_EMAIL_KEY).first()
    return row.value if row else None


def _set_email_settings(db: Session, data: dict) -> None:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_EMAIL_KEY).first()
    if row is None:
        row = AppSetting(key=SETTINGS_EMAIL_KEY, value=data)
        db.add(row)
    else:
        row.value = data
        db.add(row)
    db.commit()


def _get_user_settings(db: Session) -> Optional[dict]:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_USER_KEY).first()
    return row.value if row else None


def _set_user_settings(db: Session, data: dict) -> None:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_USER_KEY).first()
    if row is None:
        row = AppSetting(key=SETTINGS_USER_KEY, value=data)
        db.add(row)
    else:
        row.value = data
        db.add(row)
    db.commit()


@router.get("/email", response_model=EmailSettingsOut)
def get_email_settings(
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_superuser),
) -> Any:
    data = _get_email_settings(db) or {}
    if not data:
        # Return minimal defaults
        return EmailSettingsOut(
            host="",
            port=587,
            secure="starttls",
            username="",
            from_name="Sicilius",
            from_email="no-reply@example.com",
            reset_url_base="http://localhost:3000",
            invite_url_base="http://localhost:3000/davet",
        )
    return EmailSettingsOut(**{k: v for k, v in data.items() if k != "password"})


@router.put("/email", response_model=EmailSettingsOut)
def update_email_settings(
    body: EmailSettings,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_superuser),
) -> Any:
    existing = _get_email_settings(db) or {}
    merged = existing.copy()
    incoming = body.dict(exclude_none=True)
    # If password is empty/None, keep existing
    if not incoming.get("password"):
        incoming.pop("password", None)
    merged.update(incoming)
    _set_email_settings(db, merged)
    return EmailSettingsOut(**{k: v for k, v in merged.items() if k != "password"})


@router.post("/email/test")
def test_email_settings(
    to: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_superuser),
) -> Any:
    data = _get_email_settings(db)
    if not data:
        raise HTTPException(status_code=400, detail="Email settings not configured")

    msg = EmailMessage()
    msg["Subject"] = "Sicilius Test E-postası"
    msg["From"] = f"{data.get('from_name','Sicilius')} <{data['from_email']}>"
    msg["To"] = to
    msg.set_content("Bu bir test iletisidir.")

    host = data["host"]
    port = int(data["port"])
    secure = data.get("secure", "starttls")
    user = data["username"]
    password = data.get("password")
    if not password:
        raise HTTPException(status_code=400, detail="SMTP password is empty; update settings with a password")

    try:
        if secure == "ssl":
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(user, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as server:
                server.ehlo()
                server.starttls()
                server.login(user, password)
                server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SMTP error: {e}")
    return {"msg": "Test email sent"}


@router.get("/user", response_model=UserSettingsOut)
def get_user_settings(
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_superuser),
) -> Any:
    data = _get_user_settings(db) or {}
    if not data:
        return UserSettingsOut()
    return UserSettingsOut(**data)


@router.put("/user", response_model=UserSettingsOut)
def update_user_settings(
    body: UserSettings,
    db: Session = Depends(deps.get_db),
    current_user=Depends(deps.get_current_active_superuser),
) -> Any:
    merged = (_get_user_settings(db) or {})
    merged.update(body.dict())
    _set_user_settings(db, merged)
    return UserSettingsOut(**merged)
