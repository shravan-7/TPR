"""Tourist_Place_recommendation URL Configuration

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
from django.urls import path
from Tourist_App.views import *
from django.conf import settings
from django.conf.urls.static import static
import Tourist_App.views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", home, name="index"),
    path("user/", user),
    path("registration/", registration, name="reg"),
    path("saveUser/", saveUser),  # type: ignore
    path("userlogin/", userlogin, name="userLogin"),  # type: ignore
    path("logout/", logoutNow),
    path("home/", home, name="home"),
    path("preferences/", preferences),
    path("profile/", profile),
    path("search/", search),
    path("recommendation/", recommendation, name="recommendation"),
    path("preferences/", Tourist_App.views.preferences, name="preferences"),
    path("editProfile/<int:id>", editProfile, name="editProfile"),  # type: ignore
    path("feedback/", feedback, name="feedback"),
    path("loadData/", loadData, name="loadData"),
    path("get_recommendation/", get_recommendation, name="get_recommendation"),
    path("getMoreDetails/<int:id>/", getMoreDetails, name="getMoreDetails"),
    path("search_places/", search_places, name="search_places"),
    path("topRated/", topRated, name="topRated"),
path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico"))),
    path("get_user_favorites/", get_user_favorites, name="get_user_favorites"),
    path("add_favorite/", add_favorite, name="add_favorite"),
    path("remove_favorite/", remove_favorite, name="remove_favorite"),
    path("favorite_places/", favorite_places, name="favorite_places"),
    path("submit_review/<int:id>/", submit_review, name="submit_review"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=staticfiles_urlpatterns()