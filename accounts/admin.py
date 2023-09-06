from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,Type_of_Admin,Permission,Admin,Teacher
from django.utils.translation import gettext_lazy as _


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"), 
            {
                "fields": (
                    "image",
                    "first_name", 
                    "last_name",
                    "middle_name",
                    "email",
                    "type_user"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
admin.site.register(UserProfile, MyUserAdmin)
admin.site.register(Type_of_Admin)
admin.site.register(Permission)
admin.site.register(Admin)
admin.site.register(Teacher)