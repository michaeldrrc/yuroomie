from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('browse/', views.browse_rooms, name='browse'),
    path('r/<int:room_id>/', views.detail, name='detail'),
    path('r/create', views.create, name='create'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
