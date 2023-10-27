from django.shortcuts import render
from django.urls import path

from subs.views import base
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    # subs
    path('base/', base),

]