from django.shortcuts import render

# Create your views here.
def home(request):
    print('greek freak')
    return render(request, 'home.html')

def events_index(request):
    print('TESTING AGAIN')
    return render(request, 'events/index.html')

