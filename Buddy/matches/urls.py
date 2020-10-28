from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("task_bar", views.task_bar_view, name="task_bar"),
    path("complete_info", views.complete_info_view, name="complete_info"),
    path("user_info/<int:id>", views.user_info_view, name="user_info"),
    path("friend_request", views.friend_request_view, name="friend_request"),
    path("process_request", views.process_request_view, name="process_request"),
    path("delete_friend", views.delete_friend_view, name="delete_friend"),
    path("message", views.message_view, name="message"),
    path("upload_pic", views.upload_pic_view, name="upload_pic"),
]
