"""
backend/app/services/email/resend_service.py

Thin wrapper around Resend for the two transactional emails the platform
sends: verify-your-email and reset-your-password. Deliberately fails soft
(logs, doesn't raise) when RESEND_API_KEY isn't configured — a missing
email provider in dev shouldn't block registration/login flows that don't
strictly require the email to have sent.
"""
import html as html_lib
import logging

import resend

from app.core.config import settings

logger = logging.getLogger(__name__)


def _send(to: str, subject: str, html: str) -> bool:
    if not settings.RESEND_API_KEY:
        logger.warning("RESEND_API_KEY not configured — skipping email send to %s (%s)", to, subject)
        return False
    resend.api_key = settings.RESEND_API_KEY
    try:
        resend.Emails.send({
            "from": settings.EMAIL_FROM,
            "to": [to],
            "subject": subject,
            "html": html,
        })
        return True
    except Exception:
        logger.exception("Failed to send email to %s (%s)", to, subject)
        return False


def send_verification_email(to: str, full_name: str, token: str) -> bool:
    # full_name is user-supplied and goes into an HTML document. Escaping
    # it stops a crafted display name from injecting markup (or a link)
    # into a mail our domain signs and sends.
    full_name = html_lib.escape(full_name or "there")
    link = f"{settings.FRONTEND_URL}/auth/login?verify_token={token}"
    html = f"""
    <div style="font-family:sans-serif;max-width:480px;margin:0 auto">
      <h2>Verify your email</h2>
      <p>Hi {full_name},</p>
      <p>Confirm your email address to finish setting up your Masar account.</p>
      <p><a href="{link}" style="display:inline-block;padding:10px 20px;background:#f5a623;color:#111;text-decoration:none;border-radius:6px;font-weight:600">Verify email</a></p>
      <p style="color:#888;font-size:12px">This link expires in 24 hours. If you didn't create this account, you can ignore this email.</p>
    </div>
    """
    return _send(to, "Verify your email", html)


def send_password_reset_email(to: str, full_name: str, token: str) -> bool:
    full_name = html_lib.escape(full_name or "there")
    # NOTE: the token is deliberately never logged here or anywhere else —
    # a reset link in an application log is a password reset for whoever
    # can read logs.
    link = f"{settings.FRONTEND_URL}/auth/login?reset_token={token}"
    html = f"""
    <div style="font-family:sans-serif;max-width:480px;margin:0 auto">
      <h2>Reset your password</h2>
      <p>Hi {full_name},</p>
      <p>Someone requested a password reset for this account. If that was you, click below to set a new password.</p>
      <p><a href="{link}" style="display:inline-block;padding:10px 20px;background:#f5a623;color:#111;text-decoration:none;border-radius:6px;font-weight:600">Reset password</a></p>
      <p style="color:#888;font-size:12px">This link expires in 1 hour and can only be used once. If you didn't request this, you can safely ignore this email — your password won't change.</p>
    </div>
    """
    return _send(to, "Reset your password", html)
