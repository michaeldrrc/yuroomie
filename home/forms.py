from django import forms
from django.forms import ModelForm
from .models import Room

class RoomPostForm(ModelForm):
    """ inherits the Room model and casts as a form """
    class Meta:
        model = Room
        fields = ['property_name', 
                    'description', 
                    'cost', 
                    'number_of_rooms', 
                    'property_type',
                    'garages',]
