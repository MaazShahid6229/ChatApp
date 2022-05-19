from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm

# rooms = [
#     {"id": 1, "Name": "Maaz"},
#     {"id": 2, "Name": "Ali"},
#     {"id": 3, "Name": "Ahmed"},
#     {"id": 4, "Name": "Subhan"},
# ]


# Create your views here.
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
