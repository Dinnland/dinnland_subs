from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm

from subs.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):

    def __init__(self, *args, **kwargs):
        """Делаем поле 'email' - Readonly"""
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True

    def clean_email(self):
        """Функция clean_email гарантирует, что readonly значение не будет переопределено объектом POST."""
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email
        else:
            return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')  #, 'phone', 'avatar', 'country'
        # fields = ('__all__')


class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля
    """


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения
    """