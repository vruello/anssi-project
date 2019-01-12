# -*- coding: utf-8 -*-

from metasploit.msfrpc import MsfRpcClient
import re
import urllib
import time
import anssi.settings
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import shutil


def ls_files_parser(lsret):
	lines = lsret.lstrip().split("\n")
	files = []

	# Skip errors
	while len(lines) > 0 and len(lines[0]) > 0 and lines[0].split()[0] != 'Listing:':
		lines.pop(0)

	if (len(lines) <= 5):
		return files

	# Parse files
	for line in lines[5:len(lines) - 2]:
		l = line.split()
		if len(l) < 7:
			break

		#if re.match(r"40777", l[0]) == None:
		files.append({
			'name': (" ".join(l[6:])),
			'urlencoded_name': urllib.quote_plus(" ".join(l[6:])),
			'permission': l[0],
			'size': l[1],
			'type': l[2],
			'last_modified': l[3],
			'hour': l[4],
			'timezone': l[5]
		})

	return files

def ls_pwd_parser(lsret):
	lines = lsret.lstrip().split("\n")
	for line in lines:
		l = line.split()
		if len(l) > 0 and "Listing:" in l[0]:
			return " ".join(l[1:]).replace('\\', '/')
	return ""


def add_routing_files(files):
	files.insert(0, {'name': '.', 'urlencoded_name': urllib.quote_plus('.'), 'type': 'dir'})
	files.insert(0, {'name': '..', 'urlencoded_name': urllib.quote_plus('..'), 'type': 'dir'})


def ls(shell):
	shell.write('ls\n')
	result = ''
	result = shell.read()

	error = False
	if "[-] stdapi_fs_ls: Operation failed: Access is denied." in result:
		error = True
	return (ls_pwd_parser(result), ls_files_parser(result), error)


def cd(shell, arg):
	shell.write("cd \"" + arg + "\"")
	time.sleep(0.5)


def download(shell, name):
	timestamp = int(time.time())
	path = str(timestamp)
	full_path = os.path.join(anssi.settings.MEDIA_ROOT, path)

	shell.write('download "' + name + '" "' + full_path + '"')

	ret = shell.read()

	while not "download" in ret:
		time.sleep(0.1)
		ret = shell.read()

	file_path = os.path.join(anssi.settings.MEDIA_ROOT, path + '/' + name)
	if os.path.exists(file_path):
		fh = open(file_path, 'rb')
		data = fh.read()
		response = HttpResponse(content_type="application/download")
		response['Content-Disposition'] = 'attachment; filename=' + name
		response.write(data)

		shutil.rmtree(os.path.join(anssi.settings.MEDIA_ROOT, path))
		return response

def upload(shell, uploaded_file):
	fs = FileSystemStorage()
	filename = fs.save(uploaded_file.name, uploaded_file)

	file_path = os.path.join(anssi.settings.MEDIA_ROOT, filename)

	shell.write('upload "' + file_path + '" .')

	ret = shell.read()

	succeed = False
	while not "uploaded" in ret and not "Operation failed" in ret:
		time.sleep(0.1)
		ret = shell.read()

	if "uploaded" in ret:
		succeed = True

	fs.delete(file_path)

	return succeed

def rm(shell, name):
	shell.write('rm "' + name + '"')
	time.sleep(0.5)


def rmdir(shell, name):
	shell.write('rmdir "' + name + '"')
	time.sleep(0.5)
