from beta.models import PersonT, FriendsT, FacultiesT
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='/login/')
def async_subscribe_request(request):
    # print("> subscribe")
    target=request.POST['target']
    msg = FriendsT(user1=request.user.username, user2=target, applied=False)
    # print(msg)
    msg.save()