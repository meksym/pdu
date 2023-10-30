from django.urls import include, path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('sections/', sections, name='sections'),
    path('section/<int:pk>/', section, name='section'),
    path('news/', news),
    path('news/page<int:page_number>/', news, name='news'),
    path('news/<int:pk>/', one_news, name='one_news'),
    path('article/<int:pk>/', article, name='article'),
    path('schedule/', schedule, name='schedule'),
]
