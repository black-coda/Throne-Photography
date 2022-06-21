from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from main.models import Category, PhotoGraphy

User = get_user_model()
admin.site.register(Category)
admin.site.register(PhotoGraphy)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            "fields": (
                'avatar', 'bio'
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": (
                'email', 'avatar', 'bio'
            ),
        }),
    )
