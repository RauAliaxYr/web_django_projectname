from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, EventEditForm, EventDeleteForm
from .models import Profile, Event

from django.contrib.auth.decorators import login_required


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'projectname/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def dashboard(request):

    return render(request, 'projectname/dashboard.html', {'section': 'dashboard'})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
        if user is not None:
            if user.is_active:
                login(request, user)  # сохраняет текущего пользователя в сессии
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])

            # Создание профиля пользователя.

            # Сохраняем пользователя в базе данных.
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'projectname/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'projectname/register.html', {'user_form': user_form})


def edit_event(request):
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.location = "достать из гугмапс"
            new_event.save()
            Event.objects.create(new_event)
            print("мы отработаели")
            return render(request, 'projectname/event_creation_done.html', {'new_event': new_event})
        else:
            HttpResponse('Authenticated successfully')
    else:
        form = EventEditForm()
    return render(request, 'projectname/edit_event.html', {'event_edit': form})


def delete_event(request):
    if request.method == 'POST':
        form = EventDeleteForm(request.POST)
        if form.is_valid():
            form = form
    else:
        form = EventDeleteForm()
    return render(request, 'projectname/delete_events.html', {'event_delete': form})
