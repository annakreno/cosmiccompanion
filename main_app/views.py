import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, CelestialObject, Photo
from .forms import EventForm
from .forms import CelestialObjectForm

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
    
class EventCreate(LoginRequiredMixin, CreateView):
  model = Event
  form_class = EventForm
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
  
class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        event = form.save(commit=False)
        if event.user !=self.request.user:
            return redirect("/events/")
        return super().form_valid(form)
    
    # def dispatch(self, request, *args, **kwargs):
    #     event = self.get_object()
    #     if event.user != self.request.user:
    #         return redirect("/events/")
    #     return super().dispatch(request, *args, **kwargs)

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

class CelestialObjectList(ListView):
    model = CelestialObject

class CelestialObjectDetail(DetailView):
    model = CelestialObject
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        celestial_object = self.object
        events = celestial_object.event_set.all()
        context['events'] = events
        return context

class CelestialObjectCreate(LoginRequiredMixin, CreateView):
    model = CelestialObject
    form_class = CelestialObjectForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CelestialObjectUpdate(LoginRequiredMixin, UpdateView):
    model = CelestialObject
    form_class = CelestialObjectForm
    def form_valid(self, form):
        celestialobject = form.save(commit=False)
        if celestialobject.user !=self.request.user:
            return redirect("/celestialevents/")
        return super().form_valid(form)

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

def add_photo(request, event_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, event_id=event_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('events_detail', event_id=event_id)