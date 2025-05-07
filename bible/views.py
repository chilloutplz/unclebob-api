import random

from django.shortcuts import get_object_or_404
from django.db.models import Max

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer

from .models import Version, Book, Verse
from .serializers import VersionSerializer, BookSerializer, VerseSerializer, RangeRequestSerializer

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

    # 이 뷰만 누구나(토큰 없이) 접근 가능하도록 설정
    permission_classes = [AllowAny]
    # JSONRenderer 를 명시적으로 사용
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try:
             # 우리말 버전 신약만 필터
            verses = Verse.objects.filter(
                version__slug='우리말',
                book__testament='NT'
            )
            count = verses.count()
            if count == 0:
                return Response({"error": "신약 말씀을 찾을 수 없습니다."}, status=404)

            random_index = random.randint(0, count - 1)
            verse = verses[random_index]

            # DRF Response 는 renderer_classes 에 따라 JSON으로 직렬화하며
            # settings.UNICODE_JSON = True 이면 한글도 제대로 인코딩 됩니다.
            return Response({
                "version": verse.version.slug,
                "book": verse.book.name,
                "chapter": verse.chapter,
                "number": verse.number,
                "text": verse.text,
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
class VerseSearchView(ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Verse.objects.filter(text__icontains=query)

class NumberListView(generics.ListAPIView):
    def get(self, request, version_slug, book_slug, chapter):
        verses = Verse.objects.filter(version__slug=version_slug, book__slug=book_slug, chapter=chapter)
        numbers = verses.values_list('number', flat=True).distinct().order_by('number')
        return Response(numbers)
    
    
class MultiRangeVerseView(GenericAPIView):
    serializer_class = RangeRequestSerializer  # ✨ 중요

    def post(self, request):
        serializer = self.get_serializer(data=request.data.get("requests", []), many=True)
        serializer.is_valid(raise_exception=True)

        results = []
        for item in serializer.validated_data:
            version_slug = item["version"]
            book_slug = item["book"]
            ranges = item["ranges"]

            try:
                version = Version.objects.get(slug=version_slug)
                book = Book.objects.get(slug=book_slug)
            except (Version.DoesNotExist, Book.DoesNotExist):
                results.append({
                    "version": version_slug,
                    "book": book_slug,
                    "error": "Invalid version or book"
                })
                continue

            all_verses = Verse.objects.none()
            for r in ranges:
                try:
                    start, end = r.split('-')
                    sc, sv = map(int, start.split(','))
                    ec, ev = map(int, end.split(','))
                except ValueError:
                    continue

                verses = Verse.objects.filter(version=version, book=book).filter(
                    chapter__gt=sc, chapter__lt=ec
                ) | Verse.objects.filter(
                    version=version, book=book, chapter=sc, number__gte=sv
                ) | Verse.objects.filter(
                    version=version, book=book, chapter=ec, number__lte=ev
                )

                all_verses |= verses

            serialized = VerseSerializer(all_verses.order_by("chapter", "number"), many=True)
            results.append({
                "version": version.slug,
                "book": book.slug,
                "verses": serialized.data
            })

        return Response({"results": results})