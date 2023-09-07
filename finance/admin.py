from django.contrib import admin
from myconf import conf
# Register your models here.
admin.site.register(conf.get_model(conf.FINANCE))
admin.site.register(conf.get_model(conf.STUDENT_PAY))
