from django import forms
from django.contrib.auth.models import User
from account.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()   # username
    password = forms.CharField(widget=forms.PasswordInput)  # password


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password',
                                widget=forms.PasswordInput)
    password_1 = forms.CharField(label='Repeat password',
                                    widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password_1(self):
        """clean_<field> is used to test user/.
        check user input against our rules."""

        user_data = self.cleaned_data  # obtain user inputed data
        if user_data['password'] != user_data['password_1']:
            raise forms.ValidationError('Passwords don\'t match.')
        
        # return field we are checking
        return user_data['password_1']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')