from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters, generics
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment
from goals.permissions import GoalCategoryPermission, GoalPermission, GoalCommentPermission
from goals.serializers import GoalSerializer, GoalCategoryWithUserSerializer, GoalWithUserSerializer, \
    GoalCommentSerializer, \
    GoalCommentWithUserSerializer, GoalCategorySerializer


# categories views


class GoalCategoryCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer


class GoalCategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryWithUserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCategoryWithUserSerializer
    permission_classes = [GoalCategoryPermission]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').exclude(is_deleted=True)

    def perform_destroy(self, instance: GoalCategory):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=['is_deleted'])
            instance.goal_set.update(status=Goal.Status.archived)


# goals views


class GoalCreateView(generics.CreateAPIView):
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalWithUserSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = GoalDateFilter
    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority"]
    ordering = ["priority", "due_date"]

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(user=self.request.user, category__is_deleted=False
                                                          ).exclude(status=Goal.Status.archived)


class GoalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalWithUserSerializer
    permission_classes = [GoalPermission]
    queryset = Goal.objects.select_related('user').filter(category__is_deleted=False
                                                          ).exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance: Goal) -> None:
        instance.status = Goal.Status.archived
        instance.save(update_fields=['status'])


# comments views

class GoalCommentCreateView(generics.CreateAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalCommentListView(generics.ListAPIView):
    serializer_class = GoalCommentWithUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.select_related('user').filter(user=self.request.user)


class GoalCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentWithUserSerializer
    permission_classes = [GoalCommentPermission]
    queryset = GoalComment.objects.select_related('user')
