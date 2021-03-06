import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(message)s')
logger = logging.getLogger()
URL = 'https://hjd2048.com/2048'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

MAX_WORKERS = 16
DOWNLOAD_DIR = 'download'
