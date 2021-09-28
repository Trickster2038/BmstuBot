"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as authviews
from django.urls import path, include
from beta import views

urlpatterns = [
    path('outgoing/', views.outgoing, name='outgoing'),
    path('incoming/', views.incoming, name='icoming'),
    path('friends/', views.friends, name='friends'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit, name='edit'),
    # path('edit-handler/', views.edit_handler, name='edit_handler'),

    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(), name='logout'),
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('asyncview/', views.asyncview),

    path('asyncDeleteOutgoing/', views.async_delete_outgoing),
    path('asyncDeleteIncoming/', views.async_delete_incoming),
    path('asyncAcceptIncoming/', views.async_accept_incoming),
    path('asyncDeleteFriend/', views.async_delete_friend),

    path(r'setlanguage/', views.set_language, name='set_language'),
]
