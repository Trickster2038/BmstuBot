from beta.models import Friendship, People
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction
 
def index(request):
    return HttpResponse('Hello World! \
        <br/><a href="test">Test</a>\
        <br/><a href="friends">Friends</a>')

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

# Create your views here.
