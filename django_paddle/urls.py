from django.urls import path

from django_paddle import views


urlpatterns = [
    path("webhook", views.webhook, name="django_paddle_webhook"),
]
