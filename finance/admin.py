from django.contrib import admin
from myconf.conf import get_model
from myconf import conf
# Register your models here.

admin.site.register(get_model(conf.STUDENT_DEBT))
admin.site.register(get_model(conf.INCOME))
admin.site.register(get_model(conf.EXPENSE))