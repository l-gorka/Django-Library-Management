from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.mail import send_mail

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        messages.warning(request, f'You are already registered')
        return redirect('library:book-list')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                email = request.POST.get('email')
                username = form.cleaned_data.get('username')
                messages.success(request, f'Added new account for {username}.')
                '''
                send_mail(
                    'Library Management',
                    'Account has been created',
                    'lms@example.com',
                    [email],
                    fail_silently=False,
                )'''
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

class PasswordChange(LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'password-change.html'
    success_url = reverse_lazy('user-account')

    def form_valid(self, form):
        messages.success(self.request, f"Password changed")
        return super().form_valid(form)



def user_account(request):
    if not request.user.is_authenticated:
        messages.warning(request, f'You must be logged in to view your profile.')
        return redirect('login')
    context = dict()
    user = User.objects.get(username=request.user.username)
    context['user'] = user
    return render(request, 'user-account.html', context)