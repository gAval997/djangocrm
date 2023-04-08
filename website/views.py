from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
def home(request):
  # Check if user is logging in
  if request.method == 'POST':
    # Extract data from form
    username = request.POST['username']
    password = request.POST['password']
    
    # Authenticate
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user=user)
      return redirect('home')
    else:
      messages.error(request, 'Wrong credentials, please try again.')
      return redirect('home')

  return render(request, 'home.html', {})


def logout_user(request):
  logout(request)
  messages.success(request, 'You have logged out.')
  return redirect('home')


def register_user(request):
  if (request.method == 'POST'):
    signup_form = SignUpForm(request.POST)
    if (signup_form.is_valid()):
      signup_form.save()
      
      # Authenticate and login
      username = signup_form.cleaned_data['username']
      password = signup_form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user=user)
      messages.success(request, 'You have successfully registered!')
      return redirect('home')
    else:
      # This return is necessary to show form errors
      return render(request, 'register.html', { 'signup_form': signup_form })

  # This is used in a GET request and the form hasn't been previously submitted
  signup_form = SignUpForm()
  return render(request, 'register.html', { 'signup_form': signup_form })
