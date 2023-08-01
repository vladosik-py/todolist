import factory
from pytest_factoryboy import register

from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


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
