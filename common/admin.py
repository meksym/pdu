from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('gender', 'is_active', 'last_login')
    list_display = ('email', 'first_name', 'last_name', 'gender', 'is_active',
                    'last_login')

    search_fields = ('email', 'first_name', 'last_name')
    search_help_text = 'Можна шукати за наступними полями: ' \
                       'email, ім\'я, фамілія'

    exclude = ('last_login', 'user_permissions', 'is_superuser', 'password')

    def save_model(self, request, user, form, change):
        super().save_model(request, user, form, change)

        if not change:
            user.set_password('UqIefc67xm86i')
            user.save()
