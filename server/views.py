# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render

from core import core
# Create your views here.


def home(request):
    return render(request, 'server/home.html')

def sessions(request):
	sessions = core.get_sessions()
	return render(request, 'server/sessions.html', {'sessions': sessions})

def session(request):
	return render(request, '/server/session_explorer.html')


