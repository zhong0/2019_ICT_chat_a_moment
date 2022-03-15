# 療一下－聊天陪伴檢測心靈AI

Demo Video: https://youtu.be/q21peUzfRBU

專案內容
----
* ### 對話陪伴
* ### 情緒分析
* ### 寵物互動

技術說明
----
* ### 資料庫
  >使用NoSql資料庫，使其容納較多且複雜的資料格式，以Mongo DB官方釋出映像檔建立Docker於伺服器，依照指令建置資料庫。由於是非關連式資料庫，只需簡單設計欄位，例如量表問題、情緒初始分數等，作為新增使用者時，所產生的初始資料。

* ### 資料傳遞
  >以php作為靜態資料的傳遞，例如使用者身份、情緒長期分數等，並利用php-apache之映像檔建立Docker，作為對接窗口。Mongo DB指令編寫於php檔案中，並以POST接收Android端之資料，進而達成查詢、更新、刪除資料之操作。相關操作後，若要回傳至Android端，將資料包裝成Json格式，以echo回傳至Android端。此外，python作為即時資料的傳遞橋樑，例如面部、對話情緒辨識，並以含有python之映像檔建立Docker，接收使用端之資訊，進而更新資料庫資料。

* ### 對話辨識與產生
  >本專案有語音對話及文字對話，語音對話是利用Speech-to-Text API於Android Studio內轉換成文字，再進行文字辨識。在辨識語句的過程，利用python讀取Rule-based內容，其包含儲存Rule之txt檔及詞彙內容之xls檔，判斷該內容的核心事件，再以decision tree決策接下來的對話內容，其依照認知行為治療(Cognitive Behavior Therapy, CBT)程序推進對話的產生，而產生的過程也是利用Rule-based產生句子。在對話過程中，主要判斷事件、情緒、時間、對象，其中情緒會納入情緒分析之分數內。

* ### 面部情緒辨識
  >將Open CV模組匯入Android檔案內，使用手機前置鏡頭擷取圖片回傳至Python模型達成面部情緒辨識，為壓縮圖檔大小及縮短辨識時間，我們將鏡頭所拍攝的彩色圖片，轉換成黑白圖片再做辨識。其功能於語音聊天過程當中，會不斷偵測當前情緒，並將偵測結果從Android傳至Python計算，最後回傳至Mongo DB紀錄。

* ### 穿戴裝置
  >我們使用研鼎智能GoLife Care-X HR手環協助本專案偵測生理狀況，包含心跳、消耗卡路里、行走距離，以衡量長期活動量，進而評估其情緒狀態。將其公司所開發之SDK匯入Android檔案，應用於本專案當中。

* ### 使用者介面
  >本專案首頁之寵物互動為Unity開發，其餘以Android Studio開發。（將Unity相關之library import至Android檔案，並以aar檔案格式打包Unity開發內容。）Android以XML繪製Layout，Java編寫介面操作，其包含CardView、RecyclerView、Camera、LineChart等，並嵌入Open CV Module、Unity Library、GoLife Care SKD，結合多功能於使用者端，以Volley Library傳接資料，利用Gson於Java語言中接收來自php的Json格式的資料。
  

環境設置
----
* ### Database
* ### php
* ### rule-based
* ### face detection
* ### android

補充說明
----
* ### document
