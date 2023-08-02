from typing import Dict

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.serializers import BoardSerializer
from tests.factories import BoardParticipantFactory, BoardFactory


@pytest.mark.django_db
class TestBoardView:
    """ Тесты на демонстрацию списка досок """

    url: str = reverse('goals:board_list')

    def test_active_board_list_participant(self, auth_client, user) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь может получить
        список созданных досок, в которых сам пользователь
        является участником доски.
        """
        active_boards = BoardFactory.create_batch(size=5)

        for board in active_boards:
            BoardParticipantFactory(board=board, user=user)

        expected_response: Dict = BoardSerializer(active_boards, many=True).data
        response: Response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert response.data == expected_response, "Boards lists do not match"

    def test_deleted_board_list_participant(self, auth_client, user) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь не может
        просматривать список удаленных досок, в которых сам пользователь
        является участником.
        """
        deleted_boards = BoardFactory.create_batch(size=5, is_deleted=True)

        for board in deleted_boards:
            BoardParticipantFactory(board=board, user=user)

        unexpected_response: Dict = BoardSerializer(
            deleted_boards, many=True
        ).data
        response: Response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert not response.data == unexpected_response, "Deleted boards received"

    def test_board_list_not_participant(self, auth_client) -> None:
        """
        Тест, который проверяет, что зарегистрированный пользователь не может
        просматривать список досок, в которых сам пользователь
        не является участником.
        """
        boards = BoardFactory.create_batch(size=5)

        for board in boards:
            BoardParticipantFactory(board=board)

        unexpected_response: Dict = BoardSerializer(boards, many=True).data
        response: Response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK, "request failed"
        assert not response.data == unexpected_response, "not your boards"

    def test_board_list_deny(self, client) -> None:
        """
        Тест, который проверяет, что незарегистрированные пользователи
        не могут получить доступ к конечной точке API создания досок.
        """
        response: Response = client.get(self.url)

        assert (response.status_code == status.HTTP_403_FORBIDDEN), "Access denied"


