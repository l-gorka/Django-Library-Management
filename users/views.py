from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import views as auth_views

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are already registered')
        return redirect('library:book-list')
    else:
        if request.method == 'POST':
            print('v')
            form = RegisterForm(request.POST)
            if form.is_valid():
                print('v')
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Added new account for {username}.')
                return redirect('library:book-list')
        else:
            print('e')
            form = RegisterForm()
            
        return render(request, 'register.html', {'form': form})

class Login(auth_views.LoginView):
    template_name = 'login.html'
    
    def form_valid(self, form):
        messages.success(self.request, f"Logged in")
        return super().form_valid(form)


