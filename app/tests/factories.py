import factory
from pytest_factoryboy import register
from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment

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


# boards

@register
class BoardFactory(factory.django.DjangoModelFactory):
    title = 'New Board'

    class Meta:
        model = Board


@register
class BoardParticipantFactory(factory.django.DjangoModelFactory):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


# categories

@register
class CategoryFactory(factory.django.DjangoModelFactory):
    title = 'New Category'
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalCategory


# goals

@register
class GoalFactory(factory.django.DjangoModelFactory):
    title = 'New Goal'
    description = 'Description of New Goal'
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)

    class Meta:
        model = Goal


@register
class GoalCommentFactory(factory.django.DjangoModelFactory):
    text = 'test comment'
    goal = factory.SubFactory(GoalFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = GoalComment
