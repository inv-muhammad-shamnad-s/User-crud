from django.core.exceptions import ValidationError
from ..models.user_model import User
from ..messages.error_messages import (
    EMAIL_ERROR_MESSAGES,
    USERNAME_ERROR_MESSAGES,
    ROLE_ERROR_MESSAGES,
)


def email_field_validation(email, instance=None):
    check_email_exists(email, instance=instance)
    check_length(email, "Email", min_length=0, max_lenth=50)
    return email


def username_field_validation(username, instance=None):
    check_length(username, "Username", min_length=3, max_lenth=50)
    check_username_exists(username, instance=instance)
    return username


def name_field_validation(name):
    check_length(name, "Name", min_length=3, max_lenth=50)
    return name


def password_validation(password):
    check_length(password, "Password", min_length=6, max_lenth=20)
    return password


def confirm_password_validation(confirm_password, password):
    if confirm_password != password:
        raise ValidationError("Password doesn't match")


def check_email_exists(email, instance=None):
    qs = User.objects.filter(email=email)
    if instance:
        qs = qs.exclude(id=instance.id)
    if qs.exists():
        raise ValidationError(EMAIL_ERROR_MESSAGES["user_exists"])


def check_username_exists(username, instance=None):
    qs = User.objects.filter(username=username)
    if instance:
        qs = qs.exclude(id=instance.id)
    if qs.exists():
        raise ValidationError(USERNAME_ERROR_MESSAGES["user_exists"])


def check_length(value, field, min_length, max_lenth):
    if len(value) < min_length:
        raise ValidationError(f"{field} must be atleast {min_length} characters long")
    if len(value) > max_lenth:
        raise ValidationError(f"{field} must be only {max_lenth} character long")


def role_validation(role):
    if role == 0:
        raise ValidationError(ROLE_ERROR_MESSAGES["admin_role"])
    if role not in [1,2,3] :
        raise ValidationError(ROLE_ERROR_MESSAGES["invalid"])
