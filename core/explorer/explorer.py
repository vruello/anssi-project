from metasploit.msfrpc import MsfRpcClient


class Explorer:
	def __init__(self, msfToolbox):
		self._msfToolbox = msfToolbox

	def ls(self, shell):
		shell.write('ls\n')
		result = shell.read()
		print result
		return result


	def cd(self, shell, arg):
		shell.write('cd ' + arg)
		result = shell.read()
		print result
		return result
