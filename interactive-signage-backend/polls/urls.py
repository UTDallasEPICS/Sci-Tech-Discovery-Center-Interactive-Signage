from django.urls import path

from . import views

urlpatterns = [
    path("showinfo/", views.showinfo, name="showinfo"),
    path("receive-id/", views.receive_den_id, name="receive_den_id"),
    path("resetinfo/", views.restartflag, name="restartflag"),
    path("receive-button/", views.receive_button, name="receive_button"),
]