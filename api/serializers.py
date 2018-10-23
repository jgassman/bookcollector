from rest_framework import serializers

from bookcollection.models import Author, Series


class AuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Author
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = '__all__'
