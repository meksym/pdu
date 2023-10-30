from django.contrib import admin
from . import models
from . import forms


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_filter = ('is_published', 'date_of_published')
    list_display = ('title', 'is_published', 'date_of_published')

    search_fields = 'title',
    search_help_text = 'Можна шукати за заголовком'

    form = forms.NewsAdminForm
