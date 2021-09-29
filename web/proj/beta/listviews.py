from beta.models import PersonT, FriendsT, FacultiesT
from django.shortcuts import render
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
import os

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
        "neg_btn": True, \
        "caption": _("Outgoing"), \
        "btn_text": _("Cancel"), \
        "action": "delete_outgoing", \
        "alt_btn": False}
        # print(data)
        return render(request, "lists/shortcards.html", context=data)
    else:
        return render(request, "lists/empty_list.html")

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
        "neg_btn": True, \
        "caption": _("Incoming"), \
        "btn_text": _("Discard"), \
        "action": "delete_incoming", \
        "alt_btn": True, \
        "alt_btn_text": _("Accept"), \
        "alt_action": "accept_incoming"}
        # print(data)
        return render(request, "lists/shortcards.html", context=data)
    else:
        return render(request, "lists/empty_list.html")

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

        data = {"friends": friends_list}
        return render(request, "lists/friends.html", context=data)
    else:
        return render(request, "lists/empty_list.html")

@login_required(login_url='/login/')
def search(request):
    safety = (request.GET['safe'] == "true")
    print("safety: "+ str(safety))
    me = PersonT.objects.get(id=request.user.username)
    # friends = FriendsT.objects.filter(user2=request.user.username)

    requested = \
    list(FriendsT.objects\
        .filter(user1=request.user.username)\
        .values_list('user2', flat=True))

    if not safety:
        friends = PersonT.objects.filter(faculty= me.faculty,\
            department= me.department, course__gt= me.course, is_curator= True)\
        .exclude(id__in= requested)
    else:
        friends = PersonT.objects.filter(faculty= me.faculty,\
            department= me.department, course__gt= me.course, is_curator= True,\
            trusted= 2)\
        .exclude(id__in= requested)

    if friends.count() != 0:
        friends_list = []
        trustmap = [_("not checked"), _("on check"), _("checked")]
        for p in friends:
            # p = PersonT.objects.get(id=x.user1)

            p.trusted = _(trustmap[p.trusted])
            p.faculty = FacultiesT.objects.get(id=p.faculty).name
            p.department = p.faculty + str(p.department)

            picture = finders.find('avatars/' + str(p.id) + '.jpg')
            fl = (picture != None)
            friends_list.append({"rowdata": p, 
                "avatar": fl, \
                "path_avatar": 'avatars/' + str(p.id) + '.jpg'})

        data = {"friends": friends_list, \
        "neg_btn": False, \
        "alt_btn": True, \
        "caption": _("TXT.Search"), \
        "alt_btn_text": _("Subscribe"), \
        "alt_action": "send_subscribe_request"}
        # print(data)
        return render(request, "lists/shortcards.html", context=data)
    else:
        return render(request, "lists/empty_list.html")