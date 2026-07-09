import smtplib
import logging
from email.message import EmailMessage
from sqlalchemy.orm import Session
from typing import Optional
from urllib.parse import urlparse
from email.utils import make_msgid
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

# Cairo SVG is optional - if not available, logo embedding will be skipped
try:
    from cairosvg import svg2png
    HAS_CAIRO = True
except (ImportError, OSError):
    HAS_CAIRO = False
    svg2png = None

from app.models.app_setting import AppSetting

SETTINGS_EMAIL_KEY = "email_settings"
logger = logging.getLogger(__name__)


def _get_email_settings(db: Session) -> Optional[dict]:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_EMAIL_KEY).first()
    return row.value if row and isinstance(row.value, dict) else None


def _get_logo_data(db: Session):
    data = _get_email_settings(db) or {}
    brand_logo_url = data.get("brand_logo_url")
    brand_name = data.get("from_name") or "Sicilius"

    logo_bytes = None
    logo_subtype = "png"
    if HAS_CAIRO:
        try:
            inline_svg = (
                "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' width='112' height='112' "
                "fill='none' stroke='#0ea5e9' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>"
                "<path d='M15.6 12.8c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2c-1.2-1.2-2-2.8-2-4.6s.8-3.4 2-4.6c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2'></path>"
                "<path d='M8.4 11.2c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2c1.2 1.2 2 2.8 2 4.6s-.8 3.4-2 4.6c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2'></path>"
                "</svg>"
            )
            logo_bytes = svg2png(bytestring=inline_svg.encode('utf-8'))
            logo_subtype = "png"
        except Exception as e:
            logger.warning(f"SVG to PNG conversion failed: {e}")
            logo_bytes = None
            
    if logo_bytes is None:
        try:
            if not brand_logo_url:
                raise RuntimeError("brand_logo_url not configured")
            with urlopen(brand_logo_url, timeout=5) as resp:
                content_type = (resp.headers.get("Content-Type") or "image/png").lower()
                if "jpeg" in content_type or "jpg" in content_type:
                    logo_subtype = "jpeg"
                elif "png" in content_type:
                    logo_subtype = "png"
                elif "gif" in content_type:
                    logo_subtype = "gif"
                else:
                    logo_subtype = "png"
                logo_bytes = resp.read()
        except (HTTPError, URLError, TimeoutError, Exception):
            logo_bytes = None

    logo_cid = make_msgid(domain="sicilius") if logo_bytes else None
    return logo_bytes, logo_subtype, logo_cid, brand_logo_url, brand_name


def wrap_email_html(db: Session, subject: str, content_html: str, img_src: Optional[str] = None, brand_name: str = "Sicilius", preheader: str = "") -> str:
    logo_part = f'<img src="{img_src}" alt="{brand_name}" width="32" height="32" style="display:block; margin:0;" />' if img_src else f'<div class="brand">{brand_name}</div>'
    
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{subject}</title>
  <style>
    body,table,td,a {{ -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }}
    table,td {{ mso-table-lspace:0pt; mso-table-rspace:0pt; }}
    img {{ -ms-interpolation-mode:bicubic; border:0; height:auto; line-height:100%; outline:none; text-decoration:none; }}
    table {{ border-collapse:collapse !important; }}
    body {{ margin:0 !important; padding:0 !important; background-color:#f5f7fb; }}
    .container {{ max-width: 600px; margin: 0 auto; padding: 24px 12px; }}
    .card {{ background:#ffffff; border-radius:12px; box-shadow:0 1px 3px rgba(16,24,40,.06),0 1px 2px rgba(16,24,40,.10); border: 1px solid #eef2f7; }}
    .header {{ padding: 32px 32px 0px 32px; text-align:left; }}
    .brand {{ font-size: 20px; color:#0f172a; font-weight:700; margin-top:4px; font-family: system-ui, -apple-system, sans-serif; }}
    .content {{ padding: 32px; color:#334155; line-height:1.6; font-size: 15px; font-family: system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }}
    .btn {{ display:inline-block; background:#0ea5e9; color:#ffffff !important; text-decoration:none; padding:12px 24px; border-radius:8px; font-weight:600; font-size: 15px; }}
    .muted {{ color:#64748b; font-size:13px; }}
    .footer {{ padding: 16px 32px 32px; color:#64748b; font-size:12px; text-align:center; }}
    .spacer {{ height: 16px; line-height:16px; font-size:16px; }}
    .preheader {{ display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0; overflow:hidden; mso-hide:all; }}
    .highlight {{ font-weight: 600; background-color: #fef08a; padding: 2px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  {f'<div class="preheader">{preheader}</div>' if preheader else ''}
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" bgcolor="#f5f7fb">
    <tr>
      <td>
        <div class="container">
          <table role="presentation" width="100%" class="card" cellspacing="0" cellpadding="0">
            <tr>
              <td class="header">
                {logo_part}
              </td>
            </tr>
            <tr>
              <td class="content">
                {content_html}
              </td>
            </tr>
            <tr>
              <td class="footer">
                Bu e-posta yanıtlanamaz (no-reply). Yardım için lütfen sistem yöneticinizle iletişime geçin.
              </td>
            </tr>
          </table>
        </div>
      </td>
    </tr>
  </table>
</body>
</html>"""
    return html


def send_email(
    db: Session,
    to: str,
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    reply_to: Optional[str] = None,
    from_email: Optional[str] = None,
    from_name: Optional[str] = None
) -> None:
    data = _get_email_settings(db)
    if not data:
        raise RuntimeError("Email settings not configured")

    host = data.get("host")
    port = int(data.get("port") or 0)
    secure = (data.get("secure") or "starttls").lower()
    user = data.get("username")
    password = data.get("password")
    
    actual_from_name = from_name or data.get("from_name") or "Sicilius"
    actual_from_email = from_email or data.get("from_email")

    if not all([host, port, user, actual_from_email]):
        raise RuntimeError("Incomplete SMTP settings (host/port/username/from_email required)")
    if not password:
        raise RuntimeError("SMTP password missing")

    # Get logo data
    logo_bytes, logo_subtype, logo_cid, brand_logo_url, brand_name = _get_logo_data(db)
    img_src = f"cid:{logo_cid[1:-1]}" if logo_cid else brand_logo_url

    # Automatically wrap body content into the professional template if not already fully formatted
    if not body_html or not (body_html.strip().startswith("<!DOCTYPE") or body_html.strip().startswith("<html")):
        if body_html:
            content_html = body_html
        else:
            wrapped_text = (body_text or "").replace("\n", "<br>")
            wrapped_text = wrapped_text.replace("Sicilius", '<span class="highlight">Sicilius</span>')
            content_html = f"<p>{wrapped_text}</p>"
        body_html = wrap_email_html(db, subject, content_html, img_src=img_src, brand_name=brand_name)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{actual_from_name} <{actual_from_email}>"
    msg["To"] = to
    
    # Configure reply headers (no-reply for invites, reply-to for other custom addresses)
    if reply_to:
        msg["Reply-To"] = reply_to
    elif actual_from_email == "davet@sicilius.com.tr":
        msg["Reply-To"] = "no-reply@sicilius.com.tr"
    else:
        msg["Reply-To"] = actual_from_email
        
    # Plain-text part
    msg.set_content(body_text or "")
    # HTML alternative
    msg.add_alternative(body_html, subtype="html")

    if logo_bytes and logo_cid:
        # attach inline under the HTML alternative part
        html_part = None
        for p in msg.iter_parts():
            if p.get_content_type() == "text/html":
                html_part = p
                break
        target = html_part if html_part else msg
        target.add_related(logo_bytes, maintype="image", subtype=logo_subtype, cid=logo_cid)

    try:
        if secure == "ssl":
            logger.info(f"Connecting to SMTP (SSL): {host}:{port} as {user}")
            with smtplib.SMTP_SSL(host, port, timeout=30) as server:
                server.set_debuglevel(1)  # Enable SMTP debug output
                logger.info("SMTP SSL connected, attempting login...")
                server.login(user, password)
                logger.info("SMTP login successful, sending message...")
                server.send_message(msg)
                logger.info("Email sent successfully via SSL")
        else:
            logger.info(f"Connecting to SMTP (STARTTLS): {host}:{port} as {user}")
            with smtplib.SMTP(host, port, timeout=30) as server:
                server.set_debuglevel(1)  # Enable SMTP debug output
                logger.info("SMTP connected, sending EHLO...")
                server.ehlo()
                logger.info("Starting TLS...")
                server.starttls()
                server.ehlo()  # EHLO again after STARTTLS
                logger.info("STARTTLS enabled, attempting login...")
                server.login(user, password)
                logger.info("SMTP login successful, sending message...")
                server.send_message(msg)
                logger.info("Email sent successfully via STARTTLS")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {e}")
        raise RuntimeError(f"Email authentication failed: {e}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        raise RuntimeError(f"Email sending failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected email error: {e}", exc_info=True)
        raise RuntimeError(f"Email error: {e}")


def send_invite_email(db: Session, to: str, token: str) -> None:
    data = _get_email_settings(db)
    if not data:
        raise RuntimeError("Email settings not configured")

    invite_base = data.get("invite_url_base")
    if not invite_base:
        logger.error("invite_url_base is not configured. Update Email Settings to include invite_url_base.")
        raise RuntimeError("Invite URL base is not configured")

    invite_link = f"{invite_base}?token={token}"
    subject = "Sicilius Davetiyesi"
    
    # Plain text version
    body_text = (
        "Merhaba,\n\n"
        "Sicilius'a katılmanız için bir invite aldınız.\n"
        f"Davetinizi tamamlamak için aşağıdaki bağlantıya tıklayın:\n{invite_link}\n\n"
        "Bu e-posta yanıtlanamaz (no-reply).\n"
    )

    # HTML content fragment to be wrapped by wrap_email_html
    content_html = f"""<p>Merhaba,</p>
<p><span class="highlight">Sicilius</span>'a katılmanız için bir davet aldınız. Hesabınızı oluşturmak ve daveti tamamlamak için aşağıdaki butona tıklayın.</p>
<div class="spacer"></div>
<p style="text-align:center;">
  <a class="btn" href="{invite_link}" target="_blank" rel="noopener noreferrer">Davetiyeyi Tamamla</a>
</p>
<div class="spacer"></div>
<p class="muted">Buton çalışmazsa aşağıdaki bağlantıyı tarayıcınıza yapıştırın:</p>
<p style="word-break:break-all; font-size:13px;"><a href="{invite_link}" target="_blank" style="color:#0ea5e9;">{invite_link}</a></p>"""

    # Explicitly specify from_email and from_name
    send_email(
        db=db,
        to=to,
        subject=subject,
        body_text=body_text,
        body_html=content_html,
        from_email="davet@sicilius.com.tr",
        from_name="Sicilius (no-reply)"
    )


def send_contact_notification(
    db: Session,
    to_email: str,
    first_name: str,
    last_name: str,
    email: str,
    subject: str,
    message: str,
) -> None:
    """
    Send notification email for contact form submissions.
    Uses email settings from database (app_settings table).
    """
    # Plain text content
    body_text = f"""
Yeni İletişim Formu Mesajı

Ad Soyad: {first_name} {last_name}
E-posta: {email}
Konu: {subject}

Mesaj:
{message}

---
Bu mesaj Sicilius iletişim formundan gönderilmiştir.
"""
    
    # HTML content fragment
    content_html = f"""<h2 style="color: #0ea5e9; margin-top:0;">Yeni İletişim Formu Mesajı</h2>
<table style="border-collapse: collapse; margin: 20px 0; width: 100%;">
    <tr>
        <td style="padding: 8px 0; font-weight: bold; width: 100px;">Ad Soyad:</td>
        <td style="padding: 8px 0;">{first_name} {last_name}</td>
    </tr>
    <tr>
        <td style="padding: 8px 0; font-weight: bold;">E-posta:</td>
        <td style="padding: 8px 0;"><a href="mailto:{email}" style="color:#0ea5e9;">{email}</a></td>
    </tr>
    <tr>
        <td style="padding: 8px 0; font-weight: bold;">Konu:</td>
        <td style="padding: 8px 0;">{subject}</td>
    </tr>
</table>
<div style="background: #f9fafb; padding: 16px; border-left: 4px solid #0ea5e9; border-radius: 4px; margin: 20px 0;">
    <h3 style="margin-top: 0; margin-bottom: 8px; font-size: 15px;">Mesaj:</h3>
    <p style="white-space: pre-wrap; margin:0;">{message}</p>
</div>"""
    
    try:
        send_email(
            db=db,
            to=to_email,
            subject=f"İletişim Formu: {subject}",
            body_text=body_text,
            body_html=content_html,
            reply_to=email
        )
        logger.info(f"Contact notification sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send contact notification: {e}")
        # Don't raise - contact form should still work even if email fails
