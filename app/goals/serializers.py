from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, GoalComment


# categories serializers

class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("created", "updated", "user")


class GoalCategoryWithUserSerializer(GoalCategorySerializer):
    user = UserSerializer(read_only=True)


# goals serializers


class GoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ("created", "updated", "user")

    def validate_category(self, value: GoalCategory) -> GoalCategory:
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalWithUserSerializer(GoalSerializer):
    user = UserSerializer(read_only=True)


# comments serializer

class GoalCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ("created", "updated", "user", "goal")

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Goal.Status.archived:
            raise ValidationError("Goal not found")
        if self.context['request'].user.id != value.user_id:
            raise PermissionDenied
        return value


class GoalCommentWithUserSerializer(GoalCommentSerializer):
    user = UserSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)
