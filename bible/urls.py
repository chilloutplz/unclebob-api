from django.urls import path
from . import views

urlpatterns = [
    path('versions/', views.VersionListView.as_view(), name='version-list'),
    path('<slug:version_slug>/books/', views.BookListView.as_view(), name='book-list'),
    path('<slug:version_slug>/<slug:book_slug>/chapters/', views.ChapterListView.as_view(), name='chapter-list'),
    path('<slug:version_slug>/<slug:book_slug>/<int:chapter>/verses/', views.VerseListView.as_view(), name='verse-list'),
    path('search/', views.VerseSearchView.as_view(), name='verse-search'),
]
