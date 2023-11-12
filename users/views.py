import random
import stripe
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import *
from rest_framework import generics
from rest_framework.generics import get_object_or_404

from users.forms import (UserRegisterForm, UserProfileForm, UserForgotPasswordForm, UserSetNewPasswordForm,
                         UserCodeForm, NewAccessCodeForm, SubscriptionCreateForm)
from users.models import User, Payment
from pprint import pprint
from smsaero import SmsAero
from users.serializers.serializers import PaymentSerializer
from users.services import get_session, retrieve_session

SMSAERO_EMAIL = settings.SMSAERO_EMAIL
SMSAERO_API_KEY = settings.SMSAERO_API


class ProfileView(LoginRequiredMixin, UpdateView):
    """ Просмотр профиля пользователя """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """Страница для удаления User"""
    model = User
    success_url = reverse_lazy('publications:home')
    permission_required = 'users.delete_user'


class UsersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Список пользователей"""
    model = User
    context_object_name = 'users_list'
    template_name = 'users/users_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='moderator').exists()

# Работа с аккаунтом по email


class EmailRegisterView(CreateView):
    """ Регистрация пользователя по email"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

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
    """Сообщения - неуспешное подтверждение email"""
    template_name = 'users/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


class DoneGenerateNewPassword(TemplateView):
    """Пароль отправлен на почту"""
    template_name = 'users/registration/done_gen_passw.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пароль отправлен на почту'
        return context


class UserForgotPasswordEmailView(SuccessMessageMixin, PasswordResetView):
    """Представление по сбросу пароля по почте"""
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('users:done_generate_new_password')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Установки нового пароля"""
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('publications:home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
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
        return redirect(reverse('users:done_generate_new_password'))
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


# Работа с аккаунтом по телефону


class PhoneRegisterView(CreateView):
    """ Регистрация пользователя по телефону"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:access-code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        # Функционал для генерации кода и его отправки
        generate_access_code(self, db_user=user, message='Your code:')
        return redirect('users:access-code')

    def get_object(self, queryset=None):
        return self.request.user


class PhoneCodeView(FormView):
    """ Проверка успешности подтверждения access_code, активация аккаунта """
    model = User
    template_name = 'users/registration/access_code.html'
    form_class = UserCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение access_code'
        return context

    def form_valid(self, form):
        form_user = form.cleaned_data['username']
        form_access_code = form.cleaned_data['access_code']
        db_user = User.objects.filter(phone=form_user)
        if db_user:
            db_user = db_user[0]
            db_user_access_code = db_user.access_code
            if form_access_code == db_user_access_code:
                db_user.is_active = True
                db_user.is_verified = True
                db_user.access_code = None
                db_user.save()
                return redirect('users:login')
            else:
                return redirect('users:access_code_failed')
        else:
            return redirect('users:user_doesnt_exist')


class SendAccessCodeView(FormView):
    """ Отправка нового access_code """
    model = User
    template_name = 'users/registration/new_access_code.html'
    form_class = NewAccessCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отправка нового access_code'
        return context

    def form_valid(self, form):
        form_user = form.cleaned_data['username']
        db_user = User.objects.filter(phone=form_user)
        if db_user:
            db_user = db_user[0]
            generate_access_code(self, db_user=db_user, message='Your code: ')
            return redirect('users:NewAccessCodeForPasswordPhone')
        else:
            return redirect('users:user_doesnt_exist')


class NewAccessCodeForPasswordPhone(FormView):
    """ Отправка нового access_code для нового пароля """
    model = User
    template_name = 'users/registration/new_access_code.html'
    form_class = NewAccessCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отправка нового access_code'
        return context

    def form_valid(self, form):
        form_user = form.cleaned_data['username']
        db_user = User.objects.filter(phone=form_user)
        if db_user:
            db_user = db_user[0]
            generate_access_code(self, db_user=db_user, message='Your code: ')
            return redirect('users:check_access_for_password')
        else:
            return redirect('users:user_doesnt_exist')


class AccessCodeFailed(TemplateView):
    """Сообщения - неправильный AccessCode"""
    template_name = 'users/access_code_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Неправильный код доступа'
        return context


class UserDoesntExist(TemplateView):
    """Сообщения - Такого пользователя не существует"""
    template_name = 'users/user_doesnt-exist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Такого пользователя не существует'
        return context


class CheckAccessCodeForPassword(FormView):
    """ Проверка access_code для нового пароля """
    model = User
    template_name = 'users/registration/access_code.html'
    form_class = UserCodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение access_code'
        return context

    def form_valid(self, form):
        form_user = form.cleaned_data['username']
        form_access_code = form.cleaned_data['access_code']
        db_user = User.objects.filter(phone=form_user)
        if db_user:
            db_user = db_user[0]
            if form_access_code == db_user.access_code:
                new_password = get_random_string(length=12)
                db_user.set_password(new_password)
                db_user.access_code = None
                db_user.save()
                Site.objects.clear_cache()
                # Отправка кода на телефон
                format_phone = str(db_user.phone)[1:]
                int_phone = int(format_phone)
                data = send_sms(phone=int_phone, message=f'Ваш новый пароль: {new_password}')
                pprint(data)
                return redirect('users:login')
            else:
                return redirect('users:access_code_failed')
        else:
            return redirect('users:user_doesnt_exist')


def generate_access_code(queryset, db_user, message):
    """ Функционал для генерации кода и его отправки """
    access_code = random.randrange(1000, 9999)
    db_user.access_code = access_code
    db_user.save()
    Site.objects.clear_cache()

    # Отправка кода на телефон
    format_phone = str(db_user.phone)[1:]
    int_phone = int(format_phone)
    message = f'{message}{db_user.access_code}'
    send_sms(phone=int_phone, message=message)
    return db_user


def send_sms(phone: int, message: str) -> dict:
    """
    Функция отправки смс через сервис SmsAero.
    Send sms and return results.
            Parameters:
                    phone (int): Phone number
                    message (str): Message to send
            Returns:
                    data (dict): API request result
    """
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    res = api.send(phone, message)
    assert res.get('success'), res.get('message')
    return res.get('data')


# Payment -----------------------------------------------------------------------------------------------------------


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """ Создаем платеж """
    model = Payment
    template_name = 'users/subscription.html'
    form_class = SubscriptionCreateForm
    success_url = reverse_lazy('users:subscription')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создаем платеж'
        context['req_user'] = self.request.user
        vv = Payment.objects.filter(user=self.request.user)
        context['subscr'] = vv
        context['qwertyop'] = 'rrrrr'
        return context

    def form_valid(self, form):
        user = self.request.user
        if Payment.objects.filter(user=user):
            return HttpResponse("Под вашим аккаунтом уже создан платеж, посмотрите, посмотрите, активный ли он")
        else:
            payment = form.save(commit=False)
            form_payment_amount = form.cleaned_data['payment_amount']
            payment.payment_amount = int(form_payment_amount) * 100
            stripe.api_key = settings.STRIPE_SECRET_KEY
            payment.user = user
            # print(payment.user)
            payment.is_paid = False
            payment.session = get_session(payment).id
            payment.save()
            user.payment_pk = payment.id
            user.save()
            # print(user.payment_pk)
            return redirect(f'users:payment-retrieve', payment.pk)

    def get_object(self, queryset=None):
        print(self.request.user)
        return self.request.user


class PaymentRetrieveView(LoginRequiredMixin, ListView):
    """ Получаем ссылку на оплату Payment"""
    model = Payment
    queryset = Payment.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создаем платеж '
        context['req_user'] = self.request.user
        context['qwerty'] = 'final'
        return context

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        session = retrieve_session(self.obj.session)
        if session.payment_status == 'paid' and session.status == 'complete':
            self.obj.is_paid = True
            self.obj.save()
            self.request.user.subscription = True
            self.request.user.save()
        stripe_url = session["url"]
        content = {'stripe_url': stripe_url}
        return render(request, 'users/payment_url.html', content)

    def get_object(self, queryset=None):
        return self.request.user


class PaymentListView(generics.ListAPIView):
    """ Получаем список Payment"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filterset_fields = ('course', 'lesson', 'payment_type')
    # сортировка по дате оплаты
    ordering_fields = ('date_of_payment',)


class PaymentSuccessView(LoginRequiredMixin, ListView):
    """ Проверка """
    model = Payment
    context_object_name = 'payment_list'
    queryset = Payment.objects.all()

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        session = retrieve_session(self.obj.session)
        if session.payment_status == 'paid' and session.status == 'complete':
            self.obj.is_paid = True
            self.obj.save()
            self.request.user.subscription = True
            self.request.user.save()
        stripe_url = session["url"]
        content = {'stripe_url': stripe_url}
        return render(request, 'users/payment_url.html', content)

    def get_object(self, queryset=None):
        return self.request.user
