"""
URL configuration for NewsPaper project.

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
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
]

from django.urls import path
from .views import (
    NewsListView, NewsSearchView, NewsCreateView, NewsUpdateView, NewsDeleteView
)

urlpatterns = [
    path('', NewsListView.as_view(), name='news_list'),
    path('search/', NewsSearchView.as_view(), name='news_search'),


    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),


    path('articles/create/', NewsCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', NewsUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', NewsDeleteView.as_view(), name='article_delete'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('news/', include('news.urls')),
]

from django.contrib.auth.views import LoginView
from django.urls import path
from .views import edit_profile

urlpatterns = [
    path("accounts/login/", LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("profile/edit/", edit_profile, name="edit_profile"),
]

path("become_author/", become_author, name="become_author"),


