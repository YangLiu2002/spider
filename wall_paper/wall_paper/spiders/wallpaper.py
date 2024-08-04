"""
代码内容说明：
    自由选择爬取图片类型，爬取页数

函数库下载：
    pip install requests -i https://pypi.douban.com/simple
    pip install hashlib -i https://pypi.douban.com/simple   md5 加密库
    pip install bs4 -i https://pypi.douban.com/simple
    pip install lxml -i https://pypi.douban.com/simple

"""

import scrapy
from bs4 import BeautifulSoup
from ..items import WallPaperItem


class WallpaperSpider(scrapy.Spider):
    name = 'wallpaper'
    # allowed_domains = ['pic.netbian.com']
    start_urls = ['https://pic.netbian.com/']
    print('-' * 50)
    print("""
                                          请输入需要爬取壁纸类型的编号：
                                              1、4k 独家
                                              2、4k 动漫
                                              3、4k 美女
                                              4、4k 风景
                                              5、4k 游戏
                                              6、4k 影视
                                              7、4k 汽车
                                              8、4k 动物
                                              9、4k 宗教
                                              10、4k 背景
                                              11、平板壁纸
                                              12、4k 手机壁纸


              """)
    print('-' * 50)
    n = int(input("请输入对应序号："))
    m = int(input("请输入爬取页数："))

    # 请求

    def parse(self, response):
        ele = BeautifulSoup(response.text, 'html.parser')
        sections = ele.select('div.classify.clearfix a')
        hrefs = []
        for section in sections:
            href = section['href']
            hrefs.append(href)
        head_url = f"https://pic.netbian.com{hrefs[self.n - 1]}"
        for page in range(2, self.m+2):
            page_url = head_url + f'index_{page}.html'
            yield scrapy.Request(url=page_url, callback=self.parse)

        ele_model = BeautifulSoup(response.text, 'html.parser')
        sections_page = ele_model.select('div.slist ul li')
        for section_page in sections_page:
            href = section_page.select_one('a')['href']
            img_href = 'https://pic.netbian.com' + href
            yield scrapy.Request(url=img_href, callback=self.parse_detail_info)

    # 数据处理
    def parse_detail_info(self, response):
        ele = BeautifulSoup(response.text, 'html.parser')
        img_src = ele.select_one("#img img")["src"]
        img_name = ele.select_one("#img img")['title']  # 图片名字
        img_url = f"https://pic.netbian.com/{img_src}"  # 图片地址
        print('正在爬取：'+img_url, img_name)

        # 将图片和名字封装到item中

        item = WallPaperItem()
        item['img_url'] = img_url
        item['img_name'] = img_name
        item['m'] = self.m
        item['n'] = self.n

        yield item





