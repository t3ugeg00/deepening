from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def register(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, 'Account created! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(req, 'registration/register.html', {'form': form})

@login_required
def account(req):
    """View and update account information"""
    if req.method == 'POST':
        # Update user info
        req.user.email = req.POST.get('email', req.user.email)
        req.user.first_name = req.POST.get('first_name', req.user.first_name)
        req.user.last_name = req.POST.get('last_name', req.user.last_name)
        req.user.save()
        messages.success(req, 'Your account has been updated!')
        return redirect('account')
    
    return render(req, 'user/account.html')

@login_required
def profile(req):
    """Profile page - could combine with account or keep separate"""
    return render(req, 'user/profile.html', {
        'user': req.user,
        'date_joined': req.user.date_joined,
        'last_login': req.user.last_login
    })

@login_required
def change_password(req):
    """Change password view"""
    if req.method == 'POST':
        form = PasswordChangeForm(req.user, req.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(req, user)  # Keep user logged in
            messages.success(req, 'Your password has been changed!')
            return redirect('account')
    else:
        form = PasswordChangeForm(req.user)
    
    return render(req, 'user/change_password.html', {'form': form})