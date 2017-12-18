from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board
from boards.views import BoardListView


class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django Board.')
        url = reverse('boards:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/boards/')
        self.assertEquals(view.func.view_class, BoardListView)

    def test_home_view_contains_link_to_topic_page(self):
        board_topics_url = reverse('boards:board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{}"'.format(board_topics_url))