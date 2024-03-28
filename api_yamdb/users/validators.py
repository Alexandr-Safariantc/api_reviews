from django.core.exceptions import ValidationError


def check_username_for_me_value(username: str):
    """Return error if username got "me" value."""
    if username == 'me':
        raise ValidationError(
            message='Укажите корректный логин',
            params={'username': username}
        )
