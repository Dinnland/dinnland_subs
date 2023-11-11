from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('cabinet/', ProfileView.as_view(), name='profile'),
    path('email-register/', EmailRegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('email-password-reset/', UserForgotPasswordEmailView.as_view(), name='password_reset'),
    path('delete-user/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('done-generate-new-password/', DoneGenerateNewPassword.as_view(), name='done_generate_new_password/'),
    # path('done-generate-new-password/', UserForgotPasswordEmailView.as_view(), name='done_generate_new_password/'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('users-list/', UsersListView.as_view(), name='users_list'),
    # path('users-off/<int:pk>', UserStatusUpdateView.as_view(), name='users_off')
    path('access-code-failed/', AccessCodeFailed.as_view(), name='access_code_failed'),
    path('user-doesnt-exist/', UserDoesntExist.as_view(), name='user_doesnt_exist'),
    path('phone-register/', PhoneRegisterView.as_view(), name='phone_register'),
    path('access-code/', PhoneCodeView.as_view(template_name='users/registration/access_code.html'),
         name='access-code'),
    path('send-access-code/', SendAccessCodeView.as_view(), name='send-access-code'),

    path('make-access-for-password/', NewAccessCodeForPasswordPhone.as_view(), name='make_access_for_password'),
    path('check-access-for-password/', CheckAccessCodeForPassword.as_view(),
         name='check_access_for_password'),
    path('payment/list/', PaymentListView.as_view(), name='payment-list'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payment/<int:pk>/retrieve/', PaymentRetrieveView.as_view(), name='payment-retrieve'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payment_create/', PaymentCreateView.as_view(), name='payment-create'),
    path('success/<int:pk>/', PaymentRetrieveView.as_view(), name='stripe-success'),
    path('success/', RedirectView.as_view(pattern_name='users:payment-create'), name='register'),
    # path('success/', RedirectView),

]
