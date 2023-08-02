from typing import Dict, Union

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.models import Goal
from tests.factories import BoardFactory, BoardParticipantFactory, CategoryFactory


@pytest.mark.django_db
class TestGoalCreateView:
    """ Тесты для работы с целями """
    url: str = reverse("goals:create_goal")

    def test_goal_create_owner(self, auth_client, user, due_date) -> None:
        """
        Тест, который проверяет, можно ли создать новую цель,
        если пользователь является владельцем доски.
        """
        board = BoardFactory()
        category = CategoryFactory(board=board)
        BoardParticipantFactory(board=board, user=user)

        create_data: Dict[str, Union[str, int]] = {
            "category": category.pk,
            "title": "New goal",
            "due_date": due_date,
        }

        response: Response = auth_client.post(self.url, data=create_data)
        created_goal = Goal.objects.filter(
            user=user, category=category, title=create_data["title"]
        ).exists()

        assert response.status_code == status.HTTP_201_CREATED, "goal is not created"
        assert created_goal, "goal not found"