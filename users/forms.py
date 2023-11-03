from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, SetPasswordForm

from publications.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):

    def __init__(self, *args, **kwargs):
        """Делаем поле 'email' and 'phone' - Readonly"""
        super(UserProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['phone'].widget.attrs['readonly'] = True
            # self.fields['email'].widget.attrs['readonly'] = True

    # def clean_phone(self):
    #     """Функция clean_phone гарантирует, что readonly значение не будет переопределено объектом POST."""
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return instance.email, instance.phone
    #     else:
    #         # return self.cleaned_data['phone'], self.cleaned_data['email']
    #         return self.cleaned_data['phone'], self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'avatar', 'country')  #, 'phone', 'avatar', 'country'
        # fields = ('__all__')


class UserForgotPasswordForm(StyleFormMixin, PasswordResetForm):
    """
    Запрос на восстановление пароля, используется с email
    """


class UserSetNewPasswordForm(StyleFormMixin, SetPasswordForm):
    """
    Изменение пароля пользователя после подтверждения, используется с email
    """