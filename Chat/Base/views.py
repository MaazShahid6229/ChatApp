from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Password Doesn't Match")

    context = {}
    return render(request, "login.html", context)


def logoutuser(request):
    logout(request)
    return redirect("home")


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else  ""
    topic = Topic.objects.all()
    rooms = Room.objects.filter(topic__name__contains = q)
    room_count = rooms.count()
    context = {"rooms": rooms, "topic": topic, "room_count": room_count}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "room.html", context)


def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)


def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "room_form.html", context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"room": room}
    return render(request, "delete_form.html", context)
