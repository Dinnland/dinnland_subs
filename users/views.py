from django.shortcuts import render

# Create your views here.
import random

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, ListView
from django.contrib.sites.shortcuts import get_current_site

from users.forms import UserRegisterForm, UserProfileForm, UserForgotPasswordForm, UserSetNewPasswordForm
from users.models import User
from django.utils.crypto import get_random_string
# User = get_user_model()

# Create your views here.


# # Это рабочее представление регистрации без верификации
# class RegisterView(CreateView):
#     model = User
#     # form_class = UserForm
#     form_class = UserRegisterForm
#     template_name = 'users/register.html'
#     # это если без верификации
#     success_url = reverse_lazy('users:login')
#     # верификации
#     # success_url = reverse_lazy('users:verifyemail')
#
#     def form_valid(self, form):
#         self.object = form.save()
#         #  self.object
#         send_mail(
#             subject='Поздравляем с регистрацией',
#             message='Вы зарегестрированы',
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[self.object.email]
#         )
#         return super().form_valid(form)
#
#     # , redirect('confirm_email'
# LoginRequiredMixin,

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    # template_name = 'users/register.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    """ Регистрация пользователя """
    model = User
    # form_class = UserForm
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    # это если без верификации
    success_url = reverse_lazy('users:login')
    # верификации
    # success_url = reverse_lazy('users:verifyemail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        user.save()

        # Функционал для отправки письма и генерации токена
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})
        # Site.objects.clear_cache()
        current_site = Site.objects.get_current().domain

        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:'
                    f' {current_site}{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return redirect('users:email_confirmation_sent')


class UserConfirmEmailView(View):
    """ Происходит проверка успешности подверждения email """
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    """Реализация сообщения об отправке письма для подтверждения email"""
    template_name = 'users/registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    """Реализация сообщения об успешном подтверждении email"""

    template_name = 'users/registration/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    """Реализация сообщения об НЕуспешном подтверждении email"""

    template_name = 'users/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


def generate_new_password(request):
    """Генерация пароля и отправка сообщения со ссылкой на почту"""
    # new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    new_password = get_random_string(length=12)
    send_mail(
            subject='Вы сменили пароль',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            # fail_silently=False,
        )
    request.user.set_password(new_password)
    request.user.save()
    # return  redirect(reverse('users:profile'))
    return redirect(reverse('users:done_generate_new_password'))


def recovery_password(request):
    """Восстановление пароля"""
    # make_password(
    # new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    new_password = get_random_string(length=12)
    send_mail(
            subject='Вы сменили пароль',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            # fail_silently=False,
        )
    request.user.set_password(new_password)
    request.user.save()
    # return  redirect(reverse('users:profile'))
    return redirect(reverse('users:done_generate_new_password'))


class done_generate_new_password(TemplateView):
    """Реализация сообщения об успешном подтверждении email"""

    template_name = 'users/registration/done_gen_passw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пароль отправлен на почту'
        return context


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('mail_app:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('mail_app:home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """страница для удаления User"""
    # PermissionRequiredMixin,
    model = User
    # fields = ('__all__')
    # fields = ('header', 'content', 'image')
    success_url = reverse_lazy('mail_app:home')

    # ограничение доступа анонимных пользователей # 19 Уведомление для неавторизованных пользователей
    # login_url = 'mail_upp:not_authenticated'
    permission_required = 'users.delete_user'
    success_message = 'Материал был успешно Удален'


class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    context_object_name = 'users_list'
    template_name = 'users/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()


class UserStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):

    def post(self, request, *args, **kwargs):
        mailing_id = kwargs['pk']
        new_status = request.POST.get('new_status')
        mailing = User.objects.get(pk=mailing_id)
        mailing.is_active = new_status
        mailing.save()
        return redirect('users:users_list')

    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()

