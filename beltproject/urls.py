from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('travels', views.trip_dash),
    path('addtrip', views.add_new),
    path('create', views.create_trip),
    path('travels/<int:trip_id>/join', views.join),
    path('travels/<int:trip_id>/delete', views.delete),
    path('travels/<int:trip_id>/cancel', views.cancel),
    path('view/<int:trip_id>', views.show_one),
    path('logout', views.logout),
]
