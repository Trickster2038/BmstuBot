from beta.models import PersonT, FriendsT, FacultiesT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

@login_required(login_url='/login/')
def delete_outgoing(request):
    target=request.POST['target']
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=False).delete()
    return HttpResponse('delete outgoing')

@login_required(login_url='/login/')
def delete_incoming(request):
    target=request.POST['target']
    FriendsT.objects.filter(user2=request.user.username, user1=target, applied=False).delete()
    return HttpResponse('delete incoming')

@login_required(login_url='/login/')
def accept_incoming(request):
    target=request.POST['target']
    p = FriendsT.objects.get(user2=request.user.username, user1=target, applied=False)
    p.applied = True
    p.save()
    return HttpResponse('accept incoming')

@login_required(login_url='/login/')
def delete_friend(request):
    target=request.POST['target']
    FriendsT.objects.filter(user2=request.user.username, user1=target, applied=True).delete()
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=True).delete()
    return HttpResponse('delete friend')

@login_required(login_url='/login/')
def subscribe_request(request):
    target=request.POST['target']
    msg = FriendsT(user1=request.user.username, user2=target, applied=False)
    msg.save()
    return HttpResponse('subscribe request')

@login_required(login_url='/login/')
def confirm_moderation(request):
    # print("> confirm moderation")
    p = PersonT.objects.get(id=request.user.username)
    if p.is_moderator:
        target=request.POST['target']
        x = PersonT.objects.get(id=target)
        x.trusted = 2
        x.save()
    return HttpResponse('ajax moderation')

@login_required(login_url='/login/')
def discard_moderation(request):
    # print("> confirm moderation")
    p = PersonT.objects.get(id=request.user.username)
    if p.is_moderator:
        target=request.POST['target']
        x = PersonT.objects.get(id=target)
        x.trusted = 0
        x.save()
    return HttpResponse('ajax moderation')