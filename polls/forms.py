from django import forms
from django.forms import inlineformset_factory
from .models import Poll, Choice
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']  


ChoiceFormSet = inlineformset_factory(
    Poll, 
    Choice, 
    fields=('choice_text',), 
    extra=2, 
    can_delete=True
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("The two password fields must match.")
        return password2
