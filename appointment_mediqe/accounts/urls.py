from django.urls import path
from .views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView


urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/<uuid:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/<uuid:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<uuid:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
