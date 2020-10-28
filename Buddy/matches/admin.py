from django.contrib import admin
from .models import User_info, Hobby, Education, Friend_request, Message
# Register your models here.
admin.site.register(User_info)
admin.site.register(Hobby)
admin.site.register(Education)
admin.site.register(Friend_request)
admin.site.register(Message)
