from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm


class RegisterView(View):
    def get(self, request):
        create_form = CreateUserForm()
        context = {'form': create_form}
        return render(request, 'register.html', context=context)

    def post(self, request):
        create_form = CreateUserForm(data=request.POST, files=request.FILES)
        if create_form.is_valid():
            create_form.save()
            return redirect('login')
        else:
            return render(request, 'register.html', context={'form': create_form})


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        context = {'form': login_form}
        return render(request, 'login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('landing-page')
        else:
            context = {'form': login_form}
            return render(request, 'login.html', context=context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ProfileView(View):
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        return render(request, 'profile.html', {'user': user})


class ProfileUpdateView(View):
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        return render(request, 'profile_update.html', {'user': user})

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.pk)
        return render(request, 'profile_update.html', {'user': user, 'form': form})


