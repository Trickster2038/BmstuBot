from beta.models import PersonT, FriendsT, FacultiesT, UserImage
from django.shortcuts import render
from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
import os

@login_required(login_url='/login/')
def outgoing(request):
    friends = FriendsT.objects\
        .filter(user1=request.user.username, applied=False)
    # if friends.count() != 0:
    friends_list = []
    for x in friends:
        p = PersonT.objects.get(id=x.user2)
        p.append_to_list(friends_list)

    data = {"friends": friends_list, \
    "neg_btn": True, \
    "caption": _("Outgoing"), \
    "btn_text": _("Cancel"), \
    "action": "delete_outgoing", \
    "alt_btn": False}
    if len(friends_list) > 0:
        return render(request, "lists/shortcards.html", context=data)
    else:
        return render(request, "lists/empty_list.html")

@login_required(login_url='/login/')
def incoming(request):
    friends = FriendsT.objects\
        .filter(user2=request.user.username, applied=False)
    # if friends.count() != 0:
    friends_list = []
    for x in friends:
        p = PersonT.objects.get(id=x.user1)
        p.append_to_list(friends_list)

    data = {"friends": friends_list, \
    "neg_btn": True, \
    "caption": _("Incoming"), \
    "btn_text": _("Discard"), \
    "action": "delete_incoming", \
    "alt_btn": True, \
    "alt_btn_text": _("Accept"), \
    "alt_action": "accept_incoming"}
        # print(data)
    if len(friends_list) > 0:
        return render(request, "lists/shortcards.html", context=data)
    else:
        return render(request, "lists/empty_list.html")

@login_required(login_url='/login/')
def friends(request):
    friends1 = FriendsT.objects\
        .filter(user1=request.user.username, applied=True)
    friends2 = FriendsT.objects\
        .filter(user2=request.user.username, applied=True)
    # if friends1.count() + friends2.count() != 0:
    friends_list = []
    trustmap = [_("not checked"), _("on check"), _("checked")]
    for x in friends1:
        p = PersonT.objects.get(id=x.user2)
        p.append_to_list(friends_list)
    for x in friends2:
        p = PersonT.objects.get(id=x.user1)
        p.append_to_list(friends_list)

    data = {"friends": friends_list}
    if len(friends_list) > 0:
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
        friends = PersonT.objects.filter(faculty= me.faculty, is_filled=True,\
            department= me.department, course__gt= me.course, is_curator= True)\
        .exclude(id__in= requested)
    else:
        friends = PersonT.objects.filter(faculty= me.faculty, is_filled=True,\
            department= me.department, course__gt= me.course, is_curator= True,\
            trusted= 2)\
        .exclude(id__in= requested)

    if friends.count() != 0:
        friends_list = []
        for p in friends:
            p.append_to_list(friends_list)

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

@login_required(login_url='/login/')
def moderate(request):
    me = PersonT.objects.get(id=request.user.username)
    if me.is_moderator:
        accounts = PersonT.objects.filter(trusted=1)
        # if accounts.count() != 0:
        acc_list = []
        for x in accounts:
            x.append_to_moderation(acc_list)

        data = {"accounts": acc_list}
        if len(acc_list) > 0:
            return render(request, "lists/moderation_list.html", context=data)
        else:
            return render(request, "lists/empty_list.html")
    else:
            return render(request, "lists/moderator_signup.html")