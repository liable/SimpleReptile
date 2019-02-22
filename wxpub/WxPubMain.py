# -*- coding=utf-8 -*-
"""
  @author: laibo
  @time: 2019-02-22 21:45
"""
# -*- coding=utf-8 -*-
import itchat
from news_source.RequestNews import RequestNews
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


# 注册消息，监听消息
# @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        if msg['User']['NickName'] == '七人成行' and '新闻' in str(msg['Text']):
            if msg['ActualNickName'] == '邹碧林':
                itchat.send_msg(RequestNews.get_zaobao_news(), toUserName=msg['FromUserName'])
            else:
                itchat.send_msg('%s长得太丑，不给看新闻。' %(msg['ActualNickName']), toUserName=msg['FromUserName'])

@scheduler.scheduled_job('cron', hour=10,minute=0,second=0)
def auto_send_news():
    print('开始推送新闻内容到7人成行微信群')
    itchat.send_msg(RequestNews.get_zaobao_news(), toUserName='@@ff46a40770f52d1020ab445bd4393be99c63cf31af86ca03ee1765e2ffe57b6b')
    '''
    每天早上10点发送新闻到微信群
    '''

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
    # friends = itchat.get_friends(update=True)[1:]
    # toUserName = [f['NickName'] for f in friends]
    # print(toUserName)
    scheduler.start()
