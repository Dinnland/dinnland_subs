from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url

# Create your views here.
import random

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, RedirectURLMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView, ListView
from django.views.generic import *
from django.contrib.sites.shortcuts import get_current_site

from users.forms import UserRegisterForm, UserProfileForm, UserForgotPasswordForm, UserSetNewPasswordForm, UserCodeForm
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
    # success_url = reverse_lazy('users:login')
    # верификации
    success_url = reverse_lazy('users:verifyemail')

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


class SMSRegisterView(CreateView):
    """ Регистрация пользователя """
    model = User
    # form_class = UserForm
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    # это если без верификации
    # success_url = reverse_lazy('users:smscode')
    # верификации
    # success_url = reverse_lazy('users:verifyemail')

    success_url = reverse_lazy('users:smscode')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Функционал для отправки письма и генерации токена

        access_code = random.randrange(1000, 9999)
        print(f'это м сделали код {access_code}')
        user.access_code = access_code
        # Site.objects.clear_cache()
        kwargs = {'access_code': access_code}
        user.save()
        # send_mail(
        #     subject='Подтвердите свой электронный адрес',
        #     message=f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:'
        #             f' {current_site}{activation_url}',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[user.email],
        #     fail_silently=False,
        # )

        # Отправка кода на телефон
        # smsc = SMSC()
        # smsc.send_sms(profile.phone, "Your code: {}".format(access_code), sender = "sms")
        # return render(request, 'core/next.html', content)
        return redirect('users:smscode')

    def get_object(self, queryset=None):
        return self.request.user

# @login_required
# def verify_code(request):
#     if request.method == 'POST':
#         form = UserCodeForm(request.POST)
#         if form.is_valid():
#             access_code = form.cleaned_data.get('access_code')
#             if request.user.access_code, access_code:
#                 request.user.is_verified = True
#                 request.user.save()
#                 return redirect('index')
#     else:
#         form = VerifyForm()
#     return render(request, 'verify.html', {'form': form})

class SMSCodeView1(CreateView):
    """ Происходит проверка успешности подверждения access_code """
    model = User
    template_name = 'users/registration/sms_code.html'
    form_class = UserCodeForm

    # def get(self, request, access_token):
    #     pass
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context
    # def get(self, request):
    #     try:
    #         # uid = urlsafe_base64_decode(uidb64)
    #         # print(access_code)
    #
    #         # user = User.objects.get(pk=uid)
    #     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    #         user = None
    #     # f = sms_number
    #     # print(f'Получили код {f}')
    #     # if user is not None and sms_number=sms_number:
    #     #     user.is_active = True
    #     #     user.is_verified = True
    #     #     user.save()
    #     #     login(request, user)
    #     #     return redirect('users:email_confirmed')
    #     # else:
    #     #     return redirect('users:email_confirmation_failed')
    #     return redirect('users:login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return redirect('users:login')


class SMSCodeView(RedirectURLMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    # model = User

    # form_class = AuthenticationForm
    form_class = UserCodeForm
    # authentication_form = None
    UserCodeForm = None
    # template_name = "registration/login.html"
    template_name = 'users/registration/sms_code.html'

    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_form_class(self):
        return self.UserCodeForm or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    # def form_valid(self, form):
    #     """Security check complete. Log the user in."""
    #     auth_login(self.request, form.get_user())
    #     return HttpResponseRedirect(self.get_success_url())
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return redirect('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context






















class UserConfirmEmailView(View):
    """ Верификация пользователя по ссылке, отправленной на email """

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
    new_password = get_random_string(length=12)
    if request.user.email:
        send_mail(
                subject='Вы сменили пароль',
                message=f'Ваш новый пароль: {new_password}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                # fail_silently=False,
            )
        request.user.set_password(new_password)
        request.user.save()
        return redirect(reverse('users:DoneGenerateNewPassword'))
    else:
        return redirect('users:email_confirmation_failed')


def recovery_password(request):
    """Восстановление пароля"""
    if request.user.email:
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
        return redirect(reverse('users:DoneGenerateNewPassword'))
    else:
        return redirect('users:email_confirmation_failed')


class DoneGenerateNewPassword(TemplateView):
    """Реализация сообщения об успешном подтверждении email"""

    template_name = 'users/registration/done_gen_passw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пароль отправлен на почту'
        return context


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """Представление по сбросу пароля по почте"""

    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('publications:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Представление установки нового пароля"""

    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('publications:home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Страница для удаления User"""

    # PermissionRequiredMixin,
    model = User
    # fields = ('__all__')
    # fields = ('header', 'content', 'image')
    success_url = reverse_lazy('publications:home')

    # ограничение доступа анонимных пользователей # 19 Уведомление для неавторизованных пользователей
    # login_url = 'mail_upp:not_authenticated'
    permission_required = 'users.delete_user'
    # success_message = 'Материал был успешно Удален'


class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = User
    context_object_name = 'users_list'
    template_name = 'users/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()


