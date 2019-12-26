# line-weather-bot
此專案為臺中二中高一學生自主學習成果，一個簡單的 LINE 天氣查詢機器人。我們使用`LINE MESSEAGING API (Python)`進行撰寫，主要內容為將取得的 json 檔案格式化、基本字串處理和嘗試調用`LINE MESSAGING API (Python)`內的函數。
## 重點程式碼
### 讀取網頁資料
```Python
urllib.request.urlopen("https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=" + AuthCode + "&format=JSON&locationName=" + url_name)
```
讀取氣象局網頁資料，以供解碼(json)使用。

※ 變數`url_name`為轉碼(URL)後的縣市名。
### 網頁資料解碼
```Python
json.loads(url.read().decode())
```
將氣象局網頁資料解碼，以供調用後傳送至用戶。

※ 變數`url`為讀取後的氣象局網頁資料。
### 回覆 LINE 用戶訊息
```Python
line_bot_api.reply_message(reply_token, TextSendMessage(text="日期(開始)：" + start_date + "\n日期(結束)：" + end_date + "\n時間(開始)：" + start_time + "\n時間(結束)：" + end_time + "\n最高溫：" + hot + "°C\n最低溫：" + cold + "°C\n天氣狀態：" + status + "\n感受：" + feel + "\n降雨機率：" + rain + "%"))
```
回覆給 LINE 用戶天氣資訊。
## 參考資料
### LINE 官方文檔
[https://developers.line.biz/en/reference/messaging-api](https://developers.line.biz/en/reference/messaging-api)
### 中央氣象局開放資料平台
[https://opendata.cwb.gov.tw/dist/opendata-swagger.html](https://opendata.cwb.gov.tw/dist/opendata-swagger.html)



