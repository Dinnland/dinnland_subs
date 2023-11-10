from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm, \
    UsernameField
from django.core.exceptions import ValidationError
from django.utils.text import capfirst

from publications.forms import StyleFormMixin
from users.models import User
# from class FormName(forms.Form):
from django.contrib.auth.forms import UserCreationForm
from django import forms
# .PasswordResetForm

# class SmsForm(forms.ModelForm):
#     sms_field = forms.IntegerField(label=('ebat'))
#     class Meta:
#
#         fields = ('sms_field',)
UserModel = get_user_model()


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):

    def __init__(self, *args, **kwargs):
        """Делаем поле 'phone' - Readonly"""
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['phone'].widget.attrs['readonly'] = True

    def clean_phone(self):
        """Функция clean_phone гарантирует, что readonly значение не будет переопределено объектом POST."""
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.phone
        else:
            return self.cleaned_data['phone']

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'avatar', 'country')
        # fields = ('__all__')


# class UserCodeForm(StyleFormMixin, ):
#
#     class Meta:
#         model = User
#         fields = ('access_code',)
#         exclude = ('password1','password2')
class UserCodeForm1(StyleFormMixin, forms.ModelForm, ):
    class Meta:
        model = User
        fields = ('phone', 'access_code',)
        # fields = ('__all__')

        # access_code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class NewPasswordForm(StyleFormMixin, forms.Form):
    error_messages = {
        "password_mismatch": ("The two password fields didn’t match."),
    }

    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="Повторите новый пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     super().__init__(*args, **kwargs)

    # def clean_new_password2(self):
    #     password1 = self.cleaned_data.get("new_password1")
    #     password2 = self.cleaned_data.get("new_password2")
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError(
    #             self.error_messages["password_mismatch"],
    #             code="password_mismatch",
    #         )
    #     password_validation.validate_password(password2, self.user)
    #     return password2

class NewAccessCodeForm(StyleFormMixin, forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    # password =

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)
    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #
    #     return self.cleaned_data
    #
    # def get_user(self):
    #     return self.user_cache




# 6814
class UserCodeForm(StyleFormMixin, forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))
    access_code = forms.CharField(max_length=8, required=True, help_text='Enter code')


    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        username_max_length = self.username_field.max_length or 254
        self.fields["username"].max_length = username_max_length
        self.fields["username"].widget.attrs["maxlength"] = username_max_length
        if self.fields["username"].label is None:
            self.fields["username"].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get("username")
        # password = self.cleaned_data.get("password")
        access_code = self.cleaned_data.get("access_code")

        # if username is not None and access_code:  # password
        #     self.user_cache = authenticate(
        #         self.request, username=username, access_code=access_code
        #     )
        #     if self.user_cache is None:
        #         raise self.get_invalid_login_error()
        #     else:
        #         self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_user(self):
        return self.user_cache



class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля, используется с email
    """


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения, используется с email
    """