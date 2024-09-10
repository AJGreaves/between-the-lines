"""
URL configuration for between_the_lines project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import book_detail_view, books_by_genre_view

urlpatterns = [
    path('<int:pk>/<slug:slug>/', book_detail_view, name='book_detail'),
    path('genre/<slug:slug>/', books_by_genre_view, name='books_by_genre'),
]