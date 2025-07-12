from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('ask/', views.ask_question, name='ask_question'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
