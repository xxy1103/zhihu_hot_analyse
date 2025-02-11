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
import os
import re
import pandas as pd
import ast

global key



def zhihu_update(zhihu):
    global key
    global zhihu_hot_list
    try:
        change = zhihu.run(key)
    except Exception as e:
        log("更新失败,等待下次更新，错误信息：{}".format(e))
        return False
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


def csv_to_list_of_dict(csv_path):
    # 读取 CSV 文件，确保编码正确（例如 utf-8）
    # 先读取 CSV 文件的标题以确定哪些列是“回答”列（回答后跟数字的列）
    tmp_df = pd.read_csv(csv_path, encoding='utf-8', nrows=0)
    answer_cols = [col for col in tmp_df.columns if re.match(r'回答\d+', col)]
    # 为每个“回答”列创建转换函数，将字符串转换为 Python 对象
    converters = {col: (lambda x: ast.literal_eval(x)) for col in answer_cols}
    df = pd.read_csv(csv_path, encoding='utf-8', converters=converters)
    # orient='records' 表示将每一行转换为一个字典
    return df.to_dict(orient='records')



if __name__ == '__main__':
    csv_dir = './data/csv'
    if os.path.exists(csv_dir):
        files = os.listdir(csv_dir)
        keys = []
        for file in files:
            match = re.match(r'zhihu_hot(\d+)\.csv$', file)
            if match:
                keys.append(int(match.group(1)))
        if keys:  # 如果目录不为空，则取最大的 key
            key = max(keys)
            new_list = csv_to_list_of_dict(f'./data/csv/zhihu_hot{key}.csv')
            # 修改全局变量的内容，而不是重新赋值
            zhihu_hot_list.clear()
            zhihu_hot_list.extend(new_list)

        else:
            key = 0
    else:
        key = 0
    try:
        zhihu = ZhihuSpider()
        j =  zhihu_update(zhihu)
        log("程序初始化成功！！进入稳定运行阶段：")
    except Exception as e:
        log("程序初始化失败，错误信息：{}".format(e))
        exit()
    if j == False:
        exit()
    new_thread = threading.Thread(target=run)
    new_thread.start()
    schedule.every(5).minutes.do(zhihu_update,zhihu)
    while True:
        schedule.run_pending()
        time.sleep(1)