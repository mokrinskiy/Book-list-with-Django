from django.contrib import admin
from .models import *

class BookAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'slug', 'genre', 'author', 'status', 'date_added', 'date_updated', 'is_favorite', 're_reads']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']

class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']

class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'message']

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(SupportMessage)