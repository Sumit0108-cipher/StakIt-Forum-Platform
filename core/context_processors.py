from notifications.models import Notification

def notification_context(request):
    if request.user.is_authenticated:
        all_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        notifications = all_notifications[:10]  # slicing
        unread_count = all_notifications.filter(is_read=False).count()  # filtering on unsliced queryset
        return {
            'notifications': notifications,
            'unread_notification_count': unread_count,
        }
    return {}

