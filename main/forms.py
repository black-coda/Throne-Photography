from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

User = get_user_model()


class LoginForm(forms.Form):
    email_or_username = forms.CharField(max_length=255, label="Email / Username")
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        print(email_or_username)
        try:
            user = User.objects.get(Q(username__iexact=email_or_username) | Q(email__iexact=email_or_username))
        except User.DoesNotExist:
            raise forms.ValidationError(f'We cant find this user with this {email_or_username}')
        return email_or_username

    def clean_password(self):
        email_or_username = self.cleaned_data.get('email_or_username')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get((Q(username__iexact=email_or_username) | Q(email__iexact=email_or_username)))
        except:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError('invalid Password')
        elif user is None:
            pass
        else:
            return password


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and /./+/-/_ only.'),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password1', 'password2', 'username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if '@' in username:
            raise forms.ValidationError('username cannot contain @')
        userCount = User.objects.filter(username=username).count()
        if userCount > 1:
            raise forms.ValidationError(
                'This Username Has been taken already'
            )
        return username


class ChangePasswordForm(SetPasswordForm):
    old_password = forms.CharField(
        label=_('Old Password'),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ),
    )

    field_order = ['old_password', 'new_password', 'new_password2']

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect']
            )
        return old_password
