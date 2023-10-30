from django.contrib import admin
from . import models
from . import forms


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'is_published', 'is_active_record',
                    'changed_at')
    list_filter = ('department', 'is_published', 'is_active_record',
                   'changed_at', 'direction')

    search_fields = 'name',
    search_help_text = 'Можна шукати за назвою'

    form = forms.SectionAdminForm


@admin.register(models.Direction)
class DirectionAdmin(admin.ModelAdmin):
    pass
