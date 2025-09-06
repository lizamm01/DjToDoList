from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ToDoList


class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "is_admin", "is_user", "is_active")
    list_filter = ("is_admin", "is_user", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permissions", {"fields": ("is_admin", "is_user", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_admin", "is_user", "is_active"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")


class ToDoListAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bajarilgan", "done_time", "user")
    list_filter = ("bajarilgan", "user")
    search_fields = ("title", "user__username")


admin.site.register(User, UserAdmin)
admin.site.register(ToDoList, ToDoListAdmin)
