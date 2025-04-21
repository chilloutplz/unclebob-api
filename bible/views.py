import random

from django.shortcuts import get_object_or_404
from django.db.models import Max

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
        try:
            verses = Verse.objects.filter(
                version__slug='우리말',
                book__testament='NT'
            )
            count = verses.count()
            if count == 0:
                return Response({"error": "신약 말씀을 찾을 수 없습니다."}, status=404)

            random_index = random.randint(0, count - 1)
            verse = verses[random_index]

            return Response({
                "version": verse.version.slug,
                "book": verse.book.name,
                "chapter": verse.chapter,
                "number": verse.number,
                "text": verse.text,
            }, content_type="charset=utf-8")
        except Exception as e:
            return Response({"error": str(e)}, status=500)
class VerseSearchView(ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Verse.objects.filter(text__icontains=query)
