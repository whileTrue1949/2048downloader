import config
from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import etree
import os


class spider():

    # 登陆接口
    def login(self, username, passwd, question, answer, lgt, customquest='', ):
        config.logger.info("用户登陆：%s", username)
        data = {
            'jumpurl': os.path.join(config.URL, 'index.php'),
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
            resp = requests.post(os.path.join(config.URL, 'login.php'), data=data, headers=config.headers)
            html = etree.HTML(resp.content.decode())
            # 更新 cookie
            config.logger.info("cookie= %s", resp.cookies.get_dict())
            config.headers['cookie'] = ";".join([c.name + "=" + c.value for c in resp.cookies])
            # 返回登陆的信息
            return "".join(html.xpath("//span/text()"))
        except Exception as err:
            config.logger.error("登陆失败: data= %s, err= %s", data, err)
            return "登录失败请检查网络或联系软件作者\n" \
                   "https://github.com/whileTrue1949/2048downloader"

    # 检查用户登陆状态 登陆返回 True
    def check_status(self):
        return len(self.get_by_xpath('u.php?action=show', '//table//h1//text()')) == 1

    def __init__(self):
        # 初始化线程池
        self.pool = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)

    # 根据 url 返回 html
    def get_html(self, url):
        config.logger.info("请求地址 url= %s", url)
        resp = requests.get(os.path.join(config.URL, url), headers=config.headers)
        return etree.HTML(resp.content.decode())

    # 解析 url 中 xpath
    def get_by_xpath(self, url, xpath):
        config.logger.info("解析 xpath= %s", xpath)
        return self.get_html(url).xpath(xpath)

    # 下载 url 页面 种子, 可配置download_xpath, name_xpath
    def get_torrent(self, url, download_xpath='//td[1]/div[1]/a/@href',
                    name_xpath='//td[1]/div[1]/a/font/text()'):
        html = self.get_html(url)
        return html.xpath(download_xpath), html.xpath(name_xpath)

    # 下载, url 为绝对地址
    def download(self, url, filename, dir='.'):
        config.logger.info("下载 url= %s, filename= %s, dir= %s", url, filename, dir)
        filepath = os.path.join(dir, filename)
        if not os.path.isdir(dir):
            config.logger.info('文件夹不存在 dir= %s', dir)
            os.makedirs(dir)
        if os.path.isfile(filepath):
            config.logger.info('文件已经存在 filepath= %s', filepath)
            if os.path.getsize(filepath) == 0:
                os.remove(filepath)
                config.logger.info('删除无效文件 filepath= %s', filepath)
            else:
                return
        resp = requests.get(url, headers=config.headers)
        if resp.status_code == 200:
            with open(filepath, 'wb') as wf:
                wf.write(resp.content)
                config.logger.info('下载完成 filepath= %s', filepath)
        else:
            config.logger.error('下载失败 filepath= %s, url= %s, resp.status_code= %s', filepath, url, resp.status_code)

    def get_page(self, fid, page):
        return self.get_by_xpath('thread.php?fid-{}-page-{}.html'.format(fid, page), '//td[@class="tal"]/a/@href')

    # 根据 fid 下载 start_page - end_page 内所有种子
    def download_by_page(self, fid, start_page, end_page, dir='.'):
        config.logger.info("下载 fid= %s, start_page= %s, end_page= %s, dir = %s", fid, start_page, end_page, dir)
        for p in range(start_page, end_page + 1):
            config.logger.info('正在下载第 %s 页', p)
            try:
                # 单线程下载
                # self.download_page(fid, p, dir)
                # 多线程下载
                self.pool.submit(self.download_page, fid, p, dir)
            except Exception as err:
                config.logger.error('下载第 %s 页发生异常, err= {%s}', p, err)

    def download_page(self, fid, page, dir='.'):
        for one in self.get_page(fid, page):
            try:
                download_url, filename = self.get_torrent(one)
                for k, v in enumerate(download_url):
                    config.logger.info("{%s} 页面发现种子: {%s}", v, filename[k])
                    # 需要处理 获得 url 地址为绝对地址
                    # 下载就不要开启多线程了
                    self.download(os.path.join(config.URL, v), filename[k], dir)
            except Exception as err:
                config.logger.error('下载 fid= %s, 第 %s 页发生异常, err= {%s}', fid, page, err)


sp = spider()
