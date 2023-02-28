from django.test import TestCase
from django.urls import reverse
from django.http import QueryDict

from freezegun import freeze_time
from datetime import datetime

from rest_framework.test import APIRequestFactory, APITestCase, APIClient

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})


from chat.models import ThreadModel, MessageModel


class UserThreadTestCase(APITestCase):
    fixtures = ['user.json']

    def test_post_userthread(self):
        with freeze_time(datetime(2023, 2, 18, hour=15, minute=1)):
            response = self.client.post(reverse('threads'), {'participants': [2, 3]}, format='json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'thread': {'created': '2023-02-18T15:01:00Z',
                                                          'message': [],
                                                      'participants': [2, 3],
                                                      'pk': 1,
                                                      'updated': '2023-02-18T15:01:00Z'}})

        response_2 = self.client.post(reverse('threads'), {'participants': [2, 3]}, format='json')
        self.assertEqual(response_2.json(), {'thread': {'created': '2023-02-18T15:01:00Z',
                                                        'message': [],
                                                      'participants': [2, 3],
                                                      'pk': 1,
                                                      'updated': '2023-02-18T15:01:00Z'}})

    def test_post_userthread_one_user_fail(self):
        response = self.client.post(reverse('threads'), {'participants': [2]}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'participants': ['Participants should consist only two users pk.']})

    def test_can_view_userthread(self):
        url = '{base_url}?user_id=2'.format(base_url=reverse('threads'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'thread': []})

    def test_user_threads(self):
        with freeze_time(datetime(2023, 2, 18, hour=15, minute=1)):
            self.client.post(reverse('threads'), {'participants': [2, 3]}, format='json')
            self.client.post(reverse('threads'), {'participants': [2, 4]}, format='json')
        url = '{base_url}?user_id=2'.format(base_url=reverse('threads'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'thread': [{'created': '2023-02-18T15:01:00Z',
                                                       'message': [],
                                                       'participants': [2, 3],
                                                       'pk': 1,
                                                       'updated': '2023-02-18T15:01:00Z'},
                                                      {'created': '2023-02-18T15:01:00Z',
                                                       'message': [],
                                                       'participants': [2, 4],
                                                       'pk': 2,
                                                       'updated': '2023-02-18T15:01:00Z'}]})

class ThreadApiViewTestCase(APITestCase):
    fixtures = ['user.json']

    def test_thread_api_view_POST(self):
        response = self.client.post(reverse('threads'), {'participants': [2, 3]}, format='json')
        pk = response.json().get('thread').get('pk')
        with freeze_time(datetime(2023, 2, 18, hour=15, minute=1)):
            response = self.client.post(reverse('thread', args=[pk]), [{'text': 'HELLO_WORLD}'}, ], format='json')
        self.assertEqual(response.json(), {'message': [{'created': '2023-02-18T15:01:00Z',
                                                        'is_read': False,
                                                        'pk': 1,
                                                        'sender': 2,
                                                        'text': 'HELLO_WORLD}',
                                                        'thread': 1}]})

    def test_thread_api_view_GET(self):
        texts = ['HELLO_WORLD}', 'wikki', 'JOJO']
        response = self.client.post(reverse('threads'), {'participants': [2, 3]}, format='json')
        pk = response.json().get('thread').get('pk')
        minute = 1
        for text in texts:
            with freeze_time(datetime(2023, 2, 18, hour=15, minute=minute)):
                self.client.post(reverse('thread', args=[pk]), [{'text': text}, ], format='json')
            minute += 1
        response = self.client.get(reverse('thread', args=[pk]))
        self.assertEqual(response.json(), {'message': [{'sender': 2,
                                                        'text': 'JOJO',
                                                        'thread': 1,
                                                        'is_read': False,
                                                        'created': '2023-02-18T15:03:00Z',
                                                        'pk': 3
                                                        },
                                                       {'sender': 2,
                                                        'text': 'wikki',
                                                        'thread': 1,
                                                        'is_read': False,
                                                        'created': '2023-02-18T15:02:00Z',
                                                        'pk': 2
                                                        },
                                                       {'sender': 2,
                                                        'text': 'HELLO_WORLD}',
                                                        'thread': 1,
                                                        'is_read': False,
                                                        'created': '2023-02-18T15:01:00Z',
                                                        'pk': 1
                                                        }
                                                       ]})
