# bible/serializers.py

from rest_framework import serializers
from .models import Version, Book, Verse

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['name', 'slug']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'slug', 'testament']

class VerseSerializer(serializers.ModelSerializer):
    version = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    book = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Verse
        fields = ['version', 'book', 'chapter', 'number', 'text']
        
class RangeRequestSerializer(serializers.Serializer):
    version = serializers.CharField()
    book = serializers.CharField()
    ranges = serializers.ListField(child=serializers.CharField())

        