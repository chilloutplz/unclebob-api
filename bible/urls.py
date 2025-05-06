from django.urls import path
from . import views

urlpatterns = [
    path('', views.VersionListView.as_view(), name='version-list'),
    path('random/', views.RandomVerseView.as_view(), name='random-verse'),
    path('search/', views.VerseSearchView.as_view(), name='verse-search'),
    path('<str:version_slug>/', views.BookListView.as_view(), name='book-list'),
    path('<str:version_slug>/<str:book_slug>/', views.ChapterListView.as_view(), name='chapter-list'),
    path('<str:version_slug>/<str:book_slug>/<int:chapter>/numbers/', views.NumberListView.as_view(), name='number-list'),
    path('<str:version_slug>/<str:book_slug>/<int:chapter>/', views.VerseListView.as_view(), name='verse-list'),
    path('<str:version_slug>/<str:book_slug>/<int:chapter>/<int:number>/', views.SingleVerseView.as_view(), name='single-verse'),
]
