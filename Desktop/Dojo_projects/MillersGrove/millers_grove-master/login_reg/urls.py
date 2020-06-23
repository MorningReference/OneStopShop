from django.urls import path
from . import views

urlpatterns = [
    path("user/logout", views.logout),
    path("user/success", views.success),
    path("user/login", views.user_login),
    path("user/create", views.create_user),
    path("user/new", views.new_user),
    path("", views.index)
]
