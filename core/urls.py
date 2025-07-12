from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('answer/<int:answer_id>/accept/', views.accept_answer, name='accept_answer'),
    path('answer/<int:answer_id>/upvote/', views.upvote_answer, name='upvote_answer'),
]
