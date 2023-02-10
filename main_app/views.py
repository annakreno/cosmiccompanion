from django.shortcuts import render

# Create your views here.
def home(request):
    print("TESTING")
    return render(request, 'home.html')

def events_index(request):
    return render(request, 'events/index.html')

