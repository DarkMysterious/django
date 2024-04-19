from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_book", views.add_book, name="add_book"),
    path("delete_book/<str:ISBN>", views.delete_book, name="delete_book"),
    path("delete_users_data", views.delete_users_data, name="delete_users_data"),
]

