from beta.models import Friendship, People
from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return HttpResponse('Hello World! \
        <br/><a href="test">Test</a>\
        <br/><a href="friends">Friends</a>')

def test(request):
    return render(request, "beta/test.html")

def friends(request):
    # friendships = Friendship.objects.all()
    # data = {"friends": friendships}
    # print(friendships)
    # print(len(friendships))
    # for x in friendships:
    #     print(x)
    # for p in Friendship.objects.raw('SELECT * FROM friends'):
    #     print("id:" + str(p.id))
    #     # print("id:" + str(p.id2))
    #     print("user1:" + str(p.user1))
    #     print("user2:" + str(p.user2))
    for p in People.objects.raw('SELECT id, surname FROM users'):
        print("id:" + str(p.id))
        # print("id:" + str(p.id2))
        print("surname:" + str(p.surname))
    p = People.objects.raw('SELECT id, surname FROM users')
    friends = []
    for x in p:
        friends.append(str(x.surname[0]))
    data = {"friends": friends}
    # print(data)
    # data = {}
    return render(request, "beta/friends.html", context=data)

# Create your views here.
