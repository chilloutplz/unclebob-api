import random

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Version, Book, Verse
from .serializers import VersionSerializer, BookSerializer, VerseSerializer

class VersionListView(generics.ListAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

class BookListView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        version_slug = self.kwargs['version_slug']
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

class SingleVerseView(RetrieveAPIView):
    serializer_class = VerseSerializer

    def get_object(self):
        version_slug = self.kwargs['version_slug']
        book_slug = self.kwargs['book_slug']
        chapter = self.kwargs['chapter']
        number = self.kwargs['number']
        
        return get_object_or_404(
            Verse,
            version__slug=version_slug,
            book__slug=book_slug,
            chapter=chapter,
            number=number
        )
    
class RandomVerseView(APIView):
    def get(self, request):
        count = Verse.objects.count()
        if count == 0:
            return Response({"error": "No verses found."}, status=404)
        random_index = random.randint(0, count - 1)
        verses = Verse.objects.all()[random_index]
        return Response({
            "version": verses.version.slug,
            "book": verses.book.slug,
            "chapter": verses.chapter,
            "number": verses.number,
            "text": verses.text
        })
class VerseSearchView(ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Verse.objects.filter(text__icontains=query)
