from beta.models import PersonT, FriendsT, FacultiesT, UserImage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageForm, EditForm
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

@login_required(login_url='/login/')
def switch_curator(request):
    p = PersonT.objects.get(id=request.user.username)
    p.is_curator = not p.is_curator 
    p.save()
    return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def delete(request):
    if request.method=="POST":
        print("profile delete handler")
        return HttpResponse('delete profile')

@login_required(login_url='/login/')
def delete_avatar(request):
    p = UserImage.objects.filter(user=request.user.username, folder="avatars")
    for x in p:
        x.delete()
    p = PersonT.objects.get(id=request.user.username)
    p.trusted = 0
    p.save()
    return HttpResponseRedirect("/profile/")

@login_required(login_url='/login/')
def edit(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        print("> bio: " + str(request.POST['bio']))
        if form.is_valid():
            p = PersonT.objects.get(id=request.user.username)
            trusted = (p.course == int(request.POST['course']))
            if not trusted:
                p.trusted = 0
            p.bio = request.POST['bio']
            p.course = int(request.POST['course'])
            # p.is_curator = request.POST['curator']
            p.save()
        return HttpResponseRedirect('/profile/')

    else:
        # initial={'tank': 123}
        form = EditForm()
        return render(request, 'profile/edit.html', \
        {'form': form, 'action': '/edit/', 'caption':_("TXT.edit_acc_info")})

    return render(request, 'profile/edit.html', {'form': form})

@login_required(login_url='/login/')
def verify(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print("> get form")
        print(request.FILES.keys())
        if form.is_valid():
            print("> save image")
            p = UserImage.objects.filter(user=request.user.username, folder="verify")
            for x in p:
                try:
                    x.delete()
                except Exception as e:
                    pass
            img = UserImage(user=request.user.username, \
                folder="verify", \
                image=request.FILES['image'])
            img.save()
            p = PersonT.objects.get(id=request.user.username)
            p.trusted = 1
            p.save()
        else:
            print("> form error")
            print(form.errors)
        return HttpResponseRedirect("/profile/")
    else:
        form = ImageForm()

    return render(request, 'profile/edit.html', \
        {'form': form, 'action': '/verify/', 'caption':_("Edit verification photo")})

@login_required(login_url='/login/')
def avatar(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        # form.title = str(request.user.username)
        print("> get form")
        print(request.FILES.keys())
        if form.is_valid():
            p = UserImage.objects.filter(user=request.user.username, folder="avatars")
            for x in p:
                try:
                    x.delete()
                except Exception as e:
                    pass
            img = UserImage(user=request.user.username, \
                folder="avatars", \
                image=request.FILES['image'])
            img.save()
            p = PersonT.objects.get(id=request.user.username)
            p.trusted = 0
            p.save()
            print("> avatar save")
        else:
            print("> form error")
            print(form.errors)
        return HttpResponseRedirect("/profile/")

    else:
        # initial={'tank': 123}
        form = ImageForm()

    return render(request, 'profile/edit.html', \
        {'form': form, 'action': '/avatar/', 'caption':_("Edit avatar")})