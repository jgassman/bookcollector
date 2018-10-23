import simplejson as json
from django.test import TestCase

from api.serializers import SeriesSerializer
from bookcollection.models import Series


class SeriesSerializerTests(TestCase):

    def test_serializes_series(self):
        series = Series.objects.create(name='Discworld')
        serialized = SeriesSerializer(series).data
        self.assertEqual(series.id, serialized['id'])
        self.assertEqual(series.name, serialized['name'])


class SeriesTests(TestCase):

    def test_can_create_series(self):
        expected = {
            'data': {
                'id': '1',
                'type': 'series',
                'attributes': {
                    'name': 'Mary Poppins',
                }
            }
        }
        data = {'data': {'attributes': {'name': 'Mary Poppins'}, 'type': 'series'}}
        response = self.client.post('/api/series', json.dumps(data), 'application/vnd.api+json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.content), expected)
        self.assertEqual(Series.objects.count(), 1)
        series = Series.objects.all()[0]
        self.assertEqual(series.name, 'Mary Poppins')

    def test_can_get_list_of_series(self):
        warriors = Series.objects.create(name='Warriors')
        potter = Series.objects.create(name='Harry Potter')
        expected = [
            {
                'id': str(potter.pk),
                'type': 'series',
                'attributes': {
                    'name': 'Harry Potter'
                }
            }, {
                'id': str(warriors.pk),
                'type': 'series',
                'attributes': {
                    'name': 'Warriors'
                }
            }
        ]
        response = self.client.get('/api/series')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['data'], expected)

    def test_can_get_a_single_series(self):
        shadowrun = Series.objects.create(name='Shadowrun')
        expected = {
            'id': str(shadowrun.pk),
            'type': 'series',
            'attributes': {
                'name': 'Shadowrun'
            }
        }
        response = self.client.get('/api/series/{}'.format(shadowrun.pk))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['data'], expected)
