from django.db import models

class Room(models.Model):
    """model for each room listing"""
    # add roommate preferences in the future
    host_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    property_name = models.CharField(max_length=30, default="")
    description = models.TextField(default="", blank=True)
    cost = models.PositiveIntegerField(default=0)
    visits = models.PositiveIntegerField(default=0)
    property_type_options = (('a', 'apartment'),
                                ('c', 'condo'),
                                ('t', 'townhouse'),
                                ('h', 'house'))
    property_type = models.CharField(choices=property_type_options, max_length=10)
    number_of_rooms = models.PositiveSmallIntegerField()
    garages = models.PositiveSmallIntegerField()
    creator_id = models.PositiveIntegerField()
    creator_email = models.CharField(max_length=50)
    creator_phone = models.CharField(max_length=10, default="", blank=True)
    creator_gender = models.CharField(max_length=10)
    creator_major = models.CharField(max_length=20)
    creator_year = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property_name

class RoomImage(models.Model):
    """child model of room model (many to one relationship)"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField()