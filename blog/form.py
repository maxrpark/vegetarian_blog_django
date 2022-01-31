from cProfile import label
from dataclasses import fields
from django import forms

from .models import Comments


class commentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['article']
        labels = {
            "name": "Your name mate"
        }
