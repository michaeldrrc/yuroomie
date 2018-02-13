from django.db import models

class Room(models.Model):
    # add roommate preferences in the future
    host_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    property_name = models.CharField(max_length=30, default="")
    description = models.TextField(default="")
    cost = models.DecimalField(max_digits=7, decimal_places=2) # change to PositiveIntegerField
    number_of_rooms = models.PositiveSmallIntegerField()
    last_updated = models.DateTimeField('last updated')

    def __str__(self):
        return self.property_name
