from django.http import HttpResponseNotFound
from .models import Section, Direction
from django.shortcuts import render
from general.models import Article


def sections(request):
    context = {
        'types': Section.type_choices,
        'range': list(range(1, 19)),
        'directions': Direction.objects.all(),
        'articles': Article.objects.filter(is_published=True),
        'sections': Section.objects.filter(is_published=True).prefetch_related(
            'direction'
        )
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


def schedule(request):
    context = {
        'types': Section.type_choices,
        'departments': Section.department_choices,
        'sections': Section.objects.filter(is_published=True),
        'articles': Article.objects.filter(is_published=True)
    }

    return render(request, 'schedule.html', context)
