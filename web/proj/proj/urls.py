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
from beta import views, asynchandlers, listviews, profilehandlers

from django.templatetags.static import static
from django.conf import settings
# import os
# from django.conf.urls import url
from django.conf.urls.static import static

# SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

urlpatterns = [
    path('outgoing/', listviews.outgoing, name='outgoing'),
    path('incoming/', listviews.incoming, name='icoming'),
    path('friends/', listviews.friends, name='friends'),
    path('search/', listviews.search, name='search'),
    path('moderate/', listviews.moderate),

    path('', views.index, name='home'),
    path('profile/', views.profile, name='profile'),

    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),

    path('asyncDeleteOutgoing/', asynchandlers.delete_outgoing),
    path('asyncDeleteIncoming/', asynchandlers.delete_incoming),
    path('asyncAcceptIncoming/', asynchandlers.accept_incoming),
    path('asyncDeleteFriend/', asynchandlers.delete_friend),
    path('asyncSubscribeRequest/', asynchandlers.subscribe_request),

    path('profileDelete/', profilehandlers.delete),
    path('verify/', profilehandlers.verify),
    path('avatar/', profilehandlers.avatar),
    path('deleteAvatar/', profilehandlers.delete_avatar),
    path('edit/', profilehandlers.edit, name='edit'),
    path('switchCurator/', profilehandlers.switch_curator),

    path(r'setlanguage/', views.set_language, name='set_language'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
