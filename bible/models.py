from django.db import models

class Version(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = 'bible.bibleversion'

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    testament = models.CharField(max_length=10, choices=(('신', '신약'), ('구', '구약약')))
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('slug',)
        ordering = ['order']
        db_table = 'bible.book'

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
        db_table = 'bible.verse'

    def __str__(self):
        return f"{self.version.slug} {self.book.slug} {self.chapter}:{self.number}"
