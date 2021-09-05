from beta.models import Friendship
from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return HttpResponse('Hello World! \
        <br/><a href="test">Test</a>\
        <br/><a href="friends">Friends</a>')

def test(request):
    return render(request, "beta/test.html")

def friends(request):
    friendships = Friendship.objects.all()
    data = {"friends": friendships}
    print(friendships)
    print(len(friendships))
    for x in friendships:
        print(x)
    for p in Friendship.objects.raw('SELECT * FROM friends'):
        print(p)
    return render(request, "beta/friends.html", context=data)

# Create your views here.
