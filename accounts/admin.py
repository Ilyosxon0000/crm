from django.contrib import admin
from django.contrib.auth import get_user_model
from myconf import conf
from django.contrib.auth.admin import UserAdmin
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
admin.site.register(get_user_model(), MyUserAdmin)
admin.site.register(conf.get_model(conf.TYPE_OF_ADMIN))
admin.site.register(conf.get_model(conf.PERMISSION))
admin.site.register(conf.get_model(conf.ADMIN))
admin.site.register(conf.get_model(conf.TEACHER))
admin.site.register(conf.get_model(conf.EMPLOYER))
admin.site.register(conf.get_model(conf.STUDENT))
admin.site.register(conf.get_model(conf.PARENT))