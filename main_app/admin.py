from django.contrib import admin
from .models import Event, CelestialObject, Photo

# Register your models here.
admin.site.register(Event)
admin.site.register(CelestialObject)
admin.site.register(Photo)
