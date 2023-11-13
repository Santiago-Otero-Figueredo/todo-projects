from fastapi import BackgroundTasks

from config.email import send_email
from config.settings import get_settings

from apps.users.models import User

settings = get_settings()


async def send_account_verification_email(user: User):
    from config.security import hash_password

    string_context = user.get_context_string(context=settings.USER_VERIFY_ACCOUNT)
    token = hash_password(string_context)
    activate_url = f"{settings.FRONTEND_HOST}/users/verify?token={token}&email={user.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": user.username,
        'activate_url': activate_url
    }
    subject = f"Account Verification - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification.html",
        context=data,
    )


async def send_account_activation_confirmation_email(user: User):
    data = {
        'app_name': settings.APP_NAME,
        "name": user.username,
        'login_url': f'{settings.FRONTEND_HOST}'
    }
    subject = f"Welcome - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/account-verification-confirmation.html",
        context=data,
    )

async def send_password_reset_email(user: User):
    from config.security import hash_password

    string_context = user.get_context_string(context=settings.FORGOT_PASSWORD)
    token = hash_password(string_context)
    reset_url = f"{settings.FRONTEND_HOST}/reset-password?token={token}&email={user.email}"
    data = {
        'app_name': settings.APP_NAME,
        "name": user.username,
        'activate_url': reset_url,
    }
    subject = f"Reset Password - {settings.APP_NAME}"
    await send_email(
        recipients=[user.email],
        subject=subject,
        template_name="user/password-reset.html",
        context=data,
    )
