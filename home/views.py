from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RoomPostForm

from .models import Room

def index(request):
    latest_posts_list = Room.objects.order_by('-last_updated')[:4]
    return render(request, 'home/index.html', {'latest_posts_list': latest_posts_list})

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'home/detail.html', {'room': room})
    
def create(request):
    if request.method == 'POST':
        print(request.POST['address']) # we can pull and manipulate each attribute given in the POST using 'request.POST['name_of_field_in_html']'
        form = RoomPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_room = form.save()
            return HttpResponseRedirect(reverse(detail, args=(new_room.pk,)))
    else:
        form = RoomPostForm()
    return render(request, 'home/create.html', {'form': form})