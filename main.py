# TODO:
#  1 设置夜间自动回复
#  2.动态添加自动回复机器人的白名单 黑名单    完成
#  3.增加新的api功能
#  4.增加早晨天气播报功能

from chat_robot import sendMessage
from auto_reply_roles import Role
import itchat
import os
import configparser
import pymysql
import threading
import datetime
import time
import json


config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
conf = configparser.ConfigParser()
conf.read(config_path)
host = conf.get('weather_db', 'host')
user = conf.get('weather_db', 'user')
password = conf.get('weather_db','passwd')
database = conf.get('weather_db', 'database')
print(host, user, password, database)
conn = pymysql.connect(host=host, user=user, password=password, database=database)
cursor = conn.cursor()

base_dir = os.path.join( os.path.dirname(os.path.realpath(__file__)),  'forecast_names.json')

@itchat.msg_register(itchat.content.TEXT)
def auto_reply(msg):
    """腾讯闲聊机器人的自动回复"""
    if msg['ToUserName'] == 'filehelper':
        print(msg['ToUserName'], msg.fromUserName, msg.text)
        if '白名单' in msg.text:
            name = msg.text.replace(' 白名单', '')
            Role().add_name(name)
        elif '黑名单' in msg.text:
            name = msg.text.replace('黑名单', '')
            Role().del_name(name)
        else:
            itchat.send_msg(sendMessage(msg.text), toUserName='filehelper')
    else:
        friend = itchat.search_friends(userName=msg.fromUserName)
        print(friend['RemarkName'], msg.fromUserName, msg.text)
        if Role().in_white_names(friend['RemarkName']):
            answer = sendMessage(msg.text)
            answer += '♈'
            friend.send(answer)


def run_reply():
    print('开启自动回复')
    itchat.run()

def rum_timer():
    print('开始天气定时播报')
    # name_dic = {'林林': '南京',
    #             '老妈': '五台山',
    #             '老爹': '鄂托克旗',
    #             # '我':'西安',
    #              }
    while True:
        try:
            with open(base_dir, 'r', encoding='utf-8')as f:
                name_dic = json.loads(f.read(), encoding='utf-8')
            now = datetime.datetime.now()
            hour = now.time().hour
            if hour == 18:
                for key in name_dic.keys():
                    tomorrow_sql = """select city,days_2,publish_time from weather where city='{0}' 
                                      order by publish_time DESC limit 1""".format(name_dic[key])
                    cursor.execute(tomorrow_sql)
                    rows = cursor.fetchall()
                    forecast = eval(rows[0][1])
                    msg = name_dic[key] + ' 明天的天气预报如下：' + forecast['day_info'] + ' ' + forecast['day_winddirect'] \
                          + forecast['day_power'] + ' ' + forecast['day_temp'] + '(白天最高)/'+ forecast['night_temp'] + \
                          '(夜间最低)' + '\n' + '中央气象局：' + str(rows[0][2])
                    print(msg)
                    # itchat.send_msg(msg, toUserName='filehelper')
                    if key == '我':
                        friend = itchat.search_friends(remarkName='林林')[0]
                    else:
                        friend = itchat.search_friends(remarkName=key)[0]
                    # print(friend['RemarkName'])
                    friend.send(msg)
            time.sleep(60*60*24)
        except Exception as err:
            print(err, datetime.datetime.now())
            time.sleep(60*60*24)


if __name__ == '__main__':
    # itchat.auto_login(hotReload=True, enableCmdQR=True)
    itchat.auto_login(hotReload=True)
    # itchat.auto_login()
    t2 = threading.Thread(target=rum_timer)
    t1 = threading.Thread(target=run_reply)
    t1.start()
    t2.start()
    # itchat.run()


