#
#          ┌─┐       ┌─┐
#       ┌──┘ ┴───────┘ ┴──┐
#       │                 │
#       │       ───       │
#       │  ─┬┘       └┬─  │
#       │                 │
#       │       ─┴─       │
#       │                 │
#       └───┐         ┌───┘
#           │         │
#           │         │
#           │         │
#           │         └──────────────┐
#           │                        │
#           │                        ├─┐
#           │                        ┌─┘
#           │                        │
#           └─┐  ┐  ┌───────┬──┐  ┌──┘
#             │ ─┤ ─┤       │ ─┤ ─┤
#             └──┴──┘       └──┴──┘
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#      神獸保佑                永無 BUG
#

from flask import Flask, request, abort
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

import requests

import json

import urllib

app = Flask( __name__)

# Channel Access Token
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# Channel Secret
handler = WebhookHandler('YOUR_CHANNEL_SECRET')
# 氣象局會員授權碼
AuthCode = 'YOUR_AUTH_CODE'

# 監聽所有來自 /callback 的 Post Request
@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
            
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text[-2:] == '天氣': 
            location_name = check_location_name(event.message.text.split('天氣')[0])
            if location_name != False:
                send_weather_info(event.reply_token, location_name)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(
                    text='您似乎輸入了錯誤的縣市名，請確認後重新輸入，或輸入「/help」以獲得幫助列表。',
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(
                                action=MessageAction(label="幫助選單(/help)", text="/help")
                            )
                        ]
                    )
                ))
                
# 檢查縣市名稱
def check_location_name(location_name):
    all_list = ['基隆市', '臺北市', '新北市', '桃園市', '新竹市', '臺中市', '嘉義市', '臺南市', '高雄市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '屏東縣', '宜蘭縣', '花蓮縣', '臺東縣', '澎湖縣', '金門縣', '連江縣', '嘉義縣']
    city_list = ['基隆', '臺北', '新北', '桃園', '新竹', '臺中', '嘉義', '臺南', '高雄']
    shan_list = ['新竹', '苗栗', '彰化', '南投', '雲林', '屏東', '宜蘭', '花蓮', '臺東', '澎湖', '金門', '連江', '嘉義']
    if '台' in location_name:
        location_name = location_name.replace('台', '臺')
    if location_name in all_list:
        return location_name
    elif location_name in city_list:
        return location_name + '市'
    elif location_name in shan_list:
        return location_name + '縣'
    else:
        return Fals
            
# 傳送天氣訊息
def send_weather_info(reply_token, location_name):
    url_name = urllib.parse.quote(location_name)
    with urllib.request.urlopen("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + AuthCode + "&format=JSON&locationName=" + url_name) as url:
        data = json.loads(url.read().decode())
        start_date = data['records']['location'][0]['weatherElement'][0]['time'][0]['startTime'].split(" ")[0]
        start_time = data['records']['location'][0]['weatherElement'][0]['time'][0]['startTime'].split(" ")[1]
        end_date = data['records']['location'][0]['weatherElement'][0]['time'][0]['endTime'].split(" ")[0]
        end_time = data['records']['location'][0]['weatherElement'][0]['time'][0]['endTime'].split(" ")[1]
        status = data['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['parameterName']
        cold = data['records']['location'][0]['weatherElement'][2]['time'][0]['parameter']['parameterName']
        hot = data['records']['location'][0]['weatherElement'][4]['time'][0]['parameter']['parameterName']
        feel = data['records']['location'][0]['weatherElement'][3]['time'][0]['parameter']['parameterName']
        rain = data['records']['location'][0]['weatherElement'][1]['time'][0]['parameter']['parameterName']
        
        line_bot_api.reply_message(reply_token, TextSendMessage(text="日期(開始)：" + start_date + "\n日期(結束)：" + end_date + "\n時間(開始)：" + start_time + "\n時間(結束)：" + end_time +
        "\n最高溫：" + hot + "°C\n最低溫：" + cold + "°C\n天氣狀態：" + status + "\n感受：" + feel + "\n降雨機率：" + rain + "%"))

import os
if __name__ == "__main__":
    app.run(debug=True)
