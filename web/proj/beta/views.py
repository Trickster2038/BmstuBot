from beta.models import PersonT, FriendsT, FacultiesT
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection,transaction
from django.shortcuts import redirect
from django.conf import settings

# from django.contrib.staticfiles.templatetags.staticfiles import static

from django.templatetags.static import static
from django.contrib.staticfiles import finders
# from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required

from .forms import NameForm

from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.contrib.auth import logout

import os

# TODO
# + i18n
# - full profile, edit, delete, (moderator)
# - search + safe
# - separate asyncviews/handlers
 
def index(request):
    return render(request, 'root.html')

@login_required(login_url='/login/')
def profile(request):
    # print("session: " + request.user.username)
    p = PersonT.objects.get(id=request.user.username)
    trustmap = [_("not checked"), _("on check"), _("checked")]
    p.trusted = _(trustmap[p.trusted])
    p.faculty = FacultiesT.objects.get(id=p.faculty).name
    p.department = p.faculty + str(p.department)

    picture = finders.find('avatars/' + str(request.user.username) + '.jpg')
    fl = (picture != None)

    me = {"rowdata": p, 
        "avatar": fl, \
        "path_avatar": 'avatars/' + str(request.user.username) + '.jpg'}
    # print(me)

    data = {"person": me}
    return render(request, "beta/profile.html", context=data)

@login_required(login_url='/login/')
def edit(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        print("> " + str(request.POST['name']))
        return HttpResponse('Form test')

    else:
        # initial={'tank': 123}
        form = NameForm()

    return render(request, 'beta/edit.html', {'form': form})

@login_required(login_url='/login/')
def outgoing(request):
    friends = FriendsT.objects.filter(user1=request.user.username, applied=False)
    if friends.count() != 0:
        friends_list = []
        trustmap = [_("not checked"), _("on check"), _("checked")]
        for x in friends:
            p = PersonT.objects.get(id=x.user2)

            p.trusted = _(trustmap[p.trusted])
            p.faculty = FacultiesT.objects.get(id=p.faculty).name
            p.department = p.faculty + str(p.department)

            picture = finders.find('avatars/' + str(x.user2) + '.jpg')
            fl = (picture != None)
            # print("> " + url + " " + str(fl) + " " + str(gg)) 
            friends_list.append({"rowdata": p, 
                "avatar": fl, \
                "path_avatar": 'avatars/' + str(x.user2) + '.jpg'})

        data = {"friends": friends_list, \
        "caption": _("Outgoing"), \
        "btn_text": _("Cancel"), \
        "action": "delete_outgoing", \
        "alt_btn": False}
        # print(data)
        return render(request, "shortcards.html", context=data)
    else:
        return render(request, "empty_list.html")

@login_required(login_url='/login/')
def incoming(request):
    friends = FriendsT.objects.filter(user2=request.user.username, applied=False)
    if friends.count() != 0:
        friends_list = []
        trustmap = [_("not checked"), _("on check"), _("checked")]
        for x in friends:
            p = PersonT.objects.get(id=x.user1)

            p.trusted = _(trustmap[p.trusted])
            p.faculty = FacultiesT.objects.get(id=p.faculty).name
            p.department = p.faculty + str(p.department)

            picture = finders.find('avatars/' + str(x.user1) + '.jpg')
            fl = (picture != None)
            friends_list.append({"rowdata": p, 
                "avatar": fl, \
                "path_avatar": 'avatars/' + str(x.user1) + '.jpg'})

        data = {"friends": friends_list, \
        "caption": _("Incoming"), \
        "btn_text": _("Discard"), \
        "action": "delete_incoming", \
        "alt_btn": True, \
        "alt_btn_text": _("Accept"), \
        "alt_action": "accept_incoming"}
        # print(data)
        return render(request, "shortcards.html", context=data)
    else:
        return render(request, "empty_list.html")

@login_required(login_url='/login/')
def friends(request):
    friends1 = FriendsT.objects.filter(user1=request.user.username, applied=True)
    friends2 = FriendsT.objects.filter(user2=request.user.username, applied=True)
    if friends1.count() + friends2.count() != 0:
        friends_list = []
        trustmap = [_("not checked"), _("on check"), _("checked")]
        for x in friends1:
            p = PersonT.objects.get(id=x.user2)

            p.trusted = _(trustmap[p.trusted])
            p.faculty = FacultiesT.objects.get(id=p.faculty).name
            p.department = p.faculty + str(p.department)

            picture = finders.find('avatars/' + str(x.user2) + '.jpg')
            fl = (picture != None)
            friends_list.append({"rowdata": p, 
                "avatar": fl, \
                "path_avatar": 'avatars/' + str(x.user2) + '.jpg'})
        for x in friends2:
            p = PersonT.objects.get(id=x.user1)

            p.trusted = _(trustmap[p.trusted])
            p.faculty = FacultiesT.objects.get(id=p.faculty).name
            p.department = p.faculty + str(p.department)

            picture = finders.find('avatars/' + str(x.user1) + '.jpg')
            fl = (picture != None)
            friends_list.append({"rowdata": p, 
                "avatar": fl, \
                "path_avatar": 'avatars/' + str(x.user1) + '.jpg'})

        data = {"friends": friends_list, \
        "caption": _("Friends"), \
        "btn_text": _("Delete"), \
        "action": "delete_friend"}
        # print(data)
        return render(request, "fullcards.html", context=data)
    else:
        return render(request, "empty_list.html")

def asyncview(request):
    print("> ajax test view")
    if request.method=="POST":
        target=request.POST['target']
        print("> ajax target: " + target)
    return HttpResponse('ajax ok')

@login_required(login_url='/login/')
def async_delete_outgoing(request):
    target=request.POST['target']
    print("> delete out view")
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=False).delete()

@login_required(login_url='/login/')
def async_delete_incoming(request):
    target=request.POST['target']
    print("> delete in view")
    FriendsT.objects.filter(user2=request.user.username, user1=target, applied=False).delete()

@login_required(login_url='/login/')
def async_accept_incoming(request):
    target=request.POST['target']
    print("> delete in view")
    p = FriendsT.objects.get(user2=request.user.username, user1=target, applied=False)
    p.applied = True
    p.save()

@login_required(login_url='/login/')
def async_delete_friend(request):
    target=request.POST['target']
    print("> delete in view")
    FriendsT.objects.filter(user2=request.user.username, user1=target, applied=True).delete()
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=True).delete()

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

def logout_view(request):
    logout(request)
    return redirect('/')

# Create your views here.
