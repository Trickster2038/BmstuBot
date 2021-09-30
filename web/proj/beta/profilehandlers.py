from beta.models import PersonT, FriendsT, FacultiesT
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from .forms import ImageForm
from django.shortcuts import render

@login_required(login_url='/login/')
def delete(request):
    if request.method=="POST":
        print("profile delete handler")
        return HttpResponse('delete profile')

@login_required(login_url='/login/')
def verify(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        print("> get form")
        if form.is_valid():
            print("> save image")
            form.save()
        else:
            print("> form error")
        return HttpResponse('Form test')

    else:
        # initial={'tank': 123}
        form = ImageForm()

    return render(request, 'profile/verify.html', {'form': form})