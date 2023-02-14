from django import forms
from .models import Event
from .models import CelestialObject


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description', 'celestial_objects']
    def __init__(self, *args, **kwargs): 
      super().__init__(*args, **kwargs) 
      celestialobjects = CelestialObject.objects.all()
      choices = [(celestialobject.id, celestialobject.name) for celestialobject in celestialobjects]
      print(">>>>>", choices)
      self.fields['celestial_objects'].widget = forms.Select(choices=choices)
      
      
