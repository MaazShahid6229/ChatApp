from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.loginUser, name="login"),
    path("register", views.register, name="register"),
    path("logoutuser", views.logoutuser, name="logoutuser"),

    path("room/<int:pk>/", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<int:pk>", views.update_room, name="update-room"),
    path("delete-room/<int:pk>", views.delete_room, name="delete-room"),
    path("delete-message/<int:pk>", views.delete_message, name="delete_message"),

    path("user_profile/<int:pk>", views.userProfile, name="user_profile"),
    path("update_user/<int:pk>", views.update_user, name="update_user"),

]
