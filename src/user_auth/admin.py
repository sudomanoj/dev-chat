from django.contrib import admin
from .models import User, ChatGroup, UserGroup
# Register your models here.

admin.site.register(User)
admin.site.register(ChatGroup)
admin.site.register(UserGroup)