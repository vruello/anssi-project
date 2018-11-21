# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import urllib
from django.shortcuts import render

from core import core
from core.explorer import explorer
# Create your views here.


def home(request):
    return render(request, 'server/home.html')

def sessions(request):
	sessions = core.get_sessions()
	return render(request, 'server/sessions.html', {'sessions': sessions, 'length': len(sessions), 'dir': dir(sessions.items)})

def session(request, id):

	session = core.get_session_shell(int(id))	

	path = request.GET.get('path')
	print 'path', path 

	ftype = request.GET.get('type')
	print 'type', ftype

	if path != None and ftype == 'dir':
		explorer.cd(session, path)
	elif path != None and ftype == 'fil':
		explorer.download(session, path)

	pwd, files = explorer.ls(session)

	explorer.add_routing_files(files)

	return render(request, 'server/session.html', {'id': int(id), 'files': files, 'pwd': pwd})


