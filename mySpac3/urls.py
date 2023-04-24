"""mySpac3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from register import views as v
from games.views import *

urlpatterns = [
    path('bye/', v.bye_page, name="bye"),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('store.urls')),


    path('games', all_games, name='games'),
    path('game1', game1_view, name='game1'),
    path('game2', game2_view, name='game2'),
    path('game3', game3_view, name='game3'),
    # path('game4', game4_view, name='game4'),
    path('game5', game5_view, name='game5'),
    path('game1intro', game1_intro, name='game1intro'),
    path('recharge', no_money, name='recharge'),

    path('generate-link', v.generate_link, name='generate_link'),
    path('register/<str:link>', v.register, name="register"),
    path('profile', v.profile_page, name='profile'),
    path('accounts', include('django.contrib.auth.urls')),
    path('', include("django.contrib.auth.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "My SPAC3 Admin Panel"
admin.site.site_title = "My SPAC3"
admin.site.index_title = "My SPAC3"
