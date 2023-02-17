import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, CelestialObject, Photo
from .forms import EventForm
from .forms import CelestialObjectForm
from .forms import DateRangeForm
import requests
from datetime import datetime
import pytz


# Create your views here.
def apod(request):
    api_key = 'JEY9zPlHaKd05eOsx447DLTJu2n51dv8TMBNZc4a'
    pacific_tz = pytz.timezone('US/Pacific')
    # today = '2023-02-09'
    today = datetime.now(pacific_tz).date()
    url = f'https://api.nasa.gov/planetary/apod?date={today}&api_key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        context = {
            'title': data['title'],
            'date': data['date'],
            'explanation': data['explanation'],
            'image_url': data['hdurl'],
        }
        print("!!!!!!!!!!!!", context)
        return render(request, 'home.html', context)
        
    else:
        return render(request, 'error.html', {'error': 'Failed to retrieve APOD.'})


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') 


def events_index(request):
    events = Event.objects.all()
    form = DateRangeForm(request.GET)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        events = events.filter(date__range=(start_date, end_date))
    return render(request, 'events/index.html', { 'events': events, 'form': form })

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


@login_required
def remove_photo(request, event_id, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if photo.event.user != request.user:
        return HttpResponseForbidden("You do not have permission to delete this photo.")
    s3 = boto3.client('s3')
    key = photo.url.split("/")[-1]
    bucket = os.environ['S3_BUCKET']
    s3.delete_object(Bucket=bucket, Key=key)
    photo.delete()
    event = Event.objects.get(id=event_id)
    return redirect('events_detail', event_id=photo.event.id)