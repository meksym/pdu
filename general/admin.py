from django.contrib import admin
from . import models
from . import forms


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('type', 'is_published', 'changed_at')
    list_display = ('name', 'title', 'type', 'order_number', 'is_published',
                    'changed_at')

    search_fields = ('title', 'name')
    search_help_text = 'Можна шукати за заголовком'

    form = forms.ArticleAdminForm


@admin.register(models.ArticleFile)
class ArticleFileAdmin(admin.ModelAdmin):
    list_select_related = 'article',
    list_filter = 'article',
    list_display = 'name', 'article', 'file_name'

    def file_name(self, obj):
        return obj.file.name


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    list_filter = ('is_published', 'created_at')
    list_display = ('title', 'is_published', 'created_at')

    search_fields = 'title',
    search_help_text = 'Можна шукати за заголовком'

    exclude = 'created_at',
