"""Analytics REST API URL Configuration"""
from django.urls import path

from .api import rest

app_name = "analytics"

urlpatterns = [
    path("<slug:model>/", rest.analytics),
]
