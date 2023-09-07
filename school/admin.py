from django.contrib import admin
from myconf import conf


# Register your models here.
admin.site.register(conf.get_model(conf.SCIENCE))
admin.site.register(conf.get_model(conf.CLASS))
admin.site.register(conf.get_model(conf.ATTENDANCE))
admin.site.register(conf.get_model(conf.ROOM))
admin.site.register(conf.get_model(conf.LESSON_TIME))
admin.site.register(conf.get_model(conf.LESSON))