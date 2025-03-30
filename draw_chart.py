import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def draw_chart(file_path,   #读取表格路径
                font_path,  #字体路径
                output_dir, #输出路径
                key = ''    #关键字
                ):
    # 设置字体
    font = FontProperties(fname=font_path, size=15)

    # 读取csv文件
    data = pd.read_csv(file_path) 
    

    # 删除column列（如果存在）
    if 'column' in data.columns:
        data = data.drop(columns=['column'])

    # 去掉热度一列的后缀'万热度'，并转换为数值类型
    data['热度'] = data['热度'].str.replace('万热度', '').astype(float)

    # 画出热度折线图并保存到本地
    plt.figure(figsize=(10, 6))
    plt.plot(data['排名'], data['热度'], marker='o')
    plt.xlabel('排名', fontproperties=font)
    plt.ylabel('热度', fontproperties=font)
    plt.title('排名与热度关系', fontproperties=font)
    plt.savefig(f'{output_dir}src/image/热度折线图{key}.png')  #保存到本地
    plt.close()

    # 统计点赞数总和并求均值
    data['点赞均值'] = data[['回答1点赞数', '回答2点赞数']].sum(axis=1) / 5

    # 找出点赞均值前五位的标题
    top_5_titles = data.nlargest(5, '点赞均值')['标题']
    with open(f'{output_dir}public/doc/高质量的热搜标题{key}.txt', 'w', encoding='utf-8') as f:
        for title in top_5_titles:
            f.write(title + '\n')

    # 画出关注者折线图
    plt.figure(figsize=(10, 6))
    plt.plot(data['排名'], data['关注者'], marker='o')
    plt.xlabel('排名', fontproperties=font)
    plt.ylabel('关注者', fontproperties=font)
    plt.title('排名与关注者关系', fontproperties=font)
    plt.savefig(f'{output_dir}src/image/关注者折线图{key}.png')
    plt.close()

    top_5_followed_titles = data.nlargest(5, '关注者')['标题']
    with open(f'{output_dir}public/doc/关注者最高的5个标题{key}.txt', 'w', encoding='utf-8') as f:
        for title in top_5_followed_titles:
            f.write(title + '\n')

    # 画出总回答数折线图
    plt.figure(figsize=(10, 6))
    plt.plot(data['排名'], data['总回答数'], marker='o')
    plt.xlabel('排名', fontproperties=font)
    plt.ylabel('总回答数', fontproperties=font)
    plt.title('排名与总回答数关系', fontproperties=font)
    plt.savefig(f'{output_dir}/src/image/总回答数折线图{key}.png')
    plt.close()

    top_5_answer_count_titles = data.nlargest(5, '总回答数')['标题']
    with open(f'{output_dir}public/doc/总回答数最高的5个标题{key}.txt', 'w', encoding='utf-8') as f:
        for title in top_5_answer_count_titles:
            f.write(title + '\n')



if __name__ == '__main__':
    draw_chart('./data/csv/zhihu_hot0.csv', r'C:\Windows\Fonts\simhei.ttf', './data/')