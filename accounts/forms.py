from django.contrib.auth.forms import UserCreationForm
from django.forms import forms


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             label='Email',
                             error_messages={'exists': 'Oops'})
