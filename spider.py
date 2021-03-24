import config
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree


class spider():

    def login(self, username, passwd, question, answer, lgt, customquest='', ):
        data = {
            'jumpurl': config.URL + '/index.php',
            'step': '2',
            'cktime': '31536000',
            'pwuser': username,
            'pwpwd': passwd,
            'lgt': lgt,
            'question': question,
            'customquest': customquest,
            'answer': answer
        }
        try:
            resp = requests.post(config.URL + '/login.php', data=data, headers=config.headers)
            html = etree.HTML(resp.content.decode())
            config.headers['cookie'] = ";".join([c.name + "=" + c.value for c in resp.cookies])
            return "".join(html.xpath("//span/text()"))
        except Exception as err:
            print(err)
            return "登录失败请检查网络或联系软件作者QQ2312362137"

    def check_status(self):
        resp = requests.get(config.URL + '/u.php?action=show', headers=config.headers)

    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)


sp = spider()
