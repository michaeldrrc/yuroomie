from django.shortcuts import render
from django.http import Http404

from .models import Room

def index(request):
    latest_posts_list = Room.objects.order_by('-last_updated')[:5]
    return render(request, 'home/index.html', {'latest_posts_list': latest_posts_list})

def detail(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        raise Http404("It's not you, it's us. We couldn't find the listing you were looking for")

    return render(request, 'home/detail.html', {'room': room})
