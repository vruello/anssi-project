import anssi.settings
import datetime
import os

""" This file contains functions to manage media (screenshot / snapshot common file) """

MAX_MEDIA = 9

def get_media_path(session, type):
	""" Type is either screenshots or snapshots """
	date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
	return os.path.join(anssi.settings.MEDIA_ROOT, type, "{}-{}.png".format(session, date_string))


def remove_medias():
    # Remove screenshots
    screenshots_path = os.path.join(anssi.settings.MEDIA_ROOT, "screenshots")

    for root, dirs, files in os.walk(screenshots_path):
		for name in files:
			if "png" in name:
				# Don't remove gitignore
				full_path = os.path.join(screenshots_path, name)
				os.remove(full_path)


    # Remove snapshots
    snapshots_path = os.path.join(anssi.settings.MEDIA_ROOT, "snapshots")

    for root, dirs, files in os.walk(snapshots_path):
        for name in files:
			if "png" in name:
				# Don't remove gitignore
				full_path = os.path.join(snapshots_path, name)
				os.remove(full_path)
    
    # Remove passwords
    creds_path = os.path.join(anssi.settings.MEDIA_ROOT, "creds")

    for root, dirs, files in os.walk(creds_path):
        for name in files:
			if "txt" in name:
				# Don't remove gitignore
				full_path = os.path.join(creds_path, name)
				os.remove(full_path)



def remove_live_path():
	live_path = get_live_path()

	if os.path.exists(live_path):
		os.remove(live_path)


def get_live_url():
	return os.path.join(anssi.settings.MEDIA_URL, "snapshot_live.png")


def get_live_path():
	return os.path.join(anssi.settings.MEDIA_ROOT, "snapshot_live.png")


def get_medias(session, type):
    full_path = os.path.join(anssi.settings.MEDIA_ROOT, type)

    os.chdir(full_path)
    files = filter(os.path.isfile, os.listdir(full_path)) # Get the filenames

    # Select the right session
    files = [ f for f in files if f.startswith(str(session)) ]

    # Sort by date with a filter
    files.sort(key=lambda x: os.path.getmtime(os.path.join(full_path, x)))
    files.reverse()

    return files[:MAX_MEDIA]


def get_medias_url(session, type):
    files = get_medias(session, type)
    path = os.path.join(anssi.settings.MEDIA_URL, type)

    return [ os.path.join(path, f) for f in files ]
