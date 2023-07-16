from django.urls import path

from goals import views

urlpatterns = [
    path("goal_category/create", views.GoalCategoryCreateView.as_view(), name="create_category"),
    path("goal_category/list", views.GoalCategoryListView.as_view(), name="category_list"),
    path("goal_category/<int:pk>", views.GoalCategoryDetailView.as_view(), name="category_detail"),

    path("goal/create", views.GoalCreateView.as_view(), name="create_goal"),
    path("goal/list", views.GoalListView.as_view(), name="goal_list"),
    path("goal/<int:pk>", views.GoalDetailView.as_view(), name="goal_detail"),
]
