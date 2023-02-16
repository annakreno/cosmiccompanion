from django.urls import path
from . import views
from .views import apod
from django.urls import path

urlpatterns = [
    path('', views.apod, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.events_index, name='events_index'),
    path('events/<int:event_id>/', views.events_detail, name='events_detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('events/<int:event_id>/add_photo/', views.add_photo, name='add_photo'),
    path('events/<int:event_id>/remove_photo/<int:photo_id>/', views.remove_photo, name='remove_photo'),
    path('events/<int:event_id>/assoc_event/<int:celestialobject_id>', views.assoc_celestialobject, name='assoc_celestialobject'),
    path('events/<int:event_id>/disassoc_event/<int:celestialobject_id>', views.disassoc_celestialobject, name='disassoc_celestialobject'),
    path('celestialobjects/', views.CelestialObjectList.as_view(), name='celestial_objects_index'),
    path('celestialobjects/<int:pk>/', views.CelestialObjectDetail.as_view(), name='celestial_objects_detail'),
    path('celestialobjects/create/', views.CelestialObjectCreate.as_view(), name='celestial_objects_create'),
    path('celestialobjects/<int:pk>/update/', views.CelestialObjectUpdate.as_view(), name='celestial_objects_update'),
    path('celestialobjects/<int:pk>/delete', views.CelestialObjectDelete.as_view(), name='celestial_objects_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('apod/', apod, name='apod'),
    
]
