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

cookie = r"SESSIONID=F3wvGTSHXQaVMsPAmmijcgp4y2xH6g3G7RIrwKu7Hbu; JOID=W1EcB0qXSN4coRnVZJogTGOaX0Z9wQ7rVeJBsSTYBJR-6UGRPRnyc3apGdhsi60wXiEFRbNtfMB5WVNk6BbDN8Q=; osd=UVwcAE6dRd4bpRPYZJ0kRm6aWEJ3zA7sUehMsSPcDpl-7kWbMBn1d3ykGd9ogaAwWSUPSLNqeMp0WVRg4hvDMMA=; _xsrf=mkli2TRtNYyVbNeLzH5CbNwB5Gr0D6SI; _zap=27b83296-aef0-4a04-ae4c-3d9179924189; d_c0=APDRR6WVkBmPTkpxJV5GVFfKmK1SfLD5_lA=|1731979634; q_c1=752e14a99e1947878c4c8a582e035f63|1736564683000|1736564683000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1737302597,1737815283,1737879918,1738160077; z_c0=2|1:0|10:1738726849|4:z_c0|80:MS4xMlVidkNnQUFBQUFtQUFBQVlBSlZUZlJDZ21oT0FfM190bmJJZGNncUZZUlZuUnBBSG5qOGhRPT0=|507ef20541895351609cd75946c172228bac88c970fef382aed022745ee073b9; tst=h; SESSIONID=VF8LKXdMGLJoMPDYJScj6dp98Cr4MEAcoX1VSFGPFrw; JOID=UlEQC0uDPGsN1xHYPItV_H7hUkog3HZeSZxAsHzEeS1vkkGVacqKy2LeFNk51LqgxkCgL5ORKGTEOHl1iKR0huQ=; osd=V1oWA0qGN20F1hTTOoNU-XXnWksl13BWSJlLtnTFfCZpmkCQYsyCymfVEtE40bGmzkGlJJWZKWHPPnF0ja9yjuU=; __zse_ck=004_Fe7TJHiQlzZTUGt7WloV6gLlfIFnUawDQLJZst/QOE3VYE39RR5aGsy/oGBLGKo5Y0os3FVnrBsU=MHEX49P0YtAgi6ROeHQ7Vrb8IneC9T0=keOC2/zupltjjSwbNUJ-K+m+IQxJlHevH6kiYVjUcOvAm7GMHncL1W4L2NkAjwGOwqpTvQXoWPbGuccPMIGAGy4K1kj1ncM+vPF8gNbMGSLnq7pP4Ko2NQnIbARvf268VmIA7SO4GvCznC32q+x3; BEC=92a0fca0e2e4d1109c446d0a990ad863"
zhihu_hot_list = []

def log(message):
    with open('data/log/log.txt', 'a', encoding='utf-8') as f:
        f.write(f'{message}\n')



@dataclass
class name_value:
    name: List[Any] = field(default_factory=list)
    hot_value: List[Any] = field(default_factory=list)
zhihu_hot_name = name_value()

class Spider:
    def __init__(self, headers = None):
        self.headers = headers

    def get_response(self, url, params=None):
        time.sleep(uniform(0.2, 0.5))    # 延迟请求
        try:
            response = requests.get(url=url, headers=self.headers, params=params)
            if response.status_code != 200:
                self.log(f'Status code: {response.status_code} {url}')
                return None
            self.log(f'Get {response.url}')
            return response
        except requests.exceptions.ChunkedEncodingError as e:
            self.log(f"ChunkedEncodingError encountered when requesting {url}: {e}. Retrying...")
            time.sleep(1)  # 重试前延迟一下
            try:
                response = requests.get(url=url, headers=self.headers, params=params)
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
        with open('data/log/log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{message}\n')

class ZhihuSpider(Spider):
    def __init__(self):
        self.headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'cookie': cookie
                }

    def get_hot(self):
        start = time.perf_counter()
        #以下为json法
        url = "https://www.zhihu.com/api/v4/feed/topstory/hot-lists/total"
        res = self.get_response(url)
        res.encoding = 'utf-8'
        data = res.json()["data"]
        cnt = 1
        judgement = False  #判断表单是否变化
        for i in data:
            item = {'排名': None, '标题': None, '描述': None, '链接': None, '图像': None, '热度': None, '关注者': None, '被浏览量': None, '总回答数': None,"是否在榜":True,"是否已生成ai总结":False}
            item['排名'] = cnt
            item['标题'] = i['target']['title']
            item['描述'] = i['target']['excerpt']
            item['链接'] = 'https://www.zhihu.com/question/{}'.format(i['target']['id'])
            item['图像'] = i['children'][0]['thumbnail']
            item['热度'] = i['detail_text']
            item['关注者'] = i['target']['follower_count']
            item['总回答数'] = i['target']['answer_count']
            r = self.get_response(item['链接'])
            try:
                tree = html.fromstring(r.text)
                item['被浏览量'] = int(tree.xpath('//div[@class="NumberBoard-item"]//strong[@class="NumberBoard-itemValue"]/text()')[0].replace(',', ''))
            except:
                pass
            judge = False   #判断是否在榜
            for j in zhihu_hot_list:
                if item['标题'] == j['标题']:
                    j["排名"] = item["排名"]
                    j["标题"] = item["标题"]
                    j["描述"] = item["描述"]
                    j["链接"] = item["链接"]
                    j["图像"] = item["图像"]
                    j["热度"] = item["热度"]
                    j["关注者"] = item["关注者"]
                    j["被浏览量"] = item["被浏览量"]
                    j["总回答数"] = item["总回答数"]
                    j["是否在榜"] = True
                    judge = True #已经在榜了，不再添加
                    break
            #不在榜的话，添加回答
            if judge == False:
                answers = self.get_answer(i['target']['id'])
                item.update(answers)
                judgement = True
                zhihu_hot_list.append(item)
                self.log(f"已添加新热搜：{item['标题']}")
            cnt += 1
        items_to_remove = []
        for i in zhihu_hot_list:
            if not i["是否在榜"]:
                items_to_remove.append(i)
        for item in items_to_remove:
            self.log(f"热搜{item['标题']}已不在榜,准备删除")
            try:
                os.remove("./index/Social Media Data Analytics Platform/public/doc/{}.md".format(chinese_to_numeric_hash(item['标题'])))
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


    def get_answer(self, id):
        real_url = f'https://www.zhihu.com/api/v4/questions/{id}/feeds?'
        params={
                'include': 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].author.follower_count,vip_info,kvip_info,badge[*].topics;data[*].settings.table_of_content.enabled',
                'limit': '5',   # 爬取回答的个数
                'offset': '0',
                'order': 'default',
                'platform': 'desktop',
                'ws_qiangzhisafe': '1'
                }
        res = self.get_response(url = real_url, params = params)
        res.encoding = 'utf-8'
        data = res.json()['data']
        answers = {}
        cnt = 1
        for i in data:
            answers[f'回答{cnt}'] = html.fromstring(i['target']['content']).xpath('string(.)').strip()
            answers[f'回答{cnt}点赞数'] = i['target']['voteup_count']
            cnt += 1
        return answers

    def run(self,key=0):
        change = self.get_hot()    #返回是否有热搜变化
        if change == True:
            self.save_to_csv(zhihu_hot_list, name = f'./data/csv/zhihu_hot{key}')
        return change


if __name__ == '__main__':
    zhihu = ZhihuSpider()
    zhihu.run()
    