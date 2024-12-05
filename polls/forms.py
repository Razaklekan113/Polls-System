from django import forms
from django.forms import inlineformset_factory
from .models import Poll, Choice
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# PollForm for creating and editing polls
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']  # Poll question


# Inline formset for managing choices within a poll
ChoiceFormSet = inlineformset_factory(
    Poll, 
    Choice, 
    fields=('choice_text',), 
    extra=2,  # Default to 2 empty choices
    can_delete=True
)


# Custom user creation form
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
