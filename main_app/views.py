from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') 

def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', { 'events': events })

def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', { 'event': event })
    


class EventCreate(CreateView):
  model = Event
  fields = ['name', 'date', 'description']
#   success_url = '/events/{event_id}'

class EventUpdate(UpdateView):
    model = Event
    fields = ['name', 'date', 'description']

class EventDelete(DeleteView):
    model = Event
    success_url = '/events/'

