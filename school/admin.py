from django.contrib import admin
from myconf import conf


# Register your models here.
admin.site.register(conf.get_model(conf.SCIENCE))
admin.site.register(conf.get_model(conf.CLASS))
admin.site.register(conf.get_model(conf.ATTENDANCE))
admin.site.register(conf.get_model(conf.ROOM))
admin.site.register(conf.get_model(conf.LESSON_TIME))
admin.site.register(conf.get_model(conf.LESSON))
admin.site.register(conf.get_model(conf.GRADE))
admin.site.register(conf.get_model(conf.TASK))
admin.site.register(conf.get_model(conf.TASK_FOR_CLASS))
admin.site.register(conf.get_model(conf.PARENT_COMMENT))
admin.site.register(conf.get_model(conf.TEACHER_LESSON))
admin.site.register(conf.get_model(conf.QUESTION))
admin.site.register(conf.get_model(conf.COMPANY))