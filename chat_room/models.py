from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import json

class Chat_room(models.Model):
    name=models.CharField(max_length=255,unique=True)
    users=models.ManyToManyField(get_user_model(),related_name='chat_rooms',blank=True)
    slug=models.SlugField(blank=True,null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.name)
        super().save(*args, **kwargs)
    
class Message(models.Model):
    chat_room=models.ForeignKey(Chat_room,related_name='messages',on_delete=models.CASCADE)
    from_user=models.ForeignKey(get_user_model(),related_name='from_messages',on_delete=models.CASCADE)
    to_user=models.ForeignKey(get_user_model(),related_name='to_messages',on_delete=models.CASCADE)
    message=models.TextField(blank=True,null=True)
    file_message=models.FileField(upload_to="uploads/message/%Y_%m_%d",blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chat_room.name}:{self.from_user.username} --> {self.to_user.username}"

    def get_date(self):
        return self.date.strftime('%d.%m.%Y %H:%M')
    
    def get_json_date(self):
        return json.dumps(self.date)
    
    def type_message(self):
        if self.file_message:
            return 'file_message'
        else:
            return 'word_message'