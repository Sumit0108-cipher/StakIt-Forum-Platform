from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.
from django.db import models
from django.conf import settings
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self): 
        return self.name

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='default', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = CKEditor5Field(config_name='default', blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
