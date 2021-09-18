from beta.models import Friendship, People, Person, PersonT, FriendsT
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction
from django.shortcuts import redirect
 
def index(request):
    return HttpResponse('Hello World! \
        <br/><a href="test/">Test</a>\
        <br/><a href="friends/">Friends</a>\
        <br/><a href="login/">Login</a>\
        <br/><a href="profile/">Profile</a>\
        <br/><a href="outgoing/">Outgoing</a>')

def test(request):
    return render(request, "beta/test.html")

def friends(request):
    cursor = connection.cursor()
    cursor.execute("UPDATE users set surname[1]='Козлов3' where surname[1]='Козлов2'")
    transaction.commit()

    for p in People.objects.raw('SELECT id, surname FROM users'):
        print("id:" + str(p.id))
        # print("id:" + str(p.id2))
        print("surname:" + str(p.surname))
    p = People.objects.raw('SELECT id, surname FROM users')
    friends = []
    for x in p:
        friends.append(str(x.surname[0]))
    data = {"friends": friends}

    return render(request, "beta/friends.html", context=data)

def profile(request):
    print("session: " + request.user.username)
    me = PersonT.objects.get(id=request.user.username)
    print(me)
    data = {"person": me}
    return render(request, "beta/profile.html", context=data)

def outgoing(request):
    friends = FriendsT.objects.filter(user1=request.user.username)
    friends_list = []
    for x in friends:
        p = PersonT.objects.get(id=x.user2)
        friends_list.append({"rowdata": p, "path": "path1"})
    data = {"friends": friends_list, "caption": "Outgoing"}
    print(data)
    return render(request, "shortcards.html", context=data)



def asyncview(request):
    print("ajax test")
    return HttpResponse('ajax ok')

# Create your views here.
