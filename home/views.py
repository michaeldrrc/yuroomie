from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RoomPostForm
from .models import Room, RoomImage
from django.contrib.auth.decorators import login_required

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
<<<<<<< HEAD
        page = paginator.page(paginator.num_pages)
    return render(request, 'home/browse.html', {'page': page,
                                                'rooms': rooms})
=======
        pasts = paginator.page(paginator.num_pages)
    return render(request, 'home/browse.html', {'page': page, 'rooms': rooms})
>>>>>>> 98a24a2ba1b272c97c6ca404b479b728ef927264

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

@login_required()
def create(request):
    if request.method == 'POST':
        form = RoomPostForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            # if the user added more than 4 (to be changed to 6) or no images, return the form again
            if len(request.FILES.getlist('images')) > 4 or len(request.FILES.getlist('images')) == 0:
                return render(request, 'home/create.html', {'form': form})
            
            new_room = form.save(commit=False)
            new_room.host_name = (request.user.first_name + ' ' + request.user.last_name[:1])
            # concatenate all form address inputs into one consistentLy formatted address
            address = (request.POST['address1'] + ', ')
            address += (request.POST['city'] + ', ON, ' + request.POST['postalCode'])
            new_room.address = address
            new_room.creator_id = request.user.pk
            new_room.save()
            # for each image uploaded, save it with it's parent room being the room we just created
            for i in request.FILES.getlist('images'):
                image = RoomImage(room=new_room, image=i)
                image.save()
            return HttpResponseRedirect(reverse(detail, args=(new_room.pk,)))
        else:
            print('invalid')
    else:
        form = RoomPostForm()
    return render(request, 'home/create.html', {'form': form})
