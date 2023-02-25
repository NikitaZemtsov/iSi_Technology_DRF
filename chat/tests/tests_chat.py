from django.test import TestCase
from django.urls import reverse
from django.http import QueryDict

from rest_framework.test import APIRequestFactory, APITestCase, APIClient

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})


from chat.models import ThreadModel, MessageModel


class UserThreadTestCase(APITestCase):
    fixtures = ['user.json']

    def test_can_view_userthread(self):
        query_dictionary = QueryDict('', mutable=True)
        query_dictionary.update(
            {
                'user_id': 2
            }
        )
        url = '{base_url}?{querystring}'.format(
            base_url=reverse('threads'),
            querystring=query_dictionary.urlencode()
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'thread': []})

    def test_post_userthread(self):
        response = self.client.post(reverse('threads'), {'participants': [2, 3]}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'thread': [2, 3]})