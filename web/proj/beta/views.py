from beta.models import Friendship, People, Person
from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection,transaction
from django.shortcuts import redirect
 
def index(request):
    return HttpResponse('Hello World! \
        <br/><a href="test/">Test</a>\
        <br/><a href="friends/">Friends</a>\
        <br/><a href="login/">Login</a>\
        <br/><a href="profile/">Profile</a>')

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
    me = Person.objects.raw('SELECT id,name, surname, department, \
        course, faculty, username, is_moderator, is_curator \
        from users where id = {}'.format(request.user.username))
    me = me[0]
    me.name = me.name[0]
    me.surname = me.surname[0]
    me.username = me.username[0]
    print(me)
    data = {"person": me}
    return render(request, "beta/profile.html", context=data)

def asyncview(request):
    print("ajax test")
    return HttpResponse('ajax ok')

# Create your views here.
