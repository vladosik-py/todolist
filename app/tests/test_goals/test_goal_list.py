from typing import Dict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from core.models import User
from goals.models import Goal
from goals.serializers import GoalWithUserSerializer
from tests.factories import BoardFactory, CategoryFactory, BoardParticipantFactory, GoalFactory


@pytest.mark.django_db
class TestGoalListView:
    """ Тесты на демонстрацию целей """

    url: str = reverse("goals:goal_list")

    def test_active_goal_list_participant(self, auth_client, user) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь может
        просматривать список созданных целей, оторых сам пользователь
        является участником доски.
        """
        board = BoardFactory()
        category = CategoryFactory(board=board)
        active_goals = GoalFactory.create_batch(size=5, category=category)
        BoardParticipantFactory(board=board, user=user)

        expected_response: Dict = GoalWithUserSerializer(active_goals, many=True).data
        sorted_expected_response: list = sorted(
            expected_response, key=lambda x: x["priority"]
        )
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "Запрос не прошел"
        assert response.json() == sorted_expected_response, "Списки целей не совпадают"

    def test_deleted_goal_list_participant(self, auth_client, user) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь не может
        просматривать список удаленных целей, в которых сам пользователь
        является участником.
        """
        board = BoardFactory()
        category = CategoryFactory(board=board)
        deleted_goals = GoalFactory.create_batch(
            size=5, category=category, status=Goal.Status.archived
        )
        BoardParticipantFactory(board=board, user=user)

        unexpected_response: Dict = GoalWithUserSerializer(deleted_goals, many=True).data
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"

    def test_goal_list_not_participant(self, auth_client, user: User) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь не может
        просматривать список удаленных целей, в которых сам пользователь
        не является участником.
        """
        board = BoardFactory()
        category = CategoryFactory(board=board)
        goals = GoalFactory.create_batch(size=5, category=category)
        BoardParticipantFactory(board=board, user=user)

        unexpected_response: Dict = GoalWithUserSerializer(goals, many=True).data
        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert response.json() == unexpected_response, "not your goals"

    def test_goal_create_deny(self, client) -> None:
        """
        Тест, который проверяет, что незарегистрированные пользователи
        не могут получить доступ к конечной точке API создания цели.
        """
        response: Response = client.post(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, "Отказ в доступе не предоставлен"