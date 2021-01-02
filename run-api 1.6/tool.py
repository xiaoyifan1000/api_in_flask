"""
只保留爬取功能模块
其他的全删除了
返回xml
"""
import requests
from bs4 import BeautifulSoup
import function as func
import datetime
import time


class NyaaSearch:

    __request = None
    __site_now = None  # 当前爬取网页
    __criteria_now = '0'  # 标准
    __category_now = '0_0'  # 类型
    __content_now = None  # 查询内容
    __page_now = '1'  # 当前页码
    __save_file = None  # 保存文件
    __TIMES = True  # 是否需要保存
    __run = True  # 是否需要运行
    __search_time = None  # 搜索页面范围
    __user = None  # 用户搜索

    def __init__(self, site, search_time=10):
        """site：支持nyaa或者sukebei, search_time：搜索页面范围"""
        self.site = site  # 当前站点
        self.__search_time = int(search_time)+1

    def set_site(self, site):
        """设置查询网页"""
        self.__site_now = site

    def set_criteria(self, criteria):
        """设置查询的标准"""
        self.__criteria_now = criteria

    def set_category(self, category):
        """设置查询的类型"""
        self.__category_now = category

    def set_content(self, content):
        """设置查询的内容"""
        self.__content_now = content

    def set_page(self, page):
        """设置查询的页码"""
        self.__page_now = page

    def set_save(self):
        """设置查询的保存的文件目录"""
        self.__save_file = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def set_user(self, user):
        """设置查询的用户"""
        self.__user = user

    def return_site(self):
        """返回查询的站点"""
        return self.__site_now

    def return_criteria(self):
        """返回查询的标准"""
        return self.__criteria_now

    def return_category(self):
        """返回查询的类型"""
        return self.__category_now

    def return_content(self):
        """返回查询的内容"""
        return self.__content_now

    def return_page(self):
        """返回查询的页码"""
        return self.__page_now

    def return_save(self):
        """返回查询的保存的文件目录"""
        return self.__save_file

    def return_user(self):
        """返回查询的用户"""
        return self.__user

    @staticmethod
    def categories(criteria: str, category: str, page: str, content=None, user=None):
        if user:
            user = f"user/{user}"
        else:
            user = ''

        if content:
            return f"{user}?f={criteria}&c={category}&q={content}&p={page}"
        return f"{user}?f={criteria}&c={category}&q=&p={page}"

    def page(self):  # 页面合成
        self.set_site(self.site + self.categories(criteria=self.__criteria_now,
                                                  category=self.__category_now,
                                                  content=self.__content_now,
                                                  page=str(self.__page_now),
                                                  user=self.__user))

    def run_check(self):  # 运行前检测
        if self.__TIMES:
            self.set_save()
            self.__TIMES = False

    def run_and_search(self):
        """开始搜索"""
        self.run_check()
        self.page()
        if not self.__run:
            return 0
        try:
            request_ = requests.get(self.__site_now)
        except Warning:
            print("参数不存在，请检查参数！")
            return 3

        soup = BeautifulSoup(request_.text, 'html.parser')
        tboby = soup.tbody
        out = []
        name = None
        if not hasattr(tboby, 'children'):  # 无查询结果
            return 4

        for soup_tr in tboby.children:
            if soup_tr == '\n':
                continue
            category = soup_tr.a['title']
            soup_categories = soup_tr.find('td', {'colspan': '2'})
            title_url_0 = ['category', 'title', 'href']
            title_url_1 = [category]
            for tag_a in soup_categories.find_all('a'):
                if tag_a['title'] and func.filter_name(tag_a['title']) is True:
                    title_url_1.append(tag_a['title'])
                if tag_a['href'] and func.filter_name(tag_a['href']) is True:
                    title_url_1.append(tag_a['href'])
            name = dict(zip(title_url_0, title_url_1))

            torrent_magnet_0 = ['torrent', 'magnet']
            torrent_magnet_1 = []
            soup_download = soup_tr.find('td', {'class': 'text-center'})
            for tag_a in soup_download.find_all('a'):
                if tag_a['href'] and func.filter_name(tag_a['href']) is True:
                    torrent_magnet_1.append(tag_a['href'])
            torrent_magnet = dict(zip(torrent_magnet_0, torrent_magnet_1))

            soup_download_ = soup_tr.find_all('td', {'class': 'text-center'})
            download_inf = {'size': soup_download_[1].string,
                            'date': soup_download_[2].string,
                            'seeders': soup_download_[3].string,
                            'leechers': soup_download_[4].string,
                            'completed': soup_download_[5].string
                            }

            name.update(torrent_magnet)
            name.update(download_inf)
            func.write_xml(func.dict_to_xml(self.__content_now, name), f"static/{self.__save_file}.xml")
            out.append(name)
        if not name:  # 停止查询
            self.__run = False
            return -1
        return out

    def running(self):
        """范围页面查询"""
        for a in range(1, self.__search_time):
            self.__page_now = a
            out = self.run_and_search()
            time.sleep(1)
            return out

    def only_page_running(self, page):
        """单页面查询"""
        self.__page_now = page
        out = self.run_and_search()
        return out


if __name__ == '__main__':
    n = NyaaSearch('https://sukebei.nyaa.si/', search_time=1)
    n.set_user('mikocon')
    n.set_criteria('0')
    n.set_content("ルネ")
    n.set_category('1_3')
    n.set_save()
    n.running()
