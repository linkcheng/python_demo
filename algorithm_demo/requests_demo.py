#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


data = {
    "01 源码阅读准备之基础知识准备": "http://img.kaikeba.com/01%20%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E5%87%86%E5%A4%87%E4%B9%8B%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%E5%87%86%E5%A4%87.mp4",
    "02 源码阅读准备之源码环境准备": "http://img.kaikeba.com/02%20%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E5%87%86%E5%A4%87%E4%B9%8B%E6%BA%90%E7%A0%81%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87.mp4",
    "03 源码阅读准备之源码剖析思路介绍": "http://img.kaikeba.com/03%20%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E5%87%86%E5%A4%87%E4%B9%8B%E6%BA%90%E7%A0%81%E5%89%96%E6%9E%90%E6%80%9D%E8%B7%AF%E4%BB%8B%E7%BB%8D.mp4",
    "04 源码阅读准备之从一个demo入手": "http://img.kaikeba.com/04%20%E6%BA%90%E7%A0%81%E9%98%85%E8%AF%BB%E5%87%86%E5%A4%87%E4%B9%8B%E4%BB%8E%E4%B8%80%E4%B8%AAdemo%E5%85%A5%E6%89%8B.mp4",
    "05 生产者源码之producer核心流程介绍": "http://img.kaikeba.com/05%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E6%A0%B8%E5%BF%83%E6%B5%81%E7%A8%8B%E4%BB%8B%E7%BB%8D.mp4",
    "06-1 生产者源码之producer初始化": "http://img.kaikeba.com/06%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%88%9D%E5%A7%8B%E5%8C%96%281%29.mp4",
    "06-2 生产者源码之producer初始化": "http://img.kaikeba.com/06%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%88%9D%E5%A7%8B%E5%8C%96%282%29.mp4",
    "07-1 生产者源码之producer元数据管理": "http://img.kaikeba.com/07%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%85%83%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86%281%29.mp4",
    "07-2 生成者源码之producer端元数据管理": "http://img.kaikeba.com/07%20%E7%94%9F%E6%88%90%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E7%AB%AF%E5%85%83%E6%95%B0%E6%8D%AE%E7%AE%A1%E7%90%86%282%29.mp4",
    "08-1 生产者源码之producer源码核心流程初探": "http://img.kaikeba.com/08%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E6%BA%90%E7%A0%81%E6%A0%B8%E5%BF%83%E6%B5%81%E7%A8%8B%E5%88%9D%E6%8E%A2%281%29.mp4",
    "08-2 生产者之producer源码核心流程初探": "http://img.kaikeba.com/08%20%E7%94%9F%E4%BA%A7%E8%80%85%E4%B9%8Bproducer%E6%BA%90%E7%A0%81%E6%A0%B8%E5%BF%83%E6%B5%81%E7%A8%8B%E5%88%9D%E6%8E%A2%282%29.mp4",
    "09-1 生产者源码之producer加载元数据": "http://img.kaikeba.com/09%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%8A%A0%E8%BD%BD%E5%85%83%E6%95%B0%E6%8D%AE%281%29.mp4",
    "09-2 生产者源码之producer加载元数据": "http://img.kaikeba.com/09%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%8A%A0%E8%BD%BD%E5%85%83%E6%95%B0%E6%8D%AE%282%29.mp4",
    "09-3 生产者源码之producer加载元数据": "http://img.kaikeba.com/09%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%8A%A0%E8%BD%BD%E5%85%83%E6%95%B0%E6%8D%AE%283%29.mp4",
    "09-4 生成者源码之producer加载元数据": "http://img.kaikeba.com/09%20%E7%94%9F%E6%88%90%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E5%8A%A0%E8%BD%BD%E5%85%83%E6%95%B0%E6%8D%AE%284%29.mp4",
    "10 生产者源码之分区选择": "http://img.kaikeba.com/10%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%88%86%E5%8C%BA%E9%80%89%E6%8B%A9.mp4",
    "11-1 生产者源码之recordaccumulator封装消息流程初探": "http://img.kaikeba.com/11%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Brecordaccumulator%E5%B0%81%E8%A3%85%E6%B6%88%E6%81%AF%E6%B5%81%E7%A8%8B%E5%88%9D%E6%8E%A2%281%29.mp4",
    "11-2 生产者源码之recordaccumulator封装消息流程初探": "http://img.kaikeba.com/11%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Brecordaccumulator%E5%B0%81%E8%A3%85%E6%B6%88%E6%81%AF%E6%B5%81%E7%A8%8B%E5%88%9D%E6%8E%A2%282%29.mp4",
    "12 生产者源码之copyonwritemap数据结构使用": "http://img.kaikeba.com/12%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bcopyonwritemap%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%BD%BF%E7%94%A8.mp4",
    "13 生产者源码之把数据写到对应批次(分段加锁)": "http://img.kaikeba.com/13%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E6%8A%8A%E6%95%B0%E6%8D%AE%E5%86%99%E5%88%B0%E5%AF%B9%E5%BA%94%E6%89%B9%E6%AC%A1%28%E5%88%86%E6%AE%B5%E5%8A%A0%E9%94%81%29.mp4",
    "14 生产者之内存池设计": "http://img.kaikeba.com/14%20%E7%94%9F%E4%BA%A7%E8%80%85%E4%B9%8B%E5%86%85%E5%AD%98%E6%B1%A0%E8%AE%BE%E8%AE%A1.mp4",
    "15 生产者源码之sender线程运行流程初探": "http://img.kaikeba.com/15%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bsender%E7%BA%BF%E7%A8%8B%E8%BF%90%E8%A1%8C%E6%B5%81%E7%A8%8B%E5%88%9D%E6%8E%A2.mp4",
    "16 生产者源码之一个batch什么条件下可以发送": "http://img.kaikeba.com/16%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E4%B8%80%E4%B8%AAbatch%E4%BB%80%E4%B9%88%E6%9D%A1%E4%BB%B6%E4%B8%8B%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%EF%BC%9F.mp4",
    "17-1 生产者源码之筛选可以发送消息的broker": "http://img.kaikeba.com/17%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%B8%85%E9%80%89%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF%E7%9A%84broker%281%29.mp4",
    "17-2 生产者源码之筛选可以发送消息的broker": "http://img.kaikeba.com/17%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E7%AD%9B%E9%80%89%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF%E7%9A%84broker%282%29.mp4",
    "18-1 生产者源码之kafka网络设计": "http://img.kaikeba.com/18%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bkafka%E7%BD%91%E7%BB%9C%E8%AE%BE%E8%AE%A1%281%29.mp4",
    "18-2 生产者源码之kafka网络设计-错误更正": "http://img.kaikeba.com/18%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bkafka%E7%BD%91%E7%BB%9C%E8%AE%BE%E8%AE%A1-%E9%94%99%E8%AF%AF%E6%9B%B4%E6%AD%A3%282%29.mp4",
    "18-3 生产者源码之kafka网络设计": "http://img.kaikeba.com/18%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bkafka%E7%BD%91%E7%BB%9C%E8%AE%BE%E8%AE%A1%283%29.mp4",
    "19 生产者源码之如果网络没有建立好会发送消息吗": "http://img.kaikeba.com/19%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%A6%82%E6%9E%9C%E7%BD%91%E7%BB%9C%E6%B2%A1%E6%9C%89%E5%BB%BA%E7%AB%8B%E5%A5%BD%E4%BC%9A%E5%8F%91%E9%80%81%E6%B6%88%E6%81%AF%E5%90%97%EF%BC%9F.mp4",
    "20-1 生产者源码之producer终于要与broker建立连接了": "http://img.kaikeba.com/20%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E7%BB%88%E4%BA%8E%E8%A6%81%E4%B8%8Ebroker%E5%BB%BA%E7%AB%8B%E8%BF%9E%E6%8E%A5%E4%BA%86%21%281%29.mp4",
    "20-2 生成者源码之producer终于要与broker建立连接了": "http://img.kaikeba.com/20%20%E7%94%9F%E6%88%90%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E7%BB%88%E4%BA%8E%E8%A6%81%E4%B8%8Ebroker%E5%BB%BA%E7%AB%8B%E8%BF%9E%E6%8E%A5%E4%BA%86%21%EF%BC%882%EF%BC%89.mp4",
    "20-3 生产者源码之producer终于要与broker建立连接了": "http://img.kaikeba.com/20%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E7%BB%88%E4%BA%8E%E8%A6%81%E4%B8%8Ebroker%E5%BB%BA%E7%AB%8B%E8%BF%9E%E6%8E%A5%E4%BA%86%EF%BC%81%283%29.mp4",
    "21-1 生产者源码之生产者终于可以发送网络请求了": "http://img.kaikeba.com/21%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E7%94%9F%E4%BA%A7%E8%80%85%E7%BB%88%E4%BA%8E%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E7%BD%91%E7%BB%9C%E8%AF%B7%E6%B1%82%E4%BA%86%EF%BC%81%EF%BC%81%EF%BC%881%EF%BC%89.mp4",
    "21-2 生产者源码之生产者终于可以发送请求了": "http://img.kaikeba.com/21%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E7%94%9F%E4%BA%A7%E8%80%85%E7%BB%88%E4%BA%8E%E5%8F%AF%E4%BB%A5%E5%8F%91%E9%80%81%E8%AF%B7%E6%B1%82%E4%BA%86%EF%BC%81%EF%BC%81%282%29.mp4",
    "22-1 生产者源码之producer是如何处理粘包问题的": "http://img.kaikeba.com/22%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E6%98%AF%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E7%B2%98%E5%8C%85%E9%97%AE%E9%A2%98%E7%9A%84%281%29.mp4",
    "22-2 生产者源码之producer是如何处理粘包问题的": "http://img.kaikeba.com/22%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E6%98%AF%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E7%B2%98%E5%8C%85%E9%97%AE%E9%A2%98%E7%9A%84%282%29.mp4",
    "23 生产者源码之producer是如何处理拆包问题的": "http://img.kaikeba.com/23%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8Bproducer%E6%98%AF%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E6%8B%86%E5%8C%85%E9%97%AE%E9%A2%98%E7%9A%84.mp4",
    "24 生产者源码之如何处理暂存状态的响应": "http://img.kaikeba.com/24%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E6%9A%82%E5%AD%98%E7%8A%B6%E6%80%81%E7%9A%84%E5%93%8D%E5%BA%94.mp4",
    "25 生产者源码之如何处理响应消息": "http://img.kaikeba.com/25%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E5%93%8D%E5%BA%94%E6%B6%88%E6%81%AF.mp4",
    "26 生产者源码之消息发送完了以后内存如何处理": "http://img.kaikeba.com/26%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E6%B6%88%E6%81%AF%E5%8F%91%E9%80%81%E5%AE%8C%E4%BA%86%E4%BB%A5%E5%90%8E%E5%86%85%E5%AD%98%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86.mp4",
    "27 生产者源码之消息有异常是如何处理的": "http://img.kaikeba.com/27%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E6%B6%88%E6%81%AF%E6%9C%89%E5%BC%82%E5%B8%B8%E6%98%AF%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E7%9A%84.mp4",
    "28 生产者源码之如何处理超时的批次": "http://img.kaikeba.com/28%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E8%B6%85%E6%97%B6%E7%9A%84%E6%89%B9%E6%AC%A1.mp4",
    "29 生产者源码之如何处理长时间没有接受到响应的消息": "http://img.kaikeba.com/29%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E5%A6%82%E4%BD%95%E5%A4%84%E7%90%86%E9%95%BF%E6%97%B6%E9%97%B4%E6%B2%A1%E6%9C%89%E6%8E%A5%E5%8F%97%E5%88%B0%E5%93%8D%E5%BA%94%E7%9A%84%E6%B6%88%E6%81%AF.mp4",
    "30 生产者源码之生产者源码精华总结": "http://img.kaikeba.com/30%20%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E4%B9%8B%E7%94%9F%E4%BA%A7%E8%80%85%E6%BA%90%E7%A0%81%E7%B2%BE%E5%8D%8E%E6%80%BB%E7%BB%93.mp4",
}


def download(name, url):
    r = requests.get(url, stream=True)
    with open(name, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    return f'name={name}, url={url}'


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as exector:
        todo_list = [exector.submit(download, f'{name}.mp4', url) for name, url in data.items()]

        for future in as_completed(todo_list):
            try:
                print(future.result())
            except Exception as e:
                print(e)
