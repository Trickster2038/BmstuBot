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
        form = ImageForm(request.POST)
        user_id = request.user.username
        print("> ImageForm"+ str(type(request.POST['image'])))
        print("> ImageForm"+ str(request.FILES))
        for x in request.FILES:
            print("> ImageForm"+ str(x))

        form = ImageForm(request.POST or None, request.FILES or None)
        # form.save()
        print("> ImageForm"+ str(form))
        file_image = request.POST.get('image')
        print("> ImageForm"+ str(file_image))
        # file = open("sample_image.png", "wb")
        # file.write(response.content)
        # file.close()
        return HttpResponse('Form test')

    else:
        # initial={'tank': 123}
        form = ImageForm()

    return render(request, 'profile/verify.html', {'form': form})