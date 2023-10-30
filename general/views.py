from .models import Article, ArticleFile, Banner
from django.http import HttpResponseNotFound
from django.shortcuts import render
from section.models import Section
from news.models import News


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


def article(request, pk: int):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponseNotFound()

    context = {
        'types': Section.type_choices,
        'documents': ArticleFile.objects.filter(article=article),
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True),
        'article': article
    }

    return render(request, 'article.html', context)
