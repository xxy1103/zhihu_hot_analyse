import schedule
from draw_chart import draw_chart
from zhihu_spider import ZhihuSpider
from zhihu_spider import zhihu_hot_list
import threading
from response import run
import time
from AI_analyse import hot_list_analyse 


global key



def zhihu_update(zhihu):
    global key
    change = zhihu.run(key)
    if change == True:
        draw_chart(f'./data/csv/zhihu_hot{key}.csv', r'C:\Windows\Fonts\simhei.ttf', './index/Social Media Data Analytics Platform/')
        print("已更新图标")
        hot_list_analyse(f'./data/csv/zhihu_hot{key}.csv', './index/Social Media Data Analytics Platform/public/doc/')
        print("已更新ai主页分析")
        key += 1

if __name__ == '__main__':
    key = 0
    zhihu = ZhihuSpider()
    zhihu_update(zhihu)
    schedule.every(5).minutes.do(zhihu_update,zhihu)
    new_thread = threading.Thread(target=run)
    new_thread.start()
    while True:
        schedule.run_pending()
        time.sleep(1)