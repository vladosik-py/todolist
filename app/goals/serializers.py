from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.request import Request

from core.serializers import UserSerializer
from core.models import User
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


# boards serializers

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.editable_roles)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def validate_user(self, user: User) -> User:
        if self.context['request'].user == user:
            raise ValidationError('Failed to change your role')
        return user

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "board")


class BoardWithParticipantsSerializer(BoardSerializer):
    participants = BoardParticipantSerializer(many=True)

    def update(self, instance: Board, validated_data: dict) -> Board:
        request: Request = self.context['request']

        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=request.user).delete()
            BoardParticipant.objects.bulk_create(
                [
                    BoardParticipant(user=participant['user'], role=participant['role'], board=instance)
                    for participant in validated_data.get('participants', [])
                ],
                ignore_conflicts=True,
            )

            if title := validated_data.get('title'):
                instance.title = title

            instance.save()

        return instance


# categories serializers


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_board(self, value):

        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted project")
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user,
        ).exists()

        if not allow:
            raise serializers.ValidationError("must be owner or writer in project")

        return value


class GoalCategoryWithUserSerializer(GoalCategoryCreateSerializer):
    user = UserSerializer(read_only=True)


# goals serializers

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted project")
        allow = BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user=self.context["request"].user,
        ).exists()
        if not allow:
            raise serializers.ValidationError("must be owner or writer in project")
        return value


class GoalWithUserSerializer(GoalSerializer):
    user = UserSerializer(read_only=True)


# comments serializer

class GoalCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ("id", "created", "updated", "user")

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError("Goal not found")

        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context['request'].user
        ).exists():
            raise PermissionDenied
        return value


class GoalCommentWithUserSerializer(GoalCommentSerializer):
    user = UserSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)
