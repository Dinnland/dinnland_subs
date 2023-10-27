from django.urls import path

from subs.apps import SubsConfig
from subs.views import base

app_name = SubsConfig.name

urlpatterns = [
    # subs
    path('base/', base),

]