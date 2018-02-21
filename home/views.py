from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RoomPostForm
from .models import Room, RoomImage

def index(request):
    latest_posts_list = Room.objects.order_by('-last_updated')[:4]
    return render(request, 'home/index.html', {'latest_posts_list': latest_posts_list,})

def browse_rooms(request):
    rooms_list = Room.objects.all()
    paginator = Paginator(rooms_list, 2)
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        pasts = paginator.page(paginator.num_pages)
    return render(request, 'home/browse.html', {'page': page, 'rooms': rooms})

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    roomImages = list(room.roomimage_set.all())
    return render(request, 'home/detail.html', {'room': room, 'roomImages': roomImages})

def search(request):
    result_list = []
    query_set = request.GET
    if 'q' in query_set:
        print('Search request: {}'.format(request.GET['q']))

        # check all Room variables in order of importance >>
        ##  property_name > host_name > address > description
        for room in Room.objects.all():
            if query_set['q'].lower() in room.property_name.lower():
                result_list.append(room)
        for room in Room.objects.all():
            if query_set['q'].lower() in room.host_name.lower() and room not in result_list:
                result_list.append(room)
        for room in Room.objects.all():
            if query_set['q'].lower() in room.address.lower() and room not in result_list:
                result_list.append(room)
        for room in Room.objects.all():
            if query_set['q'].lower() in room.description.lower() and room not in result_list:
                result_list.append(room)

    if 'filer' in query_set:
        print(query_set['filter'])
    else: print("No request")

    return render(request, 'home/search.html', {'rooms': result_list})

def create(request):
    if request.method == 'POST':
        print(request.POST['address']) # we can pull and manipulate each attribute given in the POST using 'request.POST['name_of_field_in_html']'
        form = RoomPostForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES.getlist('images')) > 4 or len(request.FILES.getlist('images')) == 0:
                form = RoomPostForm()
                return render(request, 'home/create.html', {'form': form})

            new_room = form.save()
            for i in request.FILES.getlist('images'):
                image = RoomImage(room=new_room, image=i)
                image.save()
            return HttpResponseRedirect(reverse(detail, args=(new_room.pk,)))
    else:
        form = RoomPostForm()
    return render(request, 'home/create.html', {'form': form})
