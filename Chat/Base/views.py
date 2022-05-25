from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic, Message


# Create your views here.
def loginUser(request):
    page = "login"
    if request.user.is_authenticated:
        return HttpResponse(f"You are already Logged in with user {request.user}")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            context = {"page": page}
            return render(request, "login.html", context)

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
    room_messages = Message.objects.all()
    context = {"rooms": rooms, "topic": topic, "room_count": room_count, "room_messages": room_messages}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=Room.objects.get(id=pk),
            body=request.POST.get("body")
        )
        room.participants.add(request.user)
        redirect("room", pk)
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "room.html", context)


@login_required(login_url="login")
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room1 = form.save(commit=False)
            print(room1.host)
            room1.host = request.user
            room1.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)


@login_required(login_url="login")
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


@login_required(login_url="login")
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"room": room}
    return render(request, "delete_form.html", context)


@login_required(login_url="login")
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete this Message")

    if request.method == "POST":
        message.delete()
        return redirect("home")
    context = {"obj": message}
    return render(request, "delet_message.html", context)
