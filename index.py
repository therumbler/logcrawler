#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
import cgitb
import logging
import os
import subprocess

logger = logging.getLogger(__name__)
# DEBUG ONLY
cgitb.enable()

MAIN_PY_PATH = os.getenv('MAIN_PY_PATH')
MAIN_PY_PATH = '/Users/brumble/Sites/logcrawler'

def _send_output(content, **headers):
    """send the content to the client"""
    if not isinstance(content, str):
        content = str(content)
    if 'Content-Type' not in headers:
        headers['Content-Type'] = 'text/plain'
    
    if '<html' in content:
        headers['Content-Type'] = 'text/html'

    if 'Content-Length' not in headers:
        headers['Content-Length'] = len(content)
    
    for k, v in headers.items():
        print('{}:{}'.format(k, v))
    print('')
    print(content)

def _get_index():
    with open('./static/index.html') as file_obj:
        contents = file_obj.read()
    return contents

def check_for_websocket_server():
    """check wether websocket server is running"""
    cmd = ['ps', 'x']

    try:
        resp = subprocess.check_output(cmd).decode()
        with open('logs.txt', 'w') as file_obj:
            file_obj.write(resp)
        if 'python main.py' in resp:
            # it's running
            resp = _get_index()
        else:
            logger.info('websocket server not running')
            resp = 'not running'
            os.chdir(MAIN_PY_PATH)
            cmd = ['/Library/Frameworks/Python.framework/Versions/3.7/bin/pipenv', 'run', 'python', 'main.py']
            subprocess.Popen(cmd)
            #_send_output(cmd)
            #return
            
    except subprocess.CalledProcessError as ex:
        resp = f'''{type(ex)}
        {ex}'''
    except Exception as ex:
        resp = f'''{type(ex)}
        {ex}'''

    return resp


def main():
    #content = _get_index()
    content = check_for_websocket_server()
    #content = MAIN_PY_PATH
    _send_output(content)
    return

if __name__ == "__main__":
    main()