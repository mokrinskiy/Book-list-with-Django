from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from unidecode import unidecode

class Genre(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = (
        ('Reading', 'Reading'),
        ('Read', 'Read'),
        ('To read', 'To read'),
        ('Postponed', 'Postponed'),
        ('Abandoned', 'Abandoned')
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, editable=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='To read')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_favorite = models.BooleanField(default=False)
    re_reads = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"book_slug": self.slug})
    
    def increment_rereads(self):
        self.re_reads += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.id or self.title != self.__class__.objects.get(id=self.id).title:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)


class SupportMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.subject}"