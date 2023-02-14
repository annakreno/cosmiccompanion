# from django import forms
# from .models import CelestialObject, Event


# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['name', 'date', 'description', 'celestialobjects']
#     def __init__(self, *args, **kwargs): 
#       super().__init__(*args, **kwargs) 
#       c_objects = CelestialObject.objects.all()
#       choices = [(c_object.id, c_object.name) for c_object in c_objects] 
#       self.fields['celestialobjects'].widget = forms.Select(choices=choices)
