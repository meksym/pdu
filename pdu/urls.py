from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path

from general import views as general
from section import views as section
from news import views as news


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', general.index, name='index'),
    path('article/<int:pk>/', general.article, name='article'),

    path('sections/', section.sections, name='sections'),
    path('section/<int:pk>/', section.section, name='section'),
    path('schedule/', section.schedule, name='schedule'),

    path('news/', news.news),
    path('news/page<int:page_number>/', news.news, name='news'),
    path('news/<int:pk>/', news.one_news, name='one_news'),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
