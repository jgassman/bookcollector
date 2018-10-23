from rest_framework import generics, renderers
from rest_framework_json_api.renderers import JSONRenderer

from api.serializers import AuthorSerializer
from bookcollection.models import Author


class AuthorListCreateView(generics.ListCreateAPIView):
    renderer_classes = (
        JSONRenderer,
        renderers.BrowsableAPIRenderer,
    )
    queryset = Author.objects.all()
    resource_name = 'authors'
    serializer_class = AuthorSerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = (
        JSONRenderer,
        renderers.BrowsableAPIRenderer,
    )
    queryset = Author.objects.all()
    resource_name = 'authors'
    serializer_class = AuthorSerializer
