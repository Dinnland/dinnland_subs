from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, SetPasswordForm, UsernameField
from django.utils.text import capfirst

from publications.forms import StyleFormMixin
from users.models import User, Payment
from django.contrib.auth.forms import UserCreationForm
from django import forms


UserModel = get_user_model()


class SubscriptionCreateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment_amount',)


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


# class UserCodeForm1(StyleFormMixin, forms.ModelForm, ):
#     class Meta:
#         model = User
#         fields = ('phone', 'access_code',)


class NewAccessCodeForm(StyleFormMixin, forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))

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

    # def clean(self):
    #     # username = self.cleaned_data.get("username")
    #     # access_code = self.cleaned_data.get("access_code")
    #     return self.cleaned_data

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