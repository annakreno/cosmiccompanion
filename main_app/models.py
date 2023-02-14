from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class CelestialObject(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=5000)
    last_appearance = models.DateTimeField()
    discovered_by = models.CharField(max_length=250)
    age = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('celestial_objects_detail', kwargs={'pk': self.id})


class Event(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateTimeField()
    description = models.TextField(max_length=5000)
    celestial_objects = models.ManyToManyField(CelestialObject)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('events_detail', kwargs={'event_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=250)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for event_id: {self.event_id} @{self.url}"

    

