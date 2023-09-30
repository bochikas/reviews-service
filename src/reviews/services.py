import datetime

from django.contrib.auth import get_user_model

from reviews.models import Review

User = get_user_model()


def create_user(*, username: str, password: str, email: str = '', first_name: str = '', last_name: str = '') -> User:
    """Создание пользователя."""

    user = User(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()
    return user


def update_user(*, user: User, first_name: str = '', last_name: str = '', email: str = '', photo: str = None,
                dob: datetime.date = None, gender: str = None) -> None:
    """Изменение данных пользователя."""

    fields_to_update = {'first_name': first_name, 'last_name': last_name, 'email': email, 'photo': photo, 'dob': dob,
                        'gender': gender}

    for field, value in fields_to_update.items():
        if value:
            setattr(user, field, value)
    user.save()


def create_update_review(data: dict, instance: Review = None):
    """Создание/редактирование объекта обзора."""

    pluses = data.pop('pluses', None)
    minuses = data.pop('minuses', None)
    if review := instance:
        for field, value in data.items():
            setattr(review, field, value)
        review.save()
    else:
        review = Review.objects.create(**data)
    if pluses:
        review.pluses.add(*pluses)
    if minuses:
        review.minuses.add(*minuses)
    return review
