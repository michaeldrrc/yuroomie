import operator
from functools import reduce
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RoomPostForm
from .models import Room, RoomImage
from accounts.models import Profile
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
        page = paginator.page(paginator.num_pages)
    return render(request, 'home/browse.html', {'page': page, 'rooms': rooms})

def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    roomImages = list(room.roomimage_set.all())
    return render(request, 'home/detail.html', {'room': room, 'roomImages': roomImages})

def search(request):
    RESULTS_PER_PAGE = 10

    result_list = Room.objects.order_by('-last_updated')
    query_dict = request.GET
    context = {}
    search = True

    if 'sort' in query_dict:
        sort = context['sort'] = query_dict['sort']
        if sort == 'last':
            pass
        elif sort == 'l2h':
            result_list = result_list.order_by('cost')
        elif sort == 'h2l':
            result_list = result_list.order_by('-cost')
        else:
            sort = 'none'
    else:
        context['sort'] = 'none'

    if 'q' in query_dict and query_dict['q'] is not "":
        query_q = context['query'] = query_dict['q']

        result_list = result_list.filter(
            Q(property_name__icontains=query_q) |
            Q(address__icontains=query_q) |
            Q(description__icontains=query_q)
        )
    else:
        search = False

    if 'filter' in query_dict:
        filters = context['filters'] = query_dict['filter']
        try:
            filter_dict = dict(item.split("=") for item in filters.split("~"))
            #price range high
            if 'prh' in filter_dict:
                context['prh'] = filter_dict['prh']
                result_list = result_list.filter(cost__lte=context['prh'])
            else:
                context['prh'] = '99999'

            #price range low
            if 'prl' in filter_dict:
                context['prl'] = filter_dict['prl']
                result_list = result_list.filter(cost__gte=context['prl'])
            else: context['prl'] = '0'

            ##pre
            context['gen_m'] = 'false'
            context['gen_f'] = 'false'
            context['gen_o'] = 'false'
            context['par_1'] = 'false'
            context['par_2'] = 'false'
            context['par_3'] = 'false'
            context['par_4'] = 'false'
            context['rms_1'] = 'false'
            context['rms_2'] = 'false'
            context['rms_3'] = 'false'
            context['rms_4'] = 'false'
            context['type_a'] = 'false'
            context['type_c'] = 'false'
            context['type_t'] = 'false'
            context['type_h'] = 'false'
            ##
        
            #gender
            if 'gen' in filter_dict:
                context['gen'] = filter_dict['gen']
                s = list(context['gen'])
                for i in s:
                    if i in {'m','f','o'}:
                        context['gen_'+i] = 'true'
                result_list = result_list.filter(reduce(
                    operator.or_,  (Q(creator_gender__iexact=key) for key in s))) 

            #number of garages
            if 'par' in filter_dict:
                context['par'] = filter_dict['par']
                s = list(str(context['par']))
                for i in s:
                    if i in {'1','2','3','4'}:
                        context['par_'+i] = 'true'
                result_list = result_list.filter(reduce(
                    operator.or_,  (Q(garages__iexact=key) for key in s))) 

            #number of rooms
            if 'rms' in filter_dict:
                context['rms'] = filter_dict['rms']
                s = list(context['rms'])
                for i in s:
                    if i in {'1','2','3','4'}:
                        context['rms_'+i] = 'true'
                result_list = result_list.filter(reduce(
                    operator.or_,  (Q(number_of_rooms__iexact=key) for key in s))) 

            #property type
            if 'type' in filter_dict:
                context['type'] = filter_dict['type']
                s = list(context['type'])
                for i in s:
                    if i in {'a','c','t','h'}:
                        context['type_'+i] = 'true'
                result_list = result_list.filter(reduce(
                    operator.or_,  (Q(property_type__iexact=key) for key in s)))           
            
        except ValueError:
            pass  
    else:
        context['prh'] = '99999'
        context['prl'] = '0'
        context['gen_m'] = 'false'
        context['gen_f'] = 'false'
        context['gen_o'] = 'false'
        context['par_1'] = 'false'
        context['par_2'] = 'false'
        context['par_3'] = 'false'
        context['par_4'] = 'false'
        context['rms_1'] = 'false'
        context['rms_2'] = 'false'
        context['rms_3'] = 'false'
        context['rms_4'] = 'false'
        context['type_a'] = 'false'
        context['type_c'] = 'false'
        context['type_t'] = 'false'
        context['type_h'] = 'false'
        filters = None

    paginator = Paginator(result_list, RESULTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context['sf'] = 's' if search == True else ''
    context['sf'] += 'f' if filters is not None else ''
    
    context['rooms'] = rooms
    context['num_results'] = len(result_list)

    return render(request, 'home/search.html', context)

@login_required()
def create(request):
    if request.method == 'POST':
        form = RoomPostForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            # if the user added more than 4 (to be changed to 6) or no images, return the form again
            if len(request.FILES.getlist('images')) > 6 or len(request.FILES.getlist('images')) == 0:
                error_message = "Please enter anywhere between 1 and 6 images"
                return render(request, 'home/create.html', {'form': form, 'error_message': error_message})
            
            new_room = form.save(commit=False)
            new_room.host_name = (request.user.first_name + ' ' + request.user.last_name[:1])
            # concatenate all form address inputs into one consistentLy formatted address
            address = (request.POST['address1'] + ', ')
            address += (request.POST['city'] + ', ON, ' + request.POST['postalCode'])
            new_room.address = address
            new_room.creator_id = request.user.pk
            user = request.user
            profile = Profile.objects.get(user=user)
            new_room.creator_gender = profile.gender
            new_room.creator_major = profile.major
            new_room.creator_year = profile.year
            new_room.creator_email = user.email
            new_room.creator_phone = request.POST['creator_phone']
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
