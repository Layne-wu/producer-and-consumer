#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Wwl

import time,random
from multiprocessing import Process,JoinableQueue
# 制作热狗
def make_hotdog(queue,name):
    for i in range(3):
        time.sleep(random.randint(1,2))
        print("%s 制作了一个热狗 %s" % (name,i))
        # 生产得到的数据
        data = "%s生产的热狗%s" % (name,i)
        # 存到队列中
        queue.put(data)
    # 装入一个特别的数据 告诉消费方 没有了
    #queue.put(None)

# 吃热狗
def eat_hotdog(queue,name):
    while True:
        data = queue.get()
        time.sleep(random.randint(1, 2))
        print("%s 吃了%s" % (name,data))
        # 该函数就是用来记录一共给消费方多少数据了 就是get次数
        queue.task_done()


if __name__ == '__main__':
    #创建队列
    q = JoinableQueue()
    p1 = Process(target=make_hotdog,args=(q,"邵钻钻的热狗店"))
    p2 = Process(target=make_hotdog, args=(q, "egon的热狗店"))
    p3 = Process(target=make_hotdog, args=(q, "老王的热狗店"))


    c1 = Process(target=eat_hotdog, args=(q,"思聪"))
    c2 = Process(target=eat_hotdog, args=(q, "李哲"))

    p1.start()
    p2.start()
    p3.start()

    # 将消费者作为主进程的守护进程
    c1.daemon = True
    c2.daemon = True


    c1.start()
    c2.start()

    # 让主进程等三家店全都做完后....
    p1.join()
    p2.join()
    p3.join()


    # 如何知道生产方生产完了 并且 消费方也吃完了

    # 方法一:等待做有店都做完热狗在放None
    # # 添加结束标志   注意这种方法有几个消费者就加几个None 不太合适 不清楚将来有多少消费者
    # q.put(None)
    # q.put(None)

    # 主进程等到队列结束时再继续  那队列什么时候算结束? 生产者已经生产完了 并且消费者把数据全取完了
    q.join()  # 已经明确生产放一共有多少数据

    # 现在 需要知道什么时候做完热狗了 生产者不知道  消费者也不知道
    # 只有队列知道

    print("主进程over")
    # 生产方不生产了 然而消费方不知道 所以一直等待  get函数阻塞
    # 三家店都放了一个空表示没热狗了  但是消费者只有两个 他们只要看见None 就认为没有了
    # 于是进程也就结束了  造成一些数据没有被处理
