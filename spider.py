import config
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
import os


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
            return "登录失败请检查网络或联系软件作者\n" \
                   "https://github.com/whileTrue1949/2048downloader"

    def check_status(self):
        return self.get_by_xpath('/u.php?action=show', '//table//h1//text()')

    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)

    def get_html(self, url):
        resp = requests.get(config.URL + url, headers=config.headers)
        return etree.HTML(resp.content.decode())

    def get_by_xpath(self, url, xpath):
        return self.get_html(url).xpath(xpath)

    def get_torrent(self, url, download_xpath='//td[1]/div[1]/a/@href',
                    name_xpath='//td[1]/div[1]/a/font/text()'):
        html = self.get_html(url)
        return html.xpath(download_xpath), html.xpath(name_xpath)

    def download(self, url, filename, dir='.'):
        filepath = os.path.join(dir, filename)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        if os.path.isfile(filepath):
            print('文件已经存在', filepath)
            if os.path.getsize(filepath) == 0:
                os.remove(filepath)
                print('删除无效文件', filepath)
            else:
                return
        resp = requests.get(os.path.join(config.URL, url), headers=config.headers)
        if resp.status_code == 200:
            with open(filepath, 'wb') as wf:
                wf.write(resp.content)
                print('下载完成', filepath)
        else:
            print('下载失败', filepath)

    def get_page(self, fid, page=1):
        pass


sp = spider()
