from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User

# لیست کاربران
class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

# جزئیات یک کاربر
class UserDetailView(DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'

# ایجاد کاربر
class UserCreateView(CreateView):
    model = User
    fields = '__all__'
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

# ویرایش کاربر
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')

# حذف کاربر
class UserDeleteView(DeleteView):
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

