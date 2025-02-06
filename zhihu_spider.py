import requests
from lxml import html
from urllib import parse
from random import uniform
import time
import pandas
from dataclasses import dataclass, field
from typing import List, Any
import re
from collections import Counter

cookie = r"_xsrf=mkli2TRtNYyVbNeLzH5CbNwB5Gr0D6SI; _zap=27b83296-aef0-4a04-ae4c-3d9179924189; d_c0=APDRR6WVkBmPTkpxJV5GVFfKmK1SfLD5_lA=|1731979634; q_c1=752e14a99e1947878c4c8a582e035f63|1736564683000|1736564683000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1737302597,1737815283,1737879918,1738160077; z_c0=2|1:0|10:1738726849|4:z_c0|80:MS4xMlVidkNnQUFBQUFtQUFBQVlBSlZUZlJDZ21oT0FfM190bmJJZGNncUZZUlZuUnBBSG5qOGhRPT0=|507ef20541895351609cd75946c172228bac88c970fef382aed022745ee073b9; tst=h; SESSIONID=4mwS77wubagqcc58Ghno125PocoH3C4Dae58nou7f06; JOID=U1kXCkpgpZPwsGaNW2jFAoqAJRZBVMvvq4dR-SUCxPeK2wW4YPH8NJ-wZYVYtxmxcX965qovOu7b8aoEUCWknV8=; osd=VlEdBUxlrZn_tmOFUWfDB4KKKhBEXMHgrYJZ8yoEwf-A1AO9aPvzMpq4b4peshG7fnl_7qAgPOvT-6UCVS2uklk=; __zse_ck=004_cs5aIC4shnOvp54yRDd=tuzR9uqrgsblF7/2qj=FDMSl3jPmgF3ts8QYQpLZi0GN7N=4GmP9COSMIrK2iTTYGR62ZQa0VX2GraX7AEPscL6846DgXFt4nZLEJiTzsK3A-47gnweAMYCJ3Bx5zPWEB5DB+1uMq9ajeMBbp3BsmgswPd95xS9asWHu2FyErqiaG0sbAlkcMZtQan3Y9VjeckRtCglMeOTTNONqJPh90kl3PvEqOaXzmaJRNzd4Kda8X;"


@dataclass
class name_value:
    name: List[Any] = field(default_factory=list)
    hot_value: List[Any] = field(default_factory=list)

zhihu_hot_list = name_value()

class Spider:
    def __init__(self, headers = None):
        self.headers = headers

    def get_response(self, url, params=None):
        time.sleep(uniform(0.5, 1.0))    # 延迟请求
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
        datas = []
        cnt = 1
        if(len(zhihu_hot_list.name) != 0):
            zhihu_hot_list.name.clear()
            zhihu_hot_list.hot_value.clear()
        
        for i in data:
            item = {'排名': None, '标题': None, '描述': None, '链接': None, '图像': None, '热度': None, '关注者': None, '被浏览量': None, '总回答数': None}
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
            answers = self.get_answer(i['target']['id'])
            item.update(answers)
            datas.append(item)
            cnt += 1
            zhihu_hot_list.name.append(item['标题'])
            numbers_only = ''.join(re.findall(r'\d+', item['热度']))
            zhihu_hot_list.hot_value.append(numbers_only)
        self.log('Running time: %.6fs, Local time: %s'%(time.perf_counter() - start, time.ctime()))
        return datas

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

    def run(self,key = ''):
        datas = self.get_hot()
        self.save_to_csv(datas, name = f'data/csv/zhihu_hot{key}')


if __name__ == '__main__':
    zhihu_hot_list = name_value()
    zhihu = ZhihuSpider()
    zhihu.run()