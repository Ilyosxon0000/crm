from django.contrib import admin
from .models import Type_of_Admin,Permission,Admin,Teacher,Student,Parent,Chat_room,Message,Davomat,Science

class List_Displey_Admin(admin.ModelAdmin):
    list_display=("id","user_id","user",)

admin.site.register(Type_of_Admin)
admin.site.register(Permission)
admin.site.register(Admin,List_Displey_Admin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Chat_room)
admin.site.register(Message)
admin.site.register(Davomat)
admin.site.register(Science)