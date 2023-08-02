from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board


@pytest.mark.django_db
class TestBoardView:
    url: str = reverse('goals:board_list')

    def test_board_create(self, client, auth_client):
        """ Тест на создание доски """
        url = reverse('goals:create_board')

        expected_response = {
            'created': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'updated': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'title': 'test board',
            'is_deleted': False
        }
        response = client.post(path=url, data=expected_response)

        assert response.status_code == status.HTTP_201_CREATED
        board = Board.objects.get()
        assert board.title == expected_response['title']
        assert response.data['is_deleted'] == expected_response['is_deleted']