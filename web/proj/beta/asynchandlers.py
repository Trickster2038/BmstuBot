from beta.models import PersonT, FriendsT, FacultiesT
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def delete_outgoing(request):
    target=request.POST['target']
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=False).delete()

@login_required(login_url='/login/')
def delete_incoming(request):
    target=request.POST['target']
    FriendsT.objects.filter(user2=request.user.username, user1=target, applied=False).delete()

@login_required(login_url='/login/')
def accept_incoming(request):
    target=request.POST['target']
    p = FriendsT.objects.get(user2=request.user.username, user1=target, applied=False)
    p.applied = True
    p.save()

@login_required(login_url='/login/')
def delete_friend(request):
    target=request.POST['target']
    FriendsT.objects.filter(user2=request.user.username, user1=target, applied=True).delete()
    FriendsT.objects.filter(user1=request.user.username, user2=target, applied=True).delete()

@login_required(login_url='/login/')
def subscribe_request(request):
    target=request.POST['target']
    msg = FriendsT(user1=request.user.username, user2=target, applied=False)
    msg.save()