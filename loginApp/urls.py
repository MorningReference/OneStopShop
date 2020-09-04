from django.urls import path
from . import views

urlpatterns = [
    path("login", views.showLogin),
    path('register', views.showRegister),
    path('process/register', views.register),
    path('process/login', views.login),
    path('myaccount/<int:userId>', views.editUser),
    path('myaccount/<int:userId>/<str:updateType>/update', views.updateUser),
    # path('myaccount/<int:userId>/shipping/add', views.addShipping),
    # path('myaccount/<int:userId>/<int:shippingId>/shipping/create', views.createShipping),
    # path('myaccount/<int:userId>/<int:shippingId>/shipping/edit', views.editShipping),
    # path('myaccount/<int:userId>/<int:shippingId>/shipping/update', views.updateShipping),
    # path('myaccount/<int:userId>/<int:shippingId>/shipping/delete', views.deleteShipping),
    # path('myaccount/<int:userId>/payment/add', views.addPayment)
    # path('myaccount/<int:userId>/<int:paymentId>/payment/create', views.createPayment),
    # path('myaccount/<int:userId>/<int:paymentId>/payment/edit', views.editPayment),
    # path('myaccount/<int:userId>/<int:paymentId>/payment/update', views.updatePayment),
    # path('myaccount/<int:userId>/<int:paymentId>/payment/delete', views.deletePayment),
    path('logout', views.logout)
]