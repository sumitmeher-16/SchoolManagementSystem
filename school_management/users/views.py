from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q

from .models import User
from .forms import UserForm, UserUpdateForm


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    roles = request.GET.get('role')
    search = request.GET.get('search')
    
    if roles:
        users = users.filter(role=roles)
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    context = {
        'users': users,
        'roles': roles,
        'search': search,
    }
    return render(request, 'users/user_list.html', context)


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.get_full_name() or user.username} created successfully!')
            return redirect('users:user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Create'})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.get_full_name() or user.username} updated successfully!')
            return redirect('users:user_list')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Update', 'user_obj': user})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})


@login_required
@user_passes_test(lambda u: u.is_admin_user)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user_obj': user})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})


def check_username(request):
    username = request.GET.get('username')
    if User.objects.filter(username=username).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})
