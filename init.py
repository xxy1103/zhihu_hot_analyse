import schedule
import threading
import time
import os
import re
import pandas as pd
import ast
import sys

# 添加模块导入检查
try:
    from draw_chart import draw_chart
    from zhihu_spider import ZhihuSpider, zhihu_hot_list, log
    from response import run  # 使用更新后的response模块（内部使用Flask）
    from AI_analyse import hot_list_analyse, hot_answer_analyse
except ImportError as e:
    print(f"模块导入失败: {e}")
    print("请确保所有依赖模块都存在并且可以正常导入")
    sys.exit(1)

# 全局变量初始化
key = 0

cookie = r"SESSIONID=bl8Dk5g9iaEMyc9OH7O145kJIeVcgg3UNAadm55gYxR; JOID=UVwcC0IcmvfdbfcKERf3b6Net5wCbsa1nT6AblYu3qPsDbd8SCuWzL5g_QYRBOPXeIktqKCSLzJpKxiLamKLaLg=; osd=W10SA08Wm_nVYP0LHx_6ZaJQv5EIb8i9kDSBYF4j1KLiBbp2SSWewbRh8w4cDuLZcIQnqa6aIjhoJRCGYGOFYLU=; _zap=bced0e7d-fee0-469c-b9d3-e99dbadbacb7; d_c0=eOdTTcVIdhqPTo0xt8rcvlEpoHttVGQ1ydw=|1747394521; _xsrf=47dc90d4-229c-41e0-9ec3-8f9b9ede2a8c; captcha_session_v2=2|1:0|10:1748595118|18:captcha_session_v2|88:R1JvL096d2RON2hrRzQ2WnVyaHRDakRwbzhQUVZwa2VVbllwWXhETktmRmRFR0RtMjEzcmx4T3lPNGZadlduSg==|c841054da562a6bcbbcdbe3197861be6375ce208dfe37f35e6adf04181b8711d; __snaker__id=FTf92uY5MgpXLyYt; gdxidpyhxdE=n1yk%5CfeU3DDA%5Cf6uxc9fNZOAzdQ%2B2PRZ%2Fc4vgXKcV%5CTy%2F2kqvXeDTtiItMzmg4AoToCbhkMyuBZDCujiBfE%5Czzl%2BGNSEqqRRkKBOcoOOI5DfVahxRiBJBP5zWQAZb2OImWTf6vzmf1vMaqe1X1yoG%5CDqLUTaaOhzQEzEQI5zKyjdB%5CAv%3A1748596019701; expire_in=15552000; q_c1=4c43941855e84d01b173def59c2f3c25|1748595130000|1748595130000; z_c0=2|1:0|10:1748595132|4:z_c0|92:Mi4xMlVidkNnQUFBQUI0NTFOTnhVaDJHaGNBQUFCZ0FsVk51YjhtYVFBc1NKSk5RRHRUdFFDSzJhdWF4VXZPN05GM3Fn|a3ed9001f3c085d426a28810dc145cb7e336cb33b11076bbfd87bf0aa69a95c0; SESSIONID=uQCAYpiF8CY0aJqTlupogF5p25h3x1fuJHVt0wUZENj; JOID=VV8cBU9BCh-nKlTnfUBpg9QUHn9qNFVT5HAkgDR6SUiYSR2WJ-TkKM4pWuZwlBks3yC6gv0nyQ5evQdxbrHhwkI=; osd=UFgSB0JEDRGlJ1Hgc0JkhtMaHHJvM1tR6XUjjjZ3TE-WSxCTIOrmJcsuVOR9kR4i3S2_hfMlxAtZswV8a7bvwE8=; __zse_ck=004_X=vZSiHHpMVefUgyJRswyYoaSN3D6kStC5tZUWrX=fyKbsdqgmvBq558QCzK385Aa7xBz6i2zpfdi=XApWT7cH/zOgtQqdox6IZxd70kde1VtVhiEjNYLFOAitGC83Yw-Jw5KKouIzTUS/PG7msqb/hzDMp+aVR/SCtk9WMJmf+WNs5bAJH6p1OVVMCnmgJQ8QKaEVBy+C4+fHy7GSMmt/iHwoN4PTrlgtckNaF53no7vzTJc/8WB0VpKtAT5+I3Bkn2Bjb9NN9oqGwabdNw+rnnXlfq2dJjuXu3AYPadsdk=; tst=r; BEC=6c53268835aec2199978cd4b4f988f8c"

header = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    'cookie': cookie,
}

def zhihu_update(zhihu):
    global key
    try:
        change = zhihu.run(key)
    except Exception as e:
        log(f"更新失败,等待下次更新，错误信息：{e}")
        return False
    
    if change:
        # 使用相对路径代替硬编码路径
        font_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', 'simhei.ttf')
        
        try:
            draw_chart(f'./data/csv/zhihu_hot{key}.csv', font_path, './index/vue/')
            log("已更新图表")
        except Exception as e:
            log(f"更新图表失败，错误信息：{e}")
        
        try:
            hot_list_analyse(f'./data/csv/zhihu_hot{key}.csv', './index/vue/public/doc/')
            log("已更新ai主页分析")
        except Exception as e:
            log(f"更新ai主页分析失败，错误信息：{e}")
        
        try:
            hot_answer_analyse(zhihu_hot_list, './index/vue/public/doc/')
            log("已更新所有ai评论总结")
        except Exception as e:
            log(f"更新所有ai评论总结失败，错误信息：{e}")
        
        key += 1
        return True
    return False

def csv_to_list_of_dict(csv_path):
    """将CSV文件转换为字典列表，处理回答列的特殊格式"""
    try:
        # 检查文件是否存在
        if not os.path.exists(csv_path):
            log(f"CSV文件不存在: {csv_path}")
            return []
        
        # 先读取标题行
        tmp_df = pd.read_csv(csv_path, encoding='utf-8', nrows=0)
        answer_cols = [col for col in tmp_df.columns if re.match(r'回答\d+', col)]
        
        # 为回答列创建转换器
        converters = {col: ast.literal_eval for col in answer_cols}
        
        df = pd.read_csv(csv_path, encoding='utf-8', converters=converters)
        return df.to_dict(orient='records')
    
    except Exception as e:
        log(f"读取CSV文件失败: {e}")
        return []

def initialize_key_and_data():
    """初始化key值和热榜数据"""
    global key
    csv_dir = './data/csv'
    
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir, exist_ok=True)
        key = 0
        return
    
    files = os.listdir(csv_dir)
    keys = []
    
    for file in files:
        match = re.match(r'zhihu_hot(\d+)\.csv$', file)
        if match:
            keys.append(int(match.group(1)))
    
    if keys:
        key = max(keys)
        new_list = csv_to_list_of_dict(f'./data/csv/zhihu_hot{key}.csv')
        zhihu_hot_list.clear()
        zhihu_hot_list.extend(new_list)
        log(f"已加载现有数据，当前key值: {key}")
    else:
        key = 0
        log("未找到现有数据，从0开始")

def main():
    """主函数"""
    try:
        # 初始化数据
        initialize_key_and_data()
        
        # 创建爬虫实例
        zhihu = ZhihuSpider(headers=header)
        
        # 初始更新
        success = zhihu_update(zhihu)
        if not success:
            log("程序初始化失败，退出程序")
            return
        
        log("程序初始化成功！！进入稳定运行阶段")
        
        # 启动web服务线程
        new_thread = threading.Thread(target=run, daemon=True)
        new_thread.start()
        
        # 设置定时任务
        schedule.every(5).minutes.do(zhihu_update, zhihu)
        
        # 主循环
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        log("程序被用户中断")
    except Exception as e:
        log(f"程序运行出错：{e}")
    finally:
        log("程序退出")

if __name__ == '__main__':
    main()