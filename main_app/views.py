from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, CelestialObject
from .forms import EventForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') 

@login_required
def events_index(request):
    events = Event.objects.filter(user=request.user)
    return render(request, 'events/index.html', { 'events': events })

@login_required
def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/detail.html', { 'event': event })
    


class EventCreate(LoginRequiredMixin, CreateView):
  model = Event
  form_class = EventForm
  template_name = 'main_app/event_form.html'
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['name', 'date', 'description']

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

class CelestialObjectList(LoginRequiredMixin, ListView):
    model = CelestialObject

class CelestialObjectDetail(LoginRequiredMixin, DetailView):
    model = CelestialObject

class CelestialObjectCreate(LoginRequiredMixin, CreateView):
  model = CelestialObject
  fields = '__all__'
#   success_url = '/celestialobjects/'

class CelestialObjectUpdate(LoginRequiredMixin, UpdateView):
    model = CelestialObject
    fields = ['name', 'description', 'last_appearance']

class CelestialObjectDelete(LoginRequiredMixin, DeleteView):
    model = CelestialObject
    success_url = '/celestialobjects/'

@login_required
def assoc_celestialobject(request, event_id, celestialobject_id):
    Event.objects.get(id=event_id).celestialobjects.add(celestialobject_id)
    return redirect('events_detail', event_id=event_id)

@login_required
def disassoc_celestialobject(request, event_id, celestialobject_id):
    Event.objects.get(id=event_id).celestialobjects.remove(celestialobject_id)
    return redirect('events_detail', event_id=event_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)