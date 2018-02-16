from django.contrib import admin

from .models import Room, RoomImage

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['property_name', 'address', 'host_name', 'cost']

admin.site.register(RoomImage)