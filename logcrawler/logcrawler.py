"""tail a file"""
import asyncio
import logging
import os

LOG_FILEPATH = os.getenv('LOG_FILEPATH')

async def tail_log():
    """do it async"""
    if not LOG_FILEPATH:
        raise ValueError(f'no LOG_FILEPATH defined')
    if not os.stat(LOG_FILEPATH):
        raise ValueError('invalid file')
    command = f'tail -f {LOG_FILEPATH}'
    logging.info(f'calling {command}')
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    while True:
        try:
            #stdout, stderr = await process.communicate()
            logging.info('await readline')
            data = await process.stdout.readline()
            logging.info('got data...')
            if not data:
                logging.error('no data')
                break
            if data:
                line = data.decode('ascii').rstrip()
                yield line
        except KeyboardInterrupt:
            raise