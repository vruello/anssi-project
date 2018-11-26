# -*- coding: utf-8 -*-

from metasploit.msfrpc import MsfRpcClient
import re
import urllib
import time
import anssi.settings
from django.http import HttpResponse
import os

def ls_files_parser(lsret):
	lines = lsret.lstrip().split("\n")
	files = []
	for line in lines[5:len(lines) - 2]:
		l = line.split()
		#if re.match(r"40777", l[0]) == None:
		files.append({
			'name': (" ".join(l[6:])).encode('utf8'),
			'urlencoded_name': urllib.quote_plus(" ".join(l[6:]).encode('utf8')),
			'permission': l[0],
			'links': l[1],
			'type': l[2],
			'date': l[3],
			'hour': l[4],
			'date': l[5]
		})

	return files

def ls_pwd_parser(lsret):
	l = lsret.lstrip().split("\n")[0].split()[1:]
	return " ".join(l)


def add_routing_files(files):
	files.insert(0, {'name': '.', 'urlencoded_name': urllib.quote_plus('.'), 'type': 'dir'})
	files.insert(0, {'name': '..', 'urlencoded_name': urllib.quote_plus('..'), 'type': 'dir'})


def ls(shell):
	shell.write('ls\n')
	time.sleep(0.5)
	result = shell.read()
	return (ls_pwd_parser(result), ls_files_parser(result))


def cd(shell, arg):
	print "cd \"" + arg + "\""
	shell.write("cd \"" + arg + "\"")
	time.sleep(0.5)


def download(shell, name):
	timestamp = int(time.time())
	path = str(timestamp)
	full_path = anssi.settings.MEDIA_ROOT + path

	print full_path
	shell.write('download "' + name + '" "' + full_path + '"')

	ret = shell.read()
	print ret
	i = 0
	while re.match(r".*download.*", ret) == None:
		time.sleep(0.1)
		ret = shell.read()
		print i, ret
		i += 1

	print 'hello world'
	file_path = os.path.join(anssi.settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		fh = open(file_path, 'rb')
		response = HttpResponse(fh.read(), content_type="application/download")
		response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
		return response
