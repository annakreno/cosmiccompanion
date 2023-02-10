from django.shortcuts import render

# Create your views here.
def home(request):
    print('party time')
    return render(request, 'home.html')

def events_index(request):
    return render(request, 'events/index.html')

