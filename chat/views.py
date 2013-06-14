#from socketio import socketio_manage

#from django.http import HttpResponse
#from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

from chat.models import ChatRoom
#from chat.sockets import ChatNameSpace


def rooms(request, template="rooms.html"):
    """
    Homepage - lists all rooms
    """
    context = {"rooms": ChatRoom.objects.all()}
    return render(request, template, context)


def room(request, slug, template="room.html"):
    """
    Show a room
    """
    #context = {"room": get_object_or_404(ChatRoom, slug=slug)}

    if not request.session.get("has_session"):
        request.session["has_session"] = True

    room = request.session.session_key
    context = {"room": room}
    return render(request, template, context)


def create(request):
    name = request.POST.get("name")
    if name:
        room, created = ChatRoom.objects.get_or_create(name=name)
        return redirect(room)
    return redirect(room)
