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
      self.fields['celestial_objects'].widget = forms.SelectMultiple(choices=choices)
      
      
class CelestialObjectForm(forms.ModelForm):
    class Meta:
        model = CelestialObject
        fields = ['name', 'description', 'last_appearance', 'discovered_by', 'age']
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
    #   events1 = Event.objects.all()
    #   choices = [(event.id, event.name) for event in events1]
    #   self.fields['events'].widget = forms.SelectMultiple(choices=choices)


class DateRangeForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()
