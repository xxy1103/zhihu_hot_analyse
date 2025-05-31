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
cookie = r"_zap=bced0e7d-fee0-469c-b9d3-e99dbadbacb7; d_c0=eOdTTcVIdhqPTo0xt8rcvlEpoHttVGQ1ydw=|1747394521; _xsrf=47dc90d4-229c-41e0-9ec3-8f9b9ede2a8c; captcha_session_v2=2|1:0|10:1748595118|18:captcha_session_v2|88:R1JvL096d2RON2hrRzQ2WnVyaHRDakRwbzhQUVZwa2VVbllwWXhETktmRmRFR0RtMjEzcmx4T3lPNGZadlduSg==|c841054da562a6bcbbcdbe3197861be6375ce208dfe37f35e6adf04181b8711d; __snaker__id=FTf92uY5MgpXLyYt; gdxidpyhxdE=n1yk%5CfeU3DDA%5Cf6uxc9fNZOAzdQ%2B2PRZ%2Fc4vgXKcV%5CTy%2F2kqvXeDTtiItMzmg4AoToCbhkMyuBZDCujiBfE%5Czzl%2BGNSEqqRRkKBOcoOOI5DfVahxRiBJBP5zWQAZb2OImWTf6vzmf1vMaqe1X1yoG%5CDqLUTaaOhzQEzEQI5zKyjdB%5CAv%3A1748596019701; expire_in=15552000; q_c1=4c43941855e84d01b173def59c2f3c25|1748595130000|1748595130000; z_c0=2|1:0|10:1748595132|4:z_c0|92:Mi4xMlVidkNnQUFBQUI0NTFOTnhVaDJHaGNBQUFCZ0FsVk51YjhtYVFBc1NKSk5RRHRUdFFDSzJhdWF4VXZPN05GM3Fn|a3ed9001f3c085d426a28810dc145cb7e336cb33b11076bbfd87bf0aa69a95c0; SESSIONID=uQCAYpiF8CY0aJqTlupogF5p25h3x1fuJHVt0wUZENj; JOID=VV8cBU9BCh-nKlTnfUBpg9QUHn9qNFVT5HAkgDR6SUiYSR2WJ-TkKM4pWuZwlBks3yC6gv0nyQ5evQdxbrHhwkI=; osd=UFgSB0JEDRGlJ1Hgc0JkhtMaHHJvM1tR6XUjjjZ3TE-WSxCTIOrmJcsuVOR9kR4i3S2_hfMlxAtZswV8a7bvwE8=; tst=r; __zse_ck=004_X=vZSiHHpMVefUgyJRswyYoaSN3D6kStC5tZUWrX=fyKbsdqgmvBq558QCzK385Aa7xBz6i2zpfdi=XApWT7cH/zOgtQqdox6IZxd70kde1VtVhiEjNYLFOAitGC83Yw-Jw5KKouIzTUS/PG7msqb/hzDMp+aVR/SCtk9WMJmf+WNs5bAJH6p1OVVMCnmgJQ8QKaEVBy+C4+fHy7GSMmt/iHwoN4PTrlgtckNaF53no7vzTJc/8WB0VpKtAT5+I3Bkn2Bjb9NN9oqGwabdNw+rnnXlfq2dJjuXu3AYPadsdk=; BEC=8ce9e721fafad59a55ed220f1ad7f253"
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
    print(f"找到 {len(answer_html)} 个回答项")
    
    for i in range(len(answer_html)):
        item[f"回答{i+1}"] = []
        
        # 尝试多种可能的CSS类名，适应知乎页面结构的变化
        span = None
        possible_classes = [
            'RichText ztext CopyrightRichText-richText css-1yl6ec1',
            'RichText ztext CopyrightRichText-richText css-ob6uua',
            'RichText ztext CopyrightRichText-richText'
        ]
        
        for class_name in possible_classes:
            span = answer_html[i].find('span', class_=class_name)
            if span:
                print(f"回答{i+1}: 使用类名 '{class_name}' 找到内容")
                break
        
        # 如果仍然找不到，尝试使用更宽泛的选择器
        if not span:
            span = answer_html[i].find('span', class_=lambda x: x and 'RichText' in x and 'ztext' in x)
            if span:
                print(f"回答{i+1}: 使用宽泛选择器找到内容")
        
        if span:
            # 获取所有p标签，将每个p标签的文本作为数组的一个元素
            paragraphs = span.find_all('p')
            if paragraphs:
                item[f"回答{i+1}"] = [p.get_text() for p in paragraphs]
                print(f"回答{i+1}: 提取了 {len(paragraphs)} 个段落")
            else:
                # 如果没有p标签，直接获取span的文本内容
                item[f"回答{i+1}"] = [span.get_text().strip()]
                print(f"回答{i+1}: 直接提取span内容")
        else:
            print(f"回答{i+1}: 未找到内容元素")

        # 修改获取点赞数的方法，适应新的HTML结构
        vote_button = answer_html[i].find('button', {'aria-label': lambda x: x and '赞同' in x})
        if vote_button:
            # 从aria-label属性中提取数字，格式为"赞同 3206 " (注意可能有空格)
            aria_label = vote_button.get('aria-label', '').strip()
            match = re.search(r'赞同\s+(\d+)', aria_label)
            if match:
                item[f"回答{i+1}点赞数"] = match.group(1)
                print(f"回答{i+1}: 从aria-label提取点赞数 {match.group(1)}")
            else:
                # 尝试从按钮文本中获取
                button_text = vote_button.get_text().strip()
                match = re.search(r'赞同\s+(\d+)', button_text)
                if match:
                    item[f"回答{i+1}点赞数"] = match.group(1)
                    print(f"回答{i+1}: 从按钮文本提取点赞数 {match.group(1)}")
                else:
                    item[f"回答{i+1}点赞数"] = "0"
                    print(f"回答{i+1}: 未能解析点赞数，设为0")
        else:
            # 如果找不到按钮，尝试查找其他可能的点赞数显示方式
            vote_info = answer_html[i].find('div', string=lambda x: x and '人赞同了该回答' in x)
            if vote_info:
                match = re.search(r'(\d+)\s*人赞同了该回答', vote_info.get_text())
                if match:
                    item[f"回答{i+1}点赞数"] = match.group(1)
                    print(f"回答{i+1}: 从文本信息提取点赞数 {match.group(1)}")
                else:
                    item[f"回答{i+1}点赞数"] = "0"
                    print(f"回答{i+1}: 找到文本信息但无法解析点赞数")
            else:
                item[f"回答{i+1}点赞数"] = "0"
                print(f"回答{i+1}: 未找到点赞相关信息，设为0")

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
    
