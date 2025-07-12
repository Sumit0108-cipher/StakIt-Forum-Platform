from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'url', 'is_read', 'timestamp')
    search_fields = ('recipient__username', 'message')
    list_filter = ('is_read', 'timestamp')