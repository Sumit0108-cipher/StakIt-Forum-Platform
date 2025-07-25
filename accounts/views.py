
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth import logout

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Or change to 'questions-list' if we add that view
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('signup')
# Create your views here.
