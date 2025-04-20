from django.db import models

class Version(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    testament = models.CharField(max_length=10, choices=(('NT', 'New Testament'), ('OT', 'Old Testament')))

    class Meta:
        unique_together = ('slug',)
        ordering = ['id']

    def __str__(self):
        return self.name


class Verse(models.Model):
    version = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='verses')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='verses')
    chapter = models.PositiveIntegerField()
    number = models.PositiveIntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('version', 'book', 'chapter', 'number')
        ordering = ['version', 'book', 'chapter', 'number']

    def __str__(self):
        return f"{self.version.slug} {self.book.slug} {self.chapter}:{self.number}"
