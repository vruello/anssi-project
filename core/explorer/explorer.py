from metasploit.msfrpc import MsfRpcClient

def ls(shell):
	shell.write('ls\n')
	result = shell.read()
	print result
	return result


def cd(shell, arg):
	shell.write('cd ' + arg)
	result = shell.read()
	print result 
	return result