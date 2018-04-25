# -*- coding: UTF-8 -*-
# __author__ = 'leyex@seeapp.com'
# __file_name__ = 'views'

import hashlib
import random
import time
import os
import sys
import requests
import urllib
import urllib2
import re
import traceback
import json
from config.CustomReply import CustomReplyDict
from app import app, logger
from lxml import etree
from flask import Flask, request, render_template

reload(sys)
sys.setdefaultencoding("UTF-8")
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))


@app.route('/')
def test():
    return '<h1>test</h1>'


@app.route('/weixin', methods=['GET', 'POST'])
def weixinInterface():
    if request.method == 'POST':
        # 获取POST信息
        str_xml = request.data
        # 进行XML解析
        xml = etree.fromstring(str_xml)

        # 获取用户所输入内容
        content = xml.find("Content").text
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text

        voice_mark = False  # 语音标示

        num_mark = False

        # 鹦鹉学舌
        return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                               content=u"抱歉，功能正在开发中，您刚才所说的是：【%s】 \n感谢您的支持，谢谢！" % content)

        helplist = [u"来咯，客官，小四这厢有礼了", \
                    u"轻轻地，我来了，然后我又轻轻的走了，哈哈" \
                    ]
        CustomReply = CustomReplyDict

        welcomeText = u"✌㊤㊤㊦㊦㊧㊨㊧㊨BABA✌\n\
❤=====================\n\
  1.通过文字或语音跟小四吹吹水，聊聊天\n\
  2.问我某个城市的天气\n\
  3.问我一些菜的做法\n\
  4.输入“查快递”+“快递单号”查询快递信息\n\
  5.咨询铁路信息\n\
  6.输入“查手机”+“手机号码”查询号码归属地信息\n\
  7.让我翻译一些简单的句子或者词汇\n\
  8.回复“谁是卧底”，可与您的小伙伴一起玩谁是卧底的游戏\n\
  9.回复“开始成语接龙”，可与小四一起玩成语接龙的游戏\n\
  10.回复“猜猜”/“谜语”/“歇后语”/“脑筋急转弯”，小四跟你玩猜一猜游戏(已下线)\n\
  11.回复“今天股市怎么样”，给你一个买卖定向（纯属娱乐，切勿当真O(∩_∩)O）\n\
  更多精彩敬请期待...\n\
❤====================="

        # 语音识别
        if msgType == "voice":
            voice_mark = True
        if msgType == "text" or voice_mark:
            if voice_mark:
                content = xml.find("Recognition").text[:-1]
                # return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=content)
            else:
                content = xml.find("Content").text.lower()

            for i in CustomReplyDict:
                if i in content:
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()), content=CustomReplyDict[i])

            # 尝试转换数字
            try:
                num_mark = int(content.strip())
            except:
                pass
                # return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=traceback.format_exc())

            # 天气预报
            '''if u"天气" in content or u"气候" in content or u"温度" in content or u"气温" in content:
                segment = segment_sae(content.strip(), 102)
                if segment:
                    weather = getWeather(segment)
                    if weather[0] != -1:
                        return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=weather[1])
                else:
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=u"你是问我哪个城市的天气啊")'''

            # 翻译
            if u"翻译" in content:
                word = content.split(u"翻译", 1)
                if len(word) >= 2 and word[1]:
                    replyText = youdao(word[1].encode("UTF-8", "ignore"))
                else:
                    replyText = u"你需要我翻译什么呢"
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)
                """except:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),traceback.format_exc())"""

            # 谁是卧底
            if num_mark:
                try:
                    replyText = sswd.Judge(fromUser).createRoom(num_mark)
                except:
                    replyText = traceback.format_exc()
                render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                content=replyText)

            # 回复帮助信息
            if content.lower() in ["help", u"帮助", "?", u"？"]:
                replyText = random.choice(helplist) + u"\n功能仍在开发中，客官现在可以进行以下操作（支持“语音/文字”）:\n" + welcomeText
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            # 猜一猜游戏
            # elif content in [u'猜猜',u'谜语',u'歇后语',u'脑筋急转弯']:
            #     replyText = guessGame()
            #     return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=replyText)

            # 股市预测
            elif content == u"今天股市怎么样":
                stockguess = {0: u"经我小四夜观天象，感觉股市无需担心，持续持股，逢低入，勿追高\n☞☞☞☞买买买",
                              1: u"经我小四夜观天象，预测股市风云又起，前高附近有压力\n☞☞☞☞淡定观望",
                              2: u"经我小四夜观天象，预测股市风云又起，逢高出，勿贪\n☞☞☞☞卖卖卖"}
                result = random.randint(0, 2)
                replyText = stockguess[result]
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            # getOpenid
            elif content == "get-userid":
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=str(fromUser))
            # getToken
            # elif content == "get-token":
            #     access_token = self.createMenu(typ = "getToken")
            #     return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=str(access_token))
            # 谁是卧底
            elif content == u"谁是卧底":
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=fromUser)
                try:
                    replyText = sswd.Judge(fromUser).OnInit()
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()), content=replyText)
                except:
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()), content=traceback.format_exc())

            elif content == u"换":
                replyText = sswd.Judge(fromUser).changeWord()
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            elif u"改" in content:
                replyText = ""
                if u":" in content and u";" in content:
                    wordlist = content.split(u":")[1].split(u";", 1)
                if u"：" in content and u"；" in content:
                    wordlist = content.split(u"：")[1].split(u"；", 1)
                if wordlist:
                    if len(wordlist) == 2:
                        replyText = sswd.Judge(fromUser).changeWord(wordlist)
                if not replyText:
                    replyText = u"请以如下格式回复：\"改:单词1;单词2\";\n词与词之间用\";\"间隔"

                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            elif content == u"退出" or content == u"退房":
                replyText = sswd.Judge(fromUser).quit()
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            elif content == u"查房":
                try:
                    replyText = sswd.Judge(fromUser).checkRoom()
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()), content=replyText)
                except:
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()), content=traceback.format_exc())

            elif content.startswith(u"#"):
                try:
                    roomid = int(content.strip().split(u"#")[1])
                    replyText = sswd.People(fromUser).joinIn(roomid)
                except:
                    replyText = u"吃饭睡觉打豆豆"
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            # 查手机归属地
            elif content.startswith(u"查手机"):
                replyText = getPhone(content[4:].strip())
                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)

            # 回复热门新闻
            # elif u"新闻" in content or u"资讯" in content:
            #     try:
            #         if u"体育" in content:
            #             info = getNews("tiyu")
            #         elif u"国际" in content:
            #             info = getNews("world")
            #         elif u"科技" in content:
            #             info = getNews("keji")
            #         elif u"健康" in content:
            #             info = getNews("health")
            #         elif u"有趣" in content:
            #             info = getNews("qiwen")
            #         else:
            #             info = getNews("social")
            #         if info:
            #             return render_template("reply_news_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), infolist=info, titlelist=['title','description','picUrl','url'])
            #         else:
            #             return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=u"敬请期待")
            #     except:
            #         return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()), content=u"出错了，等主人来修复")  # traceback.format_exc()
            else:
                content = content.encode("UTF-8")
                replyText = tuling(content, fromUser)
                try:
                    result_type = replyText["results"][0]["resultType"]
                except:
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()),
                                           content=json.dumps(replyText, ensure_ascii=False))

                if result_type == "text":
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()),
                                           content=replyText["results"][0]["values"]["text"])
                else:
                    return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                           createTime=int(time.time()),
                                           content=json.dumps(replyText, ensure_ascii=False))
                    infolist = [replyText["results"][i] for i in range(len(replyText["results"])) if i <= 5]
                    if result_type == 'url':
                        infolist = [replyText["results"][i] for i in replyText["results"] if i <= 5]
                        titlelist = ['name', 'info', 'icon', 'detailurl']
                    # 新闻
                    elif result_type == 302000:
                        titlelist = ['article', 'source', 'icon', 'detailurl']
                    # 列车信息
                    elif result_type == 305000:
                        return render_template("reply_train_text.xml", fromUser=toUser, toUser=fromUser,
                                               createTime=int(time.time()), infolist=infolist)
                    try:
                        return render_template("reply_pic_text.xml", fromUser=toUser, toUser=fromUser,
                                               createTime=int(time.time()), infolist=infolist, titlelist=titlelist)
                    except:
                        return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser,
                                               createTime=int(time.time()), content=traceback.format_exc())

        # 识别订阅信息
        elif msgType == "event":
            eventType = xml.find("Event").text
            if eventType == "subscribe":
                replyText = u"感谢关注四次元生活帮，希望我们能给您的生活多一份便捷。由于目前正处开发过程中，功能暂不完善，请多多包含，文字/语音输入“help”或“帮助”可获取更多信息，Thanks！\n" + welcomeText

                return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                       content=replyText)
        # 识别图片
        elif msgType == "image":
            return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                   content=u"欺负我看不到图片，可恶！")
        else:
            return render_template("reply_text.xml", fromUser=toUser, toUser=fromUser, createTime=int(time.time()),
                                   content=u"别老发些我不懂的！")

    # Get请求
    # 获取输入参数
    signature = request.args['signature']
    timestamp = request.args['timestamp']
    nonce = request.args['nonce']
    echostr = request.args['echostr']
    # 自己的token
    token = "siciyuan_shb"  # 这里填写公众平台输入的token
    # 字典排序
    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    # sha1加密算法
    hashcode = sha1.hexdigest()

    # 如果是来自微信的请求，则回复echostr
    if hashcode == signature:
        logger.info('{} == {} >> {}'.format(hashcode, signature, hashcode == signature))
        return echostr


# 分词
def segment_sae(chinese_text, word_tag):
    status = False
    _SEGMENT_BASE_URL = "http://simonfenci.sinaapp.com/index.php?key=simon&wd=%s" % urllib.quote(
        chinese_text.encode("UTF-8"))
    html = urllib2.urlopen(_SEGMENT_BASE_URL).read()
    wordlist = re.findall(r"\[word\] =\> (.+)", html)
    taglist = re.findall(r"\[word_tag\] =\> (\d+)", html)
    for eachword, eachtag in map(None, wordlist, taglist):
        if int(eachtag) == int(word_tag):
            status = eachword
            break
    return status


# 百度API
def getAPI_byjson(url):
    req = urllib2.Request(url)
    req.add_header("apikey", "0e80cd63857111c8f8695188314df854")
    resp = urllib2.urlopen(req)
    content = resp.read()
    if content:
        result = json.loads(content)
        return result
    else:
        return False


def guessGame():
    url = 'http://apis.baidu.com/myml/c1c/c1c?id=-1'
    info = getAPI_byjson(url)
    return info['Answer'] + (u'\n☝' + '\t'*22 + '☝') * 25 + '\n' + info['Title']


# 获取天气预报
def getWeather(city):
    status = -1
    data = "None"
    url = 'http://apis.baidu.com/heweather/weather/free?city=%s' % urllib.quote(city)
    result = getAPI_byjson(url)
    # print result
    try:
        data = result[u"HeWeather data service 3.0"]
        if data:
            content = data[0]
            if content['status'] == u"ok":
                status = 0
                data = u'【小四为您播报】\n城市:%s\n发布时间:%s\n天气情况:%s\n气温:%s℃\n舒适度指数:%s\n穿衣指数:%s' % (
                content["basic"]["city"], content["basic"]["update"]["loc"], content["now"]["cond"]["txt"],
                content["now"]["tmp"], content["suggestion"]["comf"]["txt"], content["suggestion"]["drsg"]["txt"])
                try:
                    weather_sp = content["alarms"]
                    data = data + "\n\n灾害预警：%s\n状态：%s\n【%s】" % (
                    weather_sp["title"], weather_sp["stat"], weather_sp["txt"])
                except:
                    pass
    except:
        pass
    return status, data


# 不准
def getWeather1(city):
    status = -1
    data = "None"
    url = 'http://apis.baidu.com/apistore/weatherservice/citylist?cityname=%s' % urllib.quote(city.encode("UTF-8"))
    result = getAPI_byjson(url)
    if result:
        data = result["retData"]
        if data:
            city_en = result["retData"][0]["name_en"]
            url = 'http://apis.baidu.com/apistore/weatherservice/weather?citypinyin=%s' % city_en
            result = getAPI_byjson(url)
            data = str(result)
            status = 0
            content = result["retData"]
            data = u'城市:%s\n发布时间:%s\n天气情况:%s\n气温:%s℃\n温差:%s°/%s°' % (
            city, content["time"], content["weather"], content["temp"], content["h_tmp"], content["l_tmp"])

    return status, data


# 小黄鸡API
def xiaohuangji(word):
    resultlist = [u"我不懂我不懂，我还小，为什么要这样逼我",
                  u"淡定淡定，这个问题我回去问我老大",
                  u"你老说我这些有的没有的，我要去告诉我老大，你别走",
                  u"别整这些有的没的，我们决斗吧",
                  u"这个只有老天知道了"
                  ]
    try:
        qword = urllib2.quote(word)
        url = "http://www.simsimi.com/requestChat?lc=ch&ft=1.0&req=%s" % qword
        page = urllib2.urlopen(url)
        html = json.loads(page.read())
        result = html["res"]
        if result.startswith(u"I HAVE NO RESPONSE"):
            result = random.choice(resultlist)
        return result
    except:
        youdao(word)


# 图灵机器人
def tuling(word, openid=""):
    url = "http://openapi.tuling123.com/openapi/api/v2"
    apiKey = "904e87c51e5f43ee9f09de692563f1f7"
    post_data = {
        "perception": {
            "inputText": {
                "text": word
            },
            "selfInfo": {
                "location": {
                    "city": "深圳",
                    "latitude": "39.45492",
                    "longitude": "119.239293",
                    "nearest_poi_name": "上地环岛南",
                    "province": "北京",
                    "street": "信息路"
                }
            }
        },
        "userInfo": {
            "apiKey": apiKey,
            "userId": sum(map(ord, openid)) if openid else 111
        }
    }
    result = requests.post(url, json=post_data).json()

    result_code = result["intent"]["code"]
    if result_code in [308000, 302000, 305000]:
        return result
    if result_code >= 10000:
        return result
    else:
        return xiaohuangji(word)


# 二维码获取
def getQr(openid=""):
    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=TOKEN"
    post_data = {"expire_seconds": 604800, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": 123}}}


# 手机号码归属地
def getPhone(phoneNum):
    url = 'http://apis.baidu.com/apistore/mobilephoneservice/mobilephone?tel=%s' % phoneNum.strip()
    info = getAPI_byjson(url)
    if info['errNum'] == 0:
        return u"手机号码：%s\n归属地：%s - %s\n运营商：%s" % (
        info['retData']['phone'], info['retData']['province'], info['retData']['city'], info['retData']['supplier'])
    else:
        return u'小四不认识这个手机号码:%s' % phoneNum


# 新闻
def getNews(category):
    url = "http://apis.baidu.com/txapi/%s/%s?num=5&page=1" % (category, category)
    info = getAPI_byjson(url)
    if info[u'code'] == 200:
        del (info[u'code'])
        del (info[u'msg'])
        return info
    else:
        return False


# 有道翻译API
def youdao(word):
    qword = urllib2.quote(word)
    url = "http://fanyi.youdao.com/openapi.do?keyfrom=Pythonpush&key=1098322410&type=data&doctype=json&version=1.1&q=%s" % qword
    page = urllib2.urlopen(url)
    html = page.read()
    page.close()
    result = json.loads(html)
    # return result
    if result['errorCode'] == 0:
        if "basic" in result.keys():
            trans = u'%s:\n%s\n%s\n网络释义：\n%s' % (
            result['query'], ''.join(result['translation']), ''.join(result['basic']['explains']),
            ''.join(result['web'][0]['value']))
        else:
            trans = u'%s:\n%s' % (result['query'], ''.join(result['translation']))
        return trans
    elif result['errorCode'] == 20:
        return u'对不起，要翻译的文本过长'
    elif result['errorCode'] == 30:
        return u'对不起，无法进行有效的翻译'
    elif result['errorCode'] == 40:
        return u'对不起，不支持的语言类型'
    else:
        return u'对不起，您输入的单词%s无法翻译,请检查拼写' % word
