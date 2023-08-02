from typing import Dict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.serializers import GoalCategoryWithUserSerializer, BoardSerializer
from tests.factories import BoardFactory, CategoryFactory, BoardParticipantFactory


@pytest.mark.django_db
class TestCategoryListView:
    """ Тесты на демонстрацию списка категорий """

    url: str = reverse("goals:category_list")

    def test_active_category_list_participant(self, auth_client, user) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь может
        просматривать список созданных категорий, в которых сам пользователь
        является участником доски.
        """
        board = BoardFactory()
        active_categories = CategoryFactory.create_batch(size=5, board=board)
        BoardParticipantFactory(board=board, user=user)

        expected_response: Dict = GoalCategoryWithUserSerializer(
            active_categories, many=True
        ).data
        sorted_expected_response: list = sorted(
            expected_response, key=lambda x: x["title"]
        )
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert response.json() == sorted_expected_response, "Category lists do not match"

    def test_deleted_category_list_participant(self, auth_client, user) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь не может
        просматривать список удаленных категорий, в которых сам пользователь
        является участником.
        """
        board = BoardFactory()
        deleted_categories = CategoryFactory.create_batch(
            size=5, board=board, is_deleted=True
        )
        BoardParticipantFactory(board=board, user=user)

        unexpected_response: Dict = GoalCategoryWithUserSerializer(
            deleted_categories, many=True
        ).data
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert not response.json() == unexpected_response, "Deleted categories received"

    def test_category_list_not_participant(self, auth_client) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь не может
        просматривать список категорий, в которых сам пользователь
        не является участником.
        """
        board = BoardFactory()
        categories = CategoryFactory.create_batch(size=5, board=board)
        BoardParticipantFactory(board=board)

        unexpected_response: Dict = BoardSerializer(categories, many=True).data
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert not response.json() == unexpected_response, "not your categories"

    def test_category_create_deny(self, client) -> None:
        """
        Тест, который проверяет, что незарегистрированные пользователи
        не могут получить доступ к конечной точке API создания категории.
        """
        response: Response = client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, "Access denied"