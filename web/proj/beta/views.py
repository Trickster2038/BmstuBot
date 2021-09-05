from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return HttpResponse('Hello World! \
        <br/><a href="test">Test</a>')

def test(request):
    return render(request, "beta/test.html")

# Create your views here.
