from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from store.models import Customer
from .forms import UserRegistrationForm


def register_view(request):
    # print(request.body)

    # This function renders the registration form page and create a new user based on the form data
    # We use Django's UserCreationForm which is a model created by Django to create a new user.
    # UserCreationForm has three fields by default: username (from the user model), password1, and password2.
    # If you want to include email as well, switch to our own custom form called UserRegistrationForm
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        # check whether it's valid: for example it verifies that password1 and password2 match
        if form.is_valid():
            # if you want to login the user directly after registration, use the following three lines,
            # which logins the user and redirect to index
            user = form.save()
            login(request, user)
            Customer.objects.create(
                user=user,
                name=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
            )
            return redirect('index')
            # if you do want to login the user directly after registration, comment out the three lines above,
            # redirect the user to login page so that after registration the user can enter the credentials
            # form.save()
            # return redirect('login')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    # this function authenticates the user based on username and password
    # AuthenticationForm is a form for logging a user in.

    # Plug the request.post in AuthenticationForm if Post, else an empty instance of Django's AuthenticationForm
    # to generate the necessary html on the template.
    form = AuthenticationForm(data=request.POST or None)

    # if the request method is a post
    if request.method == 'POST':
        # check whether it's valid:
        if form.is_valid():
            # get the user info from the form data and login the user
            user = form.get_user()
            login(request, user)
            # redirect the user to index page
            return redirect('index')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    # This is the method to logout the user
    logout(request)
    # redirect the user to index page after logout
    return redirect('index')
