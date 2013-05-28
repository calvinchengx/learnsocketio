from chat.models import ChatRoom, ChatUser
from django.contrib import admin


class ChatRoomAdmin(admin.ModelAdmin):
    pass


class ChatUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(ChatUser, ChatUserAdmin)
