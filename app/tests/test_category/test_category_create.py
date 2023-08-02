from typing import Dict, Union

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.models import GoalCategory
from tests.factories import BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
class TestCategoryCreateView:
    url: str = reverse("goals:create_category")

    def test_category_create_owner(self, auth_client, user) -> None:
        """
        Тест, который проверяет, можно ли создать категорию,
        если пользователь является владельцем доски.
        """
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=user)

        create_data: Dict[str, Union[str, int]] = {
            "board": board.pk,
            "title": "Owner category",
        }

        response: Response = auth_client.post(self.url, data=create_data)
        created_category = GoalCategory.objects.filter(
            title=create_data["title"], board=board, user=user
        ).exists()

        assert response.status_code == status.HTTP_201_CREATED, "category is not created"
        assert created_category, "category not found"