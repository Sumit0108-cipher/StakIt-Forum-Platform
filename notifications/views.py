from django.shortcuts import render
from django.shortcuts import redirect

def mark_all_as_read(request):
    request.user.notifications.update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))