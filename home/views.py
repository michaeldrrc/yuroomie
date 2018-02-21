from django.shortcuts import get_object_or_404, render
from django.db.models import Q
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
    result_list = Room.objects.all()
    query_dict = request.GET
    context = {}
    if 'q' in query_dict:
        query_q = context['query'] = query_dict['q']
        print('Search request: {}'.format(query_q))

        result_list = result_list.filter(
            Q(property_name__icontains=query_q) |
            Q(host_name__icontains=query_q) |
            Q(address__icontains=query_q) |
            Q(description__icontains=query_q)
        )
            
    else: print("No query request")

    if 'filter' in query_dict:
        filters = context['filters'] = query_dict['filter']
        print('Filter request: {}'.format(query_dict['filter']))
        try:
            filter_dict = dict(item.split("=") for item in filters.split("~"))
            if 'prh' in filter_dict:
                context['prh'] = filter_dict['prh']
            else:
                context['prh'] = 99999
            if 'prl' in filter_dict:
                context['prl'] = filter_dict['prl']
            else:
                context['prl'] = 0
            result_list = result_list.filter(cost__gte=context['prl'], cost__lte=context['prh'])
        except ValueError:
            # do not filter, no value for all keys
            filters = None    
    else:
        context['prh'] = 99999
        context['prl'] = 0
        filters = None
        print("No filter request")
    
    context['rooms'] = result_list
    context['num_results'] = len(result_list)

    return render(request, 'home/search.html', context)

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
