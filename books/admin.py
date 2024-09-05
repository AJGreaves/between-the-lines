from django.contrib import admin
from .models import Book, Genre
from django.utils.text import slugify

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)