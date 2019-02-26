"""the Responder web app"""
import logging

import responder
from starlette.websockets import WebSocketDisconnect


from .logcrawler import tail_log

logger = logging.getLogger(__name__)

def make_api():
    api = responder.API()

    @api.route('/')
    async def index(req, resp):
        resp.text = 'Hello logparser'

    @api.route('/ws', websocket=True)
    async def websocket(ws):
        await ws.accept()
        logging.info('while True')
        
        async for line in tail_log():
            logging.info(f'sending out to ws {line}')
            await ws.send_text(line)
        """
        while True:
            try:
                data = await ws.receive_text()
            except WebSocketDisconnect:
                logger.debug('websocket disconnected')
                break
            await ws.send_text('response from server')
        """
        await ws.close()
    return api