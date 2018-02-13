from django.shortcuts import render
from django.http import Http404

from .models import Room

def index(request):
    latest_posts_list = Room.objects.order_by('-last_updated')[:5]
    return render(request, 'home/index.html', {'latest_posts_list': latest_posts_list})
