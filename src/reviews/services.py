from django.contrib.auth import get_user_model


User = get_user_model()


def create_user(*, username: str, password: str, email: str = '', first_name: str = '', last_name: str = ''):
    """Создание пользователя."""

    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    return user


def update_user(*, user: User, first_name: str, last_name: str, email: str, photo: str, dob: str, gender: str):
    """Изменение данных пользователя."""

    fields_to_update = {'first_name': first_name, 'last_name': last_name, 'email': email, 'photo': photo, 'dob': dob,
                        'gender': gender}

    for field, value in fields_to_update:
        setattr(user, field, value or getattr(user, field))
    user.save()
