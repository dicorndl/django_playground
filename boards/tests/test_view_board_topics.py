from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board
from boards.views import TopicListView


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('boards:board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('boards:board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topic_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('boards:board_topics', kwargs={'pk': 1})
        homepage_url = reverse('boards:home')
        new_topic_url = reverse('boards:new_topic', kwargs={'pk': 1})

        response = self.client.get(board_topics_url)

        self.assertContains(response, 'href="{}"'.format(homepage_url))
        self.assertContains(response, 'href="{}"'.format(new_topic_url))