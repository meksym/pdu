from django.contrib.admin import ModelAdmin, register
from .models import User, Section, News, Article, Banner, Direction
from .forms import SectionAdminForm, NewsAdminForm, ArticleAdminForm


@register(User)
class UserAdmin(ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'gender', 'is_active', 'last_login')
    list_filter = ('gender', 'is_active', 'last_login')
    exclude = ('last_login', 'user_permissions', 'password', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')

    def save_model(self, request, user, form, change):
        super().save_model(request, user, form, change)
        if not change:
            user.set_password('UqIefc67xm86i')
            user.save()


@register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ('name', 'department', 'is_published',
                    'is_active_record', 'date_of_last_change')
    list_filter = ('department', 'is_published',
                   'is_active_record', 'date_of_last_change', 'direction')
    form = SectionAdminForm
    search_fields = ('name',)


@register(News)
class NewsAdmin(ModelAdmin):
    list_display = ('title', 'is_published',
                    'date_of_published', 'date_of_last_change')
    list_filter = ('is_published', 'date_of_published', 'date_of_last_change')
    form = NewsAdminForm
    search_fields = ('title',)


@register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ('name', 'title', 'type', 'is_published', 'date_of_last_change')
    list_filter = ('type', 'is_published', 'date_of_last_change')
    form = ArticleAdminForm
    search_fields = ('title',)


@register(Banner)
class BannerAdmin(ModelAdmin):
    list_display = ('title', 'show_link', 'is_published', 'created_at')
    list_filter = ('show_link', 'is_published', 'created_at')
    exclude = ('created_at',)
    search_fields = ('title',)


@register(Direction)
class DirectionAdmin(ModelAdmin):
    pass
