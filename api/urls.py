from .views.user import UserListView, UserView, UserCreateView 
from django.urls import path

urlpatterns = [
    path('create-user/', UserCreateView.as_view(), name="create-user" ),
    path('list-users/',UserListView.as_view(), name="list-users"),
    path('user/<int:pk>',UserView.as_view(), name = "user")
]


