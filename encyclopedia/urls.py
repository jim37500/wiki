from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("add/", views.add_newpage, name="add"),
    path("random/", views.random_page, name="random"),
    path("<str:entry>/", views.pages, name="pages"),
    path("<str:entry>/edit/", views.edit_page, name="edit"),
]
