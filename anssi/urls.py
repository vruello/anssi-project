"""anssi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from server import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sessions$', views.sessions, name="sessions"),
    url(r'^sessions/(\d+)$', views.session, name="session"),
    url(r'^sessions/(\d+)/session_explorer$', views.session_explorer, name="session_explorer"),
    url(r'^sessions/(\d+)/session_screenshot$', views.session_screenshot, name="session_screenshot"),
    url(r'^init$', views.init, name="init"),
    url(r'^jobs$', views.jobs, name="jobs"),
    url(r'^$', views.home, name="home")
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
