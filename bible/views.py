# bible/views.py
from django.db.models import Q

from requests import Response

from rest_framework import generics
from rest_framework.generics import ListAPIView

from .models import Version, Book, Verse
from .serializers import VersionSerializer, BookSerializer, VerseSerializer

class VersionListView(generics.ListAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        version_slug = self.kwargs['version_slug']
        print('version_slug: ', version_slug)
        return Book.objects.filter(verses__version__slug=version_slug).distinct()

class ChapterListView(generics.ListAPIView):
    def get(self, request, version_slug, book_slug):
        verses = Verse.objects.filter(version__slug=version_slug, book__slug=book_slug)
        chapters = verses.values_list('chapter', flat=True).distinct().order_by('chapter')
        return Response(chapters)

class VerseListView(generics.ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        version_slug = self.kwargs['version_slug']
        book_slug = self.kwargs['book_slug']
        chapter = self.kwargs['chapter']
        return Verse.objects.filter(
            version__slug=version_slug,
            book__slug=book_slug,
            chapter=chapter
        ).order_by('number')

class VerseSearchView(ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Verse.objects.filter(text__icontains=query)
