from beta.models import PersonT, FriendsT, FacultiesT, UserImage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageForm
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

@login_required(login_url='/login/')
def delete(request):
    if request.method=="POST":
        print("profile delete handler")
        return HttpResponse('delete profile')

@login_required(login_url='/login/')
def edit(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        print("> " + str(request.POST['name']))
        return HttpResponse('Form test')

    else:
        # initial={'tank': 123}
        form = NameForm()

    return render(request, 'profile/edit.html', {'form': form})

@login_required(login_url='/login/')
def verify(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print("> get form")
        print(request.FILES.keys())
        if form.is_valid():
            print("> save image")
            try:
                p = UserImage.objects.filter(user=request.user.username, folder="verify")
                for x in p:
                    x.delete()
            except:
                print("no image")
            img = UserImage(user=request.user.username, \
                folder="verify", \
                image=request.FILES['image'])
            img.save()
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
            try:
                p = UserImage.objects.filter(user=request.user.username, folder="avatars")
                for x in p:
                    x.delete()
            except:
                print("no image")
            img = UserImage(user=request.user.username, \
                folder="avatars", \
                image=request.FILES['image'])
            img.save()
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