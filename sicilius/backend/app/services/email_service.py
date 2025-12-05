import smtplib
import logging
from email.message import EmailMessage
from sqlalchemy.orm import Session
from typing import Optional
from urllib.parse import urlparse
from email.utils import make_msgid
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from cairosvg import svg2png

from app.models.app_setting import AppSetting

SETTINGS_EMAIL_KEY = "email_settings"
logger = logging.getLogger(__name__)


def _get_email_settings(db: Session) -> Optional[dict]:
    row = db.query(AppSetting).filter(AppSetting.key == SETTINGS_EMAIL_KEY).first()
    return row.value if row and isinstance(row.value, dict) else None


def send_email(db: Session, to: str, subject: str, body_text: str, body_html: Optional[str] = None) -> None:
    data = _get_email_settings(db)
    if not data:
        raise RuntimeError("Email settings not configured")

    host = data.get("host")
    port = int(data.get("port") or 0)
    secure = (data.get("secure") or "starttls").lower()
    user = data.get("username")
    password = data.get("password")
    from_name = data.get("from_name") or "Sicilius"
    from_email = data.get("from_email")

    if not all([host, port, user, from_email]):
        raise RuntimeError("Incomplete SMTP settings (host/port/username/from_email required)")
    if not password:
        raise RuntimeError("SMTP password missing")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to
    # Plain-text part
    msg.set_content(body_text or "")
    # Optional HTML alternative
    if body_html:
        msg.add_alternative(body_html, subtype="html")

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
        # Do not fall back to reset_url_base; force explicit configuration to avoid wrong links
        logger.error("invite_url_base is not configured. Update Email Settings to include invite_url_base.")
        raise RuntimeError("Invite URL base is not configured")

    invite_link = f"{invite_base}?token={token}"

    subject = "Sicilius Davetiyesi"
    # Plain-text fallback
    body_text = (
        "Merhaba,\n\n"
        "Sicilius'a katılmanız için bir davet aldınız.\n"
        f"Davetinizi tamamlamak için aşağıdaki bağlantıya tıklayın:\n{invite_link}\n\n"
        "Bu e-posta yanıtlanamaz (no-reply).\n"
    )

    # Determine origin and optional override URL
    parsed = urlparse(invite_base)
    origin = f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else "https://sicilius.com.tr"
    brand_logo_url = data.get("brand_logo_url")
    brand_name = data.get("from_name") or "Sicilius"

    # Prefer a built-in inline SVG rasterized to PNG (no network dependency)
    logo_bytes: Optional[bytes] = None
    logo_subtype = "png"
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
    except Exception:
        # Fallback: try to fetch explicit override PNG/JPEG if provided
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

    # If we can embed, use CID; otherwise keep external URL
    logo_cid = make_msgid(domain="sicilius") if logo_bytes else None
    img_src = f"cid:{logo_cid[1:-1]}" if logo_cid else brand_logo_url

    # Lightweight, broadly compatible HTML email (tables + inline CSS)
    body_html = f"""
    <!DOCTYPE html>
    <html lang=\"tr\">
    <head>
      <meta charset=\"utf-8\" />
      <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
      <title>{subject}</title>
      <style>
        /* Client-safe resets */
        body,table,td,a {{ -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }}
        table,td {{ mso-table-lspace:0pt; mso-table-rspace:0pt; }}
        img {{ -ms-interpolation-mode:bicubic; }}
        img {{ border:0; height:auto; line-height:100%; outline:none; text-decoration:none; }}
        table {{ border-collapse:collapse !important; }}
        body {{ margin:0 !important; padding:0 !important; background-color:#f5f7fb; }}
        /* Utilities */
        .container {{ max-width: 600px; margin: 0 auto; padding: 24px 12px; }}
        .card {{ background:#ffffff; border-radius:12px; box-shadow:0 1px 3px rgba(16,24,40,.06),0 1px 2px rgba(16,24,40,.10); }}
        .header {{ padding: 24px; text-align:center; border-bottom:1px solid #eef2f7; }}
        .brand {{ font-size: 18px; color:#0f172a; font-weight:700; margin-top:12px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji', sans-serif; }}
        .content {{ padding: 24px; color:#334155; line-height:1.6; font-size: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif; }}
        .btn {{ display:inline-block; background:#0ea5e9; color:#ffffff !important; text-decoration:none; padding:12px 20px; border-radius:8px; font-weight:600; }}
        .muted {{ color:#64748b; font-size:13px; }}
        .footer {{ padding: 16px 24px 24px; color:#64748b; font-size:12px; text-align:center; }}
        .spacer {{ height: 16px; line-height:16px; font-size:16px; }}
        .preheader {{ display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0; overflow:hidden; mso-hide:all; }}
      </style>
    </head>
    <body>
      <div class=\"preheader\">Sicilius davetiyeniz hazır. Hesabınızı oluşturmak için bağlantıya tıklayın.</div>
      <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" bgcolor=\"#f5f7fb\">
        <tr>
          <td>
            <div class=\"container\">
              <table role=\"presentation\" width=\"100%\" class=\"card\" cellspacing=\"0\" cellpadding=\"0\">
                <tr>
                  <td class=\"header\">
                    <img src=\"{img_src}\" alt=\"{brand_name}\" width=\"24\" height=\"24\" style=\"border-radius:12px; background:#f8fafc; display:block;\" />
                  </td>
                </tr>
                <tr>
                  <td class=\"content\">
                    <p>Merhaba,</p>
                    <p>Sicilius'a katılmanız için bir davet aldınız. Hesabınızı oluşturmak ve daveti tamamlamak için aşağıdaki butona tıklayın.</p>
                    <div class=\"spacer\"></div>
                    <p style=\"text-align:center;\">
                      <a class=\"btn\" href=\"{invite_link}\" target=\"_blank\" rel=\"noopener noreferrer\">Davetiyeyi Tamamla</a>
                    </p>
                    <div class=\"spacer\"></div>
                    <p class=\"muted\">Buton çalışmazsa aşağıdaki bağlantıyı tarayıcınıza yapıştırın:</p>
                    <p style=\"word-break:break-all; font-size:13px;\"><a href=\"{invite_link}\" target=\"_blank\" style=\"color:#0ea5e9;\">{invite_link}</a></p>
                  </td>
                </tr>
                <tr>
                  <td class=\"footer\">
                    Bu e-posta yanıtlanamaz (no-reply). Yardım için lütfen sistem yöneticinizle iletişime geçin.
                  </td>
                </tr>
              </table>
            </div>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """

    # Build and send message with optional inline image
    data = _get_email_settings(db)
    host = data.get("host") if data else None
    # Reuse send_email SMTP pipeline but we need to construct the message here to attach related part
    # We'll replicate the send_email logic minimally for this special case
    if data is None:
        raise RuntimeError("Email settings not configured")

    port = int(data.get("port") or 0)
    secure = (data.get("secure") or "starttls").lower()
    user = data.get("username")
    password = data.get("password")
    from_name = data.get("from_name") or "Sicilius"
    from_email = data.get("from_email")
    if not all([host, port, user, from_email]):
        raise RuntimeError("Incomplete SMTP settings (host/port/username/from_email required)")
    if not password:
        raise RuntimeError("SMTP password missing")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to
    msg.set_content(body_text or "")
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
    # Get email settings from database
    data = _get_email_settings(db)
    if not data:
        logger.warning("Email settings not configured in database, skipping contact notification")
        return
    
    host = data.get("host")
    port = int(data.get("port") or 587)
    secure = (data.get("secure") or "starttls").lower()
    user = data.get("username")
    password = data.get("password")
    from_name = data.get("from_name") or "Sicilius"
    from_email = data.get("from_email")
    
    if not all([host, port, user, from_email, password]):
        logger.warning("Incomplete SMTP settings in database, skipping contact notification")
        return
    
    msg = EmailMessage()
    msg["Subject"] = f"İletişim Formu: {subject}"
    msg["From"] = f"{from_name} <{from_email}>"
    msg["To"] = to_email
    msg["Reply-To"] = email
    
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
    
    # HTML content
    body_html = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <h2 style="color: #2563eb;">Yeni İletişim Formu Mesajı</h2>
    
    <table style="border-collapse: collapse; margin: 20px 0;">
        <tr>
            <td style="padding: 8px; font-weight: bold;">Ad Soyad:</td>
            <td style="padding: 8px;">{first_name} {last_name}</td>
        </tr>
        <tr>
            <td style="padding: 8px; font-weight: bold;">E-posta:</td>
            <td style="padding: 8px;"><a href="mailto:{email}">{email}</a></td>
        </tr>
        <tr>
            <td style="padding: 8px; font-weight: bold;">Konu:</td>
            <td style="padding: 8px;">{subject}</td>
        </tr>
    </table>
    
    <div style="background: #f9fafb; padding: 15px; border-left: 4px solid #2563eb; margin: 20px 0;">
        <h3 style="margin-top: 0;">Mesaj:</h3>
        <p style="white-space: pre-wrap;">{message}</p>
    </div>
    
    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
    <p style="color: #6b7280; font-size: 12px;">
        Bu mesaj Sicilius iletişim formundan gönderilmiştir.
    </p>
</body>
</html>
"""
    
    msg.set_content(body_text)
    msg.add_alternative(body_html, subtype="html")
    
    # Send email
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
        logger.info(f"Contact notification sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send contact notification: {e}")
        # Don't raise - contact form should still work even if email fails

