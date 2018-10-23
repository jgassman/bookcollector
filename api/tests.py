import simplejson as json
from django.test import TestCase

from api.serializers import AuthorSerializer
from bookcollection.models import Author


class AuthorSerializerTests(TestCase):

    def test_serializes_author_with_first_and_last_name(self):
        author = Author.objects.create(first_name='Terry', last_name='Pratchett')
        serialized = AuthorSerializer(author).data
        self.assertEqual(author.id, serialized['id'])
        self.assertEqual(author.first_name, serialized['first_name'])
        self.assertEqual(author.last_name, serialized['last_name'])

    def test_serializes_author_with_only_last_name(self):
        author = Author.objects.create(last_name='Homer')
        serialized = AuthorSerializer(author).data
        self.assertEqual(author.id, serialized['id'])
        self.assertEqual(None, serialized['first_name'])
        self.assertEqual(author.last_name, serialized['last_name'])


class AuthorTests(TestCase):

    def test_can_create_author_with_first_and_last_name(self):
        expected = {
            'data': {
                'id': '1',
                'type': 'authors',
                'attributes': {
                    'first_name': 'Ransom',
                    'last_name': 'Riggs'
                }
            }
        }
        data = {'data': {'attributes': {'first_name': 'Ransom', 'last_name': 'Riggs'}, 'type': 'authors'}}
        response = self.client.post('/api/authors', json.dumps(data), 'application/vnd.api+json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(Author.objects.count(), 1)
        author = Author.objects.all()[0]
        self.assertEqual(author.first_name, 'Ransom')
        self.assertEqual(author.last_name, 'Riggs')

    def test_can_create_author_with_only_last_name(self):
        expected = {
            'data': {
                'id': '1',
                'type': 'authors',
                'attributes': {
                    'first_name': None,
                    'last_name': 'Moliere'
                }
            }
        }
        data = {'data': {'attributes': {'first_name': None, 'last_name': 'Moliere'}, 'type': 'authors'}}
        response = self.client.post('/api/authors', json.dumps(data), 'application/vnd.api+json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(Author.objects.count(), 1)
        author = Author.objects.all()[0]
        self.assertEqual(author.first_name, None)
        self.assertEqual(author.last_name, 'Moliere')

    def test_can_get_list_of_authors(self):
        pratchett = Author.objects.create(first_name='Terry', last_name='Pratchett')
        homer = Author.objects.create(last_name='Homer')
        expected = [
            {
                'id': str(homer.pk),
                'type': 'authors',
                'attributes': {
                    'first_name': None,
                    'last_name': 'Homer'
                }
            }, {
                'id': str(pratchett.pk),
                'type': 'authors',
                'attributes': {
                    'first_name': 'Terry',
                    'last_name': 'Pratchett'
                }
            }
        ]
        response = self.client.get('/api/authors')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['data'], expected)

    def test_can_get_a_single_author(self):
        bronte = Author.objects.create(first_name='Anne', last_name='Bronte')
        expected = {
            'id': str(bronte.pk),
            'type': 'authors',
            'attributes': {
                'first_name': 'Anne',
                'last_name': 'Bronte'
            }
        }
        print('/api/authors/{}'.format(bronte.pk))
        response = self.client.get('/api/authors/{}'.format(bronte.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['data'], expected)
