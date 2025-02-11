from django import forms
from django.contrib.auth.forms import UserCreationForm
from testapp.models import User, Instructor

class UserForm_byAdmin(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'address', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make password optional if we're editing an existing user
        if self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

