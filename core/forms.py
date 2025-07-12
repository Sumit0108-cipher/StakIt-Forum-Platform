from django import forms
from .models import Question
from django_ckeditor_5.widgets import CKEditor5Widget  # ✅ important

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': CKEditor5Widget(config_name='default'), 
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }