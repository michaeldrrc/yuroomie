from django.db import models

# ToDo: each for inherits information from the creators account
# i.e. hose_name, host_major

class Room(models.Model):
    """model for each room listing"""
    # add roommate preferences in the future
    host_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    property_name = models.CharField(max_length=30, default="")
    description = models.TextField(default="No Description")
    cost = models.PositiveIntegerField(default=0)
    visits = models.PositiveIntegerField(default=0)
    number_of_rooms = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.property_name

class RoomImage(models.Model):
    """child model of room model (many to one relationship)"""
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField()