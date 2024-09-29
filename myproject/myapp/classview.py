# classview.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from myapp.forms import UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'member_register_form_decor.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Change 'home' to your desired redirect URL
        return render(request, 'member_register_form_decor.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'member_login_form.html'  # Specify your login template

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')