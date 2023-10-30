from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *


def index(request):
    context = {
        'types': Section.type_choices,
        'departments': Section.department_choices,
        'banners': Banner.objects.filter(is_published=True)[:5],
        'news': News.objects.filter(is_published=True)[:24],
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True)
    }

    return render(request, 'index.html', context)


def sections(request):
    context = {
        'types': Section.type_choices,
        'range': list(range(1, 19)),
        'directions': Direction.objects.all(),
        'articles': Article.objects.filter(is_published=True),
        'sections': Section.objects.filter(is_published=True).prefetch_related('direction')
    }

    return render(request, 'sections.html', context)


def section(request, pk: int):
    try:
        section = Section.objects.get(pk=pk)
    except Section.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'types': Section.type_choices,
        'section': section,
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True)
    }

    return render(request, 'section.html', context)


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


def article(request, pk: int):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'types': Section.type_choices,
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True),
        'article': article
    }

    return render(request, 'article.html', context)

def schedule(request):
    context = {
        'types': Section.type_choices,
        'departments': Section.department_choices,
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True)
    }

    return render(request, 'schedule.html', context)