from django.urls import path, include
from polls import views
urlpatterns = [
    path('login/', views.my_login, name="login"),
    path('logout/', views.my_logout, name="logout"),
    path('index/', views.index, name="index"),
    path('details/<int:poll_id>', views.details, name="detail"),
    path('createpoll/', views.create, name="create"),
    path('createcomment/', views.comment, name="comment"),
    path('changepass/', views.changepass, name="changepass"),
    path('register/', views.register, name="register"),
    path('update/<int:poll_id>', views.update, name="update"),
    path('delete/<int:question_id>', views.delete_question, name="delete"),
    path('<int:question_id>/add_choice/', views.add_choice, name="add_choice"),
    path('api/<int:question_id>/add_choice/', views.add_choice_api, name="add_choice_api"),

]
