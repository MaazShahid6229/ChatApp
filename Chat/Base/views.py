from django.shortcuts import render, redirect
from django.http import  HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.
def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return HttpResponse(f"You are already Logged in with user {request.user}")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Password Doesn't Match")

    context = {"page": page}
    return render(request, "login.html", context)


def logoutuser(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "User Can't be created")
    form = UserCreationForm()
    context = {"form": form}
    return render(request, "login.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topic = Topic.objects.all()
    rooms = Room.objects.filter(topic__name__contains=q)
    room_count = rooms.count()
    context = {"rooms": rooms, "topic": topic, "room_count": room_count}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "room.html", context)


@login_required(login_url= "login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)


@login_required(login_url= "login")
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)


@login_required(login_url= "login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"room": room}
    return render(request, "delete_form.html", context)