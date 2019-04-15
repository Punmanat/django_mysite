from django.urls import path
from polls import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('details/<int:poll_id>', views.details, name="detail"),
    path('createpoll/', views.create, name="create"),

]