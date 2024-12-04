from django import forms
from django.forms import inlineformset_factory
from .models import Poll, Choice

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']

ChoiceFormSet = inlineformset_factory(Poll, Choice, fields=('choice_text',), extra=2, can_delete=True)
