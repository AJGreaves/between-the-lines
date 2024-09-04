from django.shortcuts import render
from django.views.generic import ListView
from .models import Book

# Create your views here.

# a ListView for home page that dispalys all the books
class BookListView(ListView):
    model = Book
    template_name = 'index.html'
    context_object_name = 'books'