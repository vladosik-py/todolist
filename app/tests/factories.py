import factory
from pytest_factoryboy import register
from core.models import User

from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


# core

@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs) -> User:
        return User.objects.create_user(*args, **kwargs)


class SignUpRequest(factory.DictFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    password_repeat = factory.LazyAttribute(lambda o: o.password)


# goals

@register
class CreateGoalCategoryRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


@register
class CreateGoalRequest(factory.DictFactory):
    title = factory.Faker('catch_phrase')


@register
class CreateGoalCommentRequest(factory.DictFactory):
    text = factory.Faker('sentence')
