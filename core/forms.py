from django import forms
from .models import Question, Answer,Tag
from django_ckeditor_5.widgets import CKEditor5Widget 

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Django, React, JWT'}),
        help_text='Enter comma-separated tags.'
    )
    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditor5Widget(config_name='default'), 
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
        }
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': CKEditor5Widget(config_name='default'), 
        }