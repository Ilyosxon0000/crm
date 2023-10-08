from django.contrib import admin
from myconf import conf
from .models import Each_Pay
# Register your models here.
admin.site.register(conf.get_model(conf.EXPENSE))
admin.site.register(conf.get_model(conf.STUDENT_PAY))
admin.site.register(Each_Pay)
