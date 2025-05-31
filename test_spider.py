#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试知乎爬虫的回答提取功能
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from zhihu_spider import get_info

def test_answer_extraction():
    """测试回答提取功能"""
    # 创建一个测试项目
    test_item = {
        '链接': 'https://www.zhihu.com/question/651188608',  # 使用你提供的HTML文件对应的链接
        '标题': '古代，如果一个男人没有那方面的能力会发生什么？'
    }
    
    print("开始测试回答提取功能...")
    print(f"测试链接: {test_item['链接']}")
    print("-" * 50)
    
    try:
        # 调用get_info函数
        get_info(test_item)
        
        # 打印结果
        print("提取结果:")
        for key, value in test_item.items():
            if key.startswith('回答'):
                print(f"{key}: {value[:100] if isinstance(value, list) and value else '空'}")
            elif '点赞数' in key:
                print(f"{key}: {value}")
            elif key in ['关注者', '被浏览量', '总回答数']:
                print(f"{key}: {value}")
        
        print("-" * 50)
        print("测试完成!")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_answer_extraction()
