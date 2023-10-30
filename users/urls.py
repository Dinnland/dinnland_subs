from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ### path('cabinet/', ProfileView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),

    path('delete-user/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),

    ### path('done-generate-new-password/', UserForgotPasswordView.as_view(), name='done_generate_new_password'),

    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    ### path('profile/', ProfileView.as_view(), name='profile'),

    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('users-list/', UsersListView.as_view(), name='users_list'),
    path('users-off/<int:pk>', UserStatusUpdateView.as_view(), name='users_off')

]
