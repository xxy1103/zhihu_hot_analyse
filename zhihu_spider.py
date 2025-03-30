import requests
from lxml import html
from urllib import parse
from random import uniform
import time
import pandas
from dataclasses import dataclass, field
from typing import List, Any
import os
import hashlib
from bs4 import BeautifulSoup as bf
import urllib.request
from threading import Thread, Lock
import queue
import socket
import re
# 设置超时和重试参数
MAX_RETRIES = 3
TIMEOUT = 10

# 创建全局队列和锁
result_queue = queue.Queue()
print_lock = Lock()
data_lock = Lock()
make_dir_lock = Lock()


zhihu_hot_list = []
cookie = r"_xsrf=mkli2TRtNYyVbNeLzH5CbNwB5Gr0D6SI; _zap=27b83296-aef0-4a04-ae4c-3d9179924189; d_c0=APDRR6WVkBmPTkpxJV5GVFfKmK1SfLD5_lA=|1731979634; q_c1=752e14a99e1947878c4c8a582e035f63|1736564683000|1736564683000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1737302597,1737815283,1737879918,1738160077; z_c0=2|1:0|10:1742628512|4:z_c0|80:MS4xMlVidkNnQUFBQUFtQUFBQVlBSlZUYTFac1doZFd5SS1yWno4TktuTGEzQTFMRGRpTnJVby1nPT0=|70b029da16297402eef905ee4ac37a703c7f160d1419727e85fd56dc095a6ed2; __zse_ck=004_xOlE2Srhcc=JQ0Z8ctSqI1SeP/rPrdg6ltq0fzAyk=eAznxph9ypqsbqmZ2gqjwFzblzQmKTDOndgCDmDLayITjeaHlLcmDzrvJDyggrJQRxPEuhXQgL/raTfbPIu4/r-u38msjQnq7VMBEKMRIyykFIYzKVNF7PlUFAbEC+qHzgMCejTzeZwHRtq1txo2jOVxHQ6CwfNEfCADBUNnpUwvdq7thuquEUg3wtvyRRfCMHFfRpai0TttZjocAisSazWf/PAKC3oiPqmiIIKccTOUIqa6dP+3UhKuC3qjNBfZTE=; tst=h; BEC=8ce9e721fafad59a55ed220f1ad7f253; SESSIONID=CdJ9yt8O9SHdAw953HqacCkyV96OGfOViKqNb8wHhBP; JOID=U1sUA0jr6u_NbuZHBeqKfbxfrNwcqoyk9xWQfUvQu6WoLJN8Mi9fCqtu5kQHgm0Su6V-QnloQxE4Gbpdjb7fvOM=; osd=UFoQAEzo6-vOauVGAemOfr1br9gfq4in8xaReUjUuKSsL5d_MytcDqhv4kcDgWwWuKF9Q31rRxI5HblZjr_bv-c="
header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
          'cookie':cookie,
          }
def log(message):
        """线程安全的打印函数"""
        with print_lock:
            with open('data/log/log.txt', 'a', encoding='utf-8') as f:
                f.write(f'{message}\n')
def request_with_retry(url, max_retries=MAX_RETRIES, timeout=TIMEOUT):
    """带有重试机制的请求函数"""
    for attempt in range(max_retries):
        global header
        try:
            request = urllib.request.Request(url, headers = header)
            response = urllib.request.urlopen(request, timeout=timeout)
            return response
        except (urllib.error.URLError, socket.timeout) as e:
            log(f"尝试 {attempt+1}/{max_retries} 失败: {url} - {str(e)}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2)  # 失败后等待2秒再重试
def chinese_to_numeric_hash(text: str) -> str:
    """
    将输入的汉字字符串使用 SHA-256 哈希后，
    将结果转换为一个十进制数字字符串返回
    """
    # 对文本进行 UTF-8 编码，并计算 SHA-256 的哈希值（16进制字符串）
    hex_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    # 将16进制字符串转换为一个大整数，再转为十进制字符串
    numeric_hash = str(int(hex_hash, 16))
    return numeric_hash


@dataclass
class name_value:
    name: List[Any] = field(default_factory=list)
    hot_value: List[Any] = field(default_factory=list)
    
zhihu_hot_name = name_value()

class Spider:
    def __init__(self, headers = None):
        self.headers = headers

    def get_response(self, url, params=None):
        time.sleep(uniform(0.5, 0.8))    # 延迟请求
        try:
            response = requests.get(url=url, headers=self.headers, params=params, timeout=10)
            if response.status_code != 200:
                self.log(f'Status code: {response.status_code} {url}')
                return None
            self.log(f'Get {response.url}')
            return response
        except requests.exceptions.ChunkedEncodingError as e:
            self.log(f"ChunkedEncodingError encountered when requesting {url}: {e}. Retrying...")
            time.sleep(10)  # 重试前延迟一下
            try:
                response = requests.get(url=url, headers=self.headers, params=params, timeout=10)
                if response.status_code != 200:
                    self.log(f'Status code: {response.status_code} {url}')
                    return None
                self.log(f'Get {response.url}')
                return response
            except Exception as e:
                self.log(f"Retry failed for {url}: {e}")
                return None
        except requests.RequestException as e:
            self.log(f"Request failed for {url}: {e}")
            return None

    def save_to_csv(self, datas, name):
        df = pandas.DataFrame(datas)
        df.to_csv(f'{name}.csv', index=False, encoding='utf-8')

    def log(self, message):
        """线程安全的打印函数"""
        with print_lock:
            with open('data/log/log.txt', 'a', encoding='utf-8') as f:
                f.write(f'{message}\n')

def get_info(item):
    answer_url = item['链接']
    html = bf(request_with_retry(answer_url).read(), 'html.parser')
    QuestionHeader_side = html.find('div', class_='QuestionHeader-side')
    if QuestionHeader_side:
        item['关注者'] = QuestionHeader_side.find_all('strong',class_ = "NumberBoard-itemValue")[0].get_text()
        # 清理数字中的逗号等非数字字符，只保留数字
        item['关注者'] = re.sub(r'[^\d]', '', item['关注者'])
        item['被浏览量'] = QuestionHeader_side.find_all('strong',class_ = "NumberBoard-itemValue")[1].get_text()
    header_text = html.find('h4', class_='List-headerText')
    if header_text:
        item['总回答数'] = header_text.get_text().split(' ')[0]
    
    answer_html = html.find_all('div', class_='List-item')
    for i in range(len(answer_html)):
        item[f"回答{i+1}"] = []
        span = answer_html[i].find('span', class_='RichText ztext CopyrightRichText-richText css-ob6uua')
        if span:
            # 获取所有p标签，将每个p标签的文本作为数组的一个元素
            paragraphs = span.find_all('p')
            item[f"回答{i+1}"] = [p.get_text() for p in paragraphs]

        # 修改获取点赞数的方法
        vote_button = answer_html[i].find('button', {'aria-label': lambda x: x and '赞同' in x})
        if vote_button:
            # 从aria-label属性中提取数字，格式为"赞同 1107"
            aria_label = vote_button.get('aria-label', '')
            match = re.search(r'赞同\s+(\d+)', aria_label)
            if match:
                item[f"回答{i+1}点赞数"] = match.group(1)
            else:
                # 尝试从按钮文本中获取，格式为"赞同 1107"
                button_text = vote_button.get_text().strip()
                match = re.search(r'赞同\s+(\d+)', button_text)
                if match:
                    item[f"回答{i+1}点赞数"] = match.group(1)
                else:
                    item[f"回答{i+1}点赞数"] = "0"
        else:
            item[f"回答{i+1}点赞数"] = "0"

    return item
    
    
class ZhihuSpider(Spider):
    def __init__(self, headers=None):
        super().__init__(headers=headers)

    def get_hot(self):
        start = time.perf_counter()
        #以下为json法
        url = "https://www.zhihu.com/hot"
        res = request_with_retry(url)
        html = bf(res.read(), 'html.parser')
        HotItem = html.find_all('section', class_='HotItem')
        judgement = False  #判断表单是否变化
        for i in range(len(HotItem)):
            item = {'排名': None, '标题': None, '描述': None, '链接': None, '图像': None, '热度': None, '关注者': None, '被浏览量': None, '总回答数': None,"是否在榜":True,"是否已生成ai总结":False,"Hash":None}
            item['排名'] = i + 1
            item['标题'] = HotItem[i].find('h2').get_text()
            item['链接'] = HotItem[i].find('a')['href']
            raw_hot = HotItem[i].find('div', class_='HotItem-metrics').get_text()
            hot_match = re.search(r'(\d+(?:\.\d+)?)\s*(\w+)热度', raw_hot)
            if hot_match:
                hot_value = hot_match.group(1)  # 数字部分，如 "1644"
                hot_unit = hot_match.group(2)   # 单位部分，如 "万"
                item['热度'] = f"{hot_value} 万热度"# 只保留数字部分
            tmp = HotItem[i].find('p',class_='HotItem-excerpt')
            if tmp:
                item['描述'] = tmp.get_text()
            img = HotItem[i].find('img')
            if img:
                item['图像'] = img['src']
            item['Hash'] = chinese_to_numeric_hash(item['标题'])
            judge = False   #判断是否在榜
            for j in zhihu_hot_list:
                if item['标题'] == j['标题']:
                    j["排名"] = item["排名"]
                    j["描述"] = item["描述"]
                    j["链接"] = item["链接"]
                    j["图像"] = item["图像"]
                    j["热度"] = item["热度"]
                    j["是否在榜"] = True
                    judge = True #已经在榜了，不再添加
                    break
            #不在榜的话，添加回答
            if judge == False:
                item = get_info(item)
                judgement = True
                zhihu_hot_list.append(item)
                self.log(f"已添加新热搜：{item['标题']}")
        items_to_remove = []
        for i in zhihu_hot_list:
            if not i["是否在榜"]:
                items_to_remove.append(i)
        for item in items_to_remove:
            self.log(f"热搜{item['标题']}已不在榜,准备删除")
            try:
                os.remove("./index/Social Media Data Analytics Platform/public/doc/{}.md".format(item["Hash"]))
                self.log(f"已删除热搜{item['标题']}的ai评论总结")
            except Exception as e:
                    self.log(f"删除热搜{item['标题']}的ai评论总结失败, 原因: {e}")
            try:
                zhihu_hot_list.remove(item)
                self.log(f"已删除热搜{item['标题']}")
            except Exception as e:
                self.log(f"删除热搜{item['标题']}失败, 原因: {e}")
        #按排名排序
        zhihu_hot_list.sort(key=lambda x: x['排名'])

        for i in zhihu_hot_list:
            i["是否在榜"] = False
        #将热搜名字和热度存入zhihu_hot_name
        zhihu_hot_name.name = [i['标题'] for i in zhihu_hot_list]
        zhihu_hot_name.hot_value = [i['热度'] for i in zhihu_hot_list]
        self.log('Running time: %.6fs, Local time: %s'%(time.perf_counter() - start, time.ctime()))
        return judgement

    def run(self,key=0):
        change = self.get_hot()    #返回是否有热搜变化
        if change == True:
            self.save_to_csv(zhihu_hot_list, name = f'./data/csv/zhihu_hot{key}')
        return change


if __name__ == '__main__':
    zhihu = ZhihuSpider()
    zhihu.run()
    
