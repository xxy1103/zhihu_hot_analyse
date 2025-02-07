import schedule
from draw_chart import draw_chart
from zhihu_spider import ZhihuSpider
from zhihu_spider import zhihu_hot_list
from zhihu_spider import log
import threading
from response import run
import time
from AI_analyse import hot_list_analyse 
from AI_analyse import hot_answer_analyse

global key



def zhihu_update(zhihu):
    global key
    change = zhihu.run(key)
    if change == True:
        try:
            draw_chart(f'./data/csv/zhihu_hot{key}.csv', r'C:\Windows\Fonts\simhei.ttf', './index/Social Media Data Analytics Platform/')
            log("已更新图表")
        except Exception as e:
            log("更新图表失败，错误信息：{}".format(e))
        try:
            hot_list_analyse(f'./data/csv/zhihu_hot{key}.csv', './index/Social Media Data Analytics Platform/public/doc/')
            log("已更新ai主页分析")
        except Exception as e:
            log("更新ai主页分析失败，错误信息：{}".format(e))
        try:
            hot_answer_analyse(zhihu_hot_list, './index/Social Media Data Analytics Platform/public/doc/')
            log("已更新所有ai评论总结")
        except Exception as e:
            log("更新所有ai评论总结失败，错误信息：{}".format(e))
        key += 1

if __name__ == '__main__':
    key = 0
    try:
        zhihu = ZhihuSpider()
        zhihu_update(zhihu)
        log("程序初始化成功！！进入稳定运行阶段：")
    except Exception as e:
        log("程序初始化失败，错误信息：{}".format(e))
        exit()
    new_thread = threading.Thread(target=run)
    new_thread.start()
    schedule.every(5).minutes.do(zhihu_update,zhihu)
    while True:
        schedule.run_pending()
        log("等待下一次更新...")
        time.sleep(1)