from beta.models import Friendship, People, Person, PersonT, FriendsT, FacultiesT
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,transaction
from django.shortcuts import redirect
from django.conf import settings

# from django.contrib.staticfiles.templatetags.staticfiles import static

from django.templatetags.static import static
from django.contrib.staticfiles import finders
# from django.contrib.staticfiles.storage import staticfiles_storage

import os
 
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
    # print(request.session[settings.LANGUAGE_SESSION_KEY])
    friends = FriendsT.objects.filter(user1=request.user.username, applied=False)
    friends_list = []
    trustmap = ["no", "on check", "yes"]
    # print("> " + str(settings.BASE_DIR))
    for x in friends:
        p = PersonT.objects.get(id=x.user2)

        p.trusted = trustmap[p.trusted]
        p.faculty = FacultiesT.objects.get(id=p.faculty).name
        p.department = p.faculty + str(p.department)

        picture = finders.find('avatars/' + str(x.user2) + '.jpg')
        fl = (picture != None)
        # print("> " + url + " " + str(fl) + " " + str(gg)) 
        friends_list.append({"rowdata": p, 
            "avatar": fl, \
            "path_avatar": 'avatars/' + str(x.user2) + '.jpg'})

    data = {"friends": friends_list, \
    "caption": "Outgoing", \
    "btn_style": "btn-outline-danger", \
    "btn_text": "Cancel", \
    "action": "delete_outgoing"}
    print(data)
    return render(request, "shortcards.html", context=data)

def asyncview(request):
    print("> ajax test view")
    if request.method=="POST":
        target=request.POST['target']
        print("> ajax target: " + target)
    return HttpResponse('ajax ok')

def async_delete_outgoing(request):
    target=request.POST['target']
    print("> delete view")
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=False).delete()

def set_language(request):
    if not settings.LANGUAGE_SESSION_KEY in request.session:
        request.session[settings.LANGUAGE_SESSION_KEY] = "en-us"
    if request.session[settings.LANGUAGE_SESSION_KEY] == "en-us":
        lang = "ru"
    else:
        lang = "en-us"
    request.session[settings.LANGUAGE_SESSION_KEY] = lang
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    print(request.session[settings.LANGUAGE_SESSION_KEY])
    return response

# Create your views here.
