from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from django.shortcuts import render
from general.models import Article
from section.models import Section
from .models import News


def news(request, page_number: int = 1):
    news = News.objects.filter(is_published=True)

    context = {
        'types': Section.type_choices,
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True),
        'news': Paginator(news, 10).get_page(page_number)
    }

    return render(request, 'news.html', context)


def one_news(request, pk: int):
    try:
        news = News.objects.get(pk=pk)
    except News.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'types': Section.type_choices,
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True),
        'news': news
    }

    return render(request, 'one_news.html', context)
