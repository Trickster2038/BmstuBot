from beta.models import PersonT, FriendsT, FacultiesT, UserImage
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import redirect
from django.conf import settings

from django.templatetags.static import static
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required
# from .forms import NameForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import logout
import os

# from django.contrib.staticfiles.templatetags.staticfiles import static
# from django.db import connection,transaction
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.db.models import Q


# TODO
# - edit, delete, (moderator)
# - media sources
 
def index(request):
    return render(request, 'misc/root.html')

@login_required(login_url='/login/')
def profile(request):
    # print("session: " + request.user.username)
    p = PersonT.objects.get(id=request.user.username)
    p = p.detail()

    fl = p.avatar_exist()
    me = {"rowdata": p, 
        "avatar": fl, \
        "path_avatar": 'avatars/' + str(request.user.username) + '.jpg'}
    # print(me)

    data = {"person": me}
    return render(request, "profile/profile.html", context=data)

# def asyncview(request):
#     print("> ajax test view")
#     if request.method=="POST":
#         target=request.POST['target']
#         print("> ajax target: " + target)
#     return HttpResponse('ajax ok')

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
