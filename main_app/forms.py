from django import forms
from django.forms import ModelForm, Select
from .models import CelestialObject, Event


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, celestialobject):
        return '%s' % celestialobject.name
    
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'description', 'celestialobjects']
    
    name = forms.CharField()
    date = forms.DateInput()
    description = forms.CharField()
    celestialobjects = CustomMMCF(
        queryset=CelestialObject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
