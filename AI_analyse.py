from ollama import Client
import pandas as pd
import re
from zhihu_spider import chinese_to_numeric_hash
from zhihu_spider import log 




def hot_list_analyse(file_path, output_dir, key =""):
    
    data = pd.read_csv(file_path)
    client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)
    response = client.chat(model='deepseek-r1:8b', messages=[
    {
      'role': 'system',
      'content': 
      '''
你是一个专门负责总结热榜的机器人，你根据热搜榜的信息总结出社会当前的热门话题，并且将所有的热门话题进行分类，展示当前社会最关注的几个方面:
输出部分格式如下：
(具体有几个分类由你决定，每个分类有几个话题也由你决定，不过需要按照格式展示)
### 1. **第一个分类**
  - ...（第一个分类的第一个话题）
  - ...（第一个分类的第二个话题）
  - ...(具体有几个话题由你自己决定）

### 2. **第二个分类**
   - ...（第二个分类的第一个话题）
   - ...（第二个分类的第二个话题）

### 3. **第三个分类**
    - ...（第三个分类的第一个话题）
      ''',
    },
    {
      'role': 'user',
      'content': str(data['标题']),
    },
])
    parts = re.split(r"<think>.*?</think>\n\n", response['message']['content'], flags=re.S)
    with open(output_dir + "hot_list_analyse.md", "w") as f:
        f.write(parts[1])

def hot_answer_analyse(zhihu_hot_list, output_dir, key =""):
    cnt = 1
    for i in zhihu_hot_list:
      if i["是否已生成ai总结"] == True:
        continue
      client = Client(
        host='http://localhost:11434',
        headers={'x-some-header': 'some-value'}
      )
      response = client.chat(model='deepseek-r1:8b', messages=[
      {
      'role': 'system',
      'content': 
      '''
我希望你扮演一个知乎评论分析师，结合**问题**以及阅读以下热门评论，并为我提炼出评论中的核心争议点。请分析不同观点之间的冲突，并解释每个观点的潜在影响。
      ''',
    },
    {
      'role': 'user',
      'content': str(i),
    },
])
      parts = re.split(r"<think>.*?</think>\n\n", response['message']['content'], flags=re.S)
      name = chinese_to_numeric_hash(i["标题"])
      with open(output_dir + name +".md", "w") as f:
        f.write(parts[1])
      log(f"已分析第{cnt}条热搜{i['标题']}的热门评论")
      cnt += 1
      i["是否已生成ai总结"] = True


if __name__ == '__main__':
  hot_list_analyse("./data/csv/zhihu_hot0.csv", "./data/text")
  