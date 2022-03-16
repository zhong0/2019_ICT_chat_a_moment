# 療一下－聊天陪伴檢測心靈AI

Demo Video: https://youtu.be/q21peUzfRBU
* 2019大專校院資訊應用服務創新競賽佳作：資訊應用組
* 2019大專校院資訊應用服務創新競賽入圍：AWS雲端科技趨勢應用組

專案內容
----
* ### 對話陪伴
  >本專案期望達到使用者能隨時傾訴心情，使其掌握自身情緒狀況外，也期望達成療癒效果，因此，我們以認知行為治療(Cognitive Behavior Therapy, CBT)程序作為聊天架構，一步步了解使用者對於傾訴事件的情緒與想法，並自動產生偵測到之事件紀錄，包含事件、發生時間、情緒、對象關係，作為後續回顧調整。

* ### 情緒分析
  >情緒分析分為短期追蹤及長期追蹤，短期追蹤為在聊天過程當中偵測開心、難過、憤怒、恐懼、厭惡五大情緒字眼，又因複雜情緒於文字聊天不易解讀，所以，開發語音功能搭配前置鏡頭進行面部情緒偵測，最終統整結果以圓餅圖呈現給使用者查看；長期追蹤則有焦慮傾向、憂鬱傾向數值顯現，在聊天過程當中，除了會偵測情緒字眼、負向扭曲言論之外，也會不時提出焦慮、憂鬱量表內容，追蹤使用者狀況，並利用手環生理偵測，以長期追蹤心跳、卡路里、行走距離數據，同步於本系統當中，協助完成情緒分析。

* ### 寵物互動
  >本專案亦添加寵物互動元素讓使用者能有更多陪伴感。互動包含：拖曳、點擊、餵食等使用者可以進行的操作，也有寵物本身自動的動作如：跳躍、走動、搖擺等。而寵物也有自身的情緒，當使用者太久沒與寵物互動或與聊天機器人聊天會讓寵物的情緒越來低落，寵物表情亦會受到影響，以上設計目的是希望能展現活生生的表現以及讓使用者多多使用聊天陪伴功能，以增加使用黏著性。

技術說明
----
* ### 資料庫
  >使用NoSql資料庫，使其容納較多且複雜的資料格式，以Mongo DB官方釋出映像檔建立Docker於伺服器，依照指令建置資料庫。由於是非關連式資料庫，只需簡單設計欄位，例如量表問題、情緒初始分數等，作為新增使用者時，所產生的初始資料。

* ### 資料傳遞
  >以php作為靜態資料的傳遞，例如使用者身份、情緒長期分數等，並利用php-apache之映像檔建立Docker，作為對接窗口。Mongo DB指令編寫於php檔案中，並以POST接收Android端之資料，進而達成查詢、更新、刪除資料之操作。相關操作後，若要回傳至Android端，將資料包裝成Json格式，以echo回傳至Android端。此外，python作為即時資料的傳遞橋樑，例如面部、對話情緒辨識，並以含有python環境的Docker，接收使用端的資訊，進而利用Socket方法連接並更新資料庫資料。

* ### 對話辨識與產生
  >本專案有語音對話及文字對話，語音對話是利用Speech-to-Text API於Android Studio內轉換成文字，再進行文字辨識。在辨識語句的過程，利用python讀取Rule-based內容，其包含儲存Rule之txt檔及詞彙內容之xls檔，判斷該內容的核心事件，再以decision tree決策接下來的對話內容，其依照CBT程序推進對話的產生，而產生的過程也是利用Rule-based產生句子。在對話過程中，主要判斷事件、情緒、時間、對象，其中情緒會納入情緒分析之分數內。

* ### 面部情緒辨識
  >將Open CV模組匯入Android檔案內，使用手機前置鏡頭擷取圖片回傳至Python模型達成面部情緒辨識，為壓縮圖檔大小及縮短辨識時間，我們將鏡頭所拍攝的彩色圖片，轉換成黑白圖片再做辨識，模型以tensorflow建立。其功能於語音聊天過程當中，會不斷偵測當前情緒，並將偵測結果從Android傳至Python計算，最後回傳至Mongo DB紀錄。

* ### 穿戴裝置
  >我們使用研鼎智能GoLife Care-X HR手環協助本專案偵測生理狀況，包含心跳、消耗卡路里、行走距離，以衡量長期活動量，進而評估其情緒狀態。將其公司所開發之SDK匯入Android檔案，應用於本專案當中。

* ### 使用者介面
  >本專案首頁及寵物互動介面為Unity開發，其餘以Android Studio開發。兩者結合方式為將Android Studio檔案設定為lib檔並打包為aar檔，再由Unity專案引入，最後以Unity匯出apk檔。Unity和Android Studio之間的溝通以static call方式進行參數傳遞、呼叫。Android以XML繪製Layout，Java編寫介面操作，其包含CardView、RecyclerView、Camera、PieChart等，並嵌入Open CV Module、Unity Library、GoLife Care SDK，結合多功能於使用者端，以Volley Library傳接資料，利用Gson於Java語言中接收來自php的Json格式的資料。
  

環境設置
----
* ### Database
  >本專案使用Ubuntu作業系統環境建立Docker，使用mongo官方映像檔，其資源庫及標籤名稱mongo:last，host port設定為28017，container port為其default port 27017。
  
  >指令：docker run -d -p 28017:27017 --name 28to27 mongo:latest
* ### php
  >在同一台伺服器中建立Docker，使用映像檔之資源庫及標籤名稱為php:5-apache，並連接到上述Docker，host port設定為8020，其為外部連進此Docker之port，container port設為80。接著安裝相關套件，將php檔案置入其中。
  
  >指令：docker run -d -p 8020:80 --link 28to27 --name php-mongo php:5-apache <br>

  >環境設定：
  >* apt-get install openssl libssl-dev libcurl4-openssl-dev
  >* pecl install mongo
  >* echo "extension=mongo.so" > /usr/local/etc/php/conf.d/mongo.ini

* ### rule-based
  >建立新的Docker，使用映像檔之資源庫及標籤名稱為php:5-apache，並連接到28to27 Docker，host port設定為7070，其為外部連接port，container port設為8888。接著安裝python環境及相關套件，將rule-based之相關檔案置入其中。
  
  >指令：docker run -d -p 7070:8888 --link 28to27 --name connectPython php:5-apache

  >環境設定：
  >* apt-get install python3
  >* apt-get install python3-pip
  >* pip install requests, ckip-segamentor, pandas, pymongo, xlrd

* ### face detection
  >建立新的Docker，使用映像檔之資源庫及標籤名稱為tensorflow/tensorflow:1.5.0-py3，host port設定為7072，其為外部連接port，container port設為8082，且把faceEmotionDockere綁定掛載，接著將Emotion-detection-master資料夾移至docker中，並安裝相關套件。
  
  >指令：docker run -d -v ~/faceEmotionDocker:/notebooks/faceEmoOnD -p 7072:8082 --name testTensorflow tensorflow/tensorflow:1.5.0-py3
  
  >環境設定：
  >* docker cp Emotion-detection-master/ testTensorflow:/notebooks
  >* pip install opencv-python, keras==2.2.4

* ### android
  >依照官方說明下載Android Studio，從Android Studio開啟本專案檔案，若電腦尚未下載Java需依照環境提示安裝，並同步Gradle，完成專案設定。目前本專案之雲端伺服器IP已關閉，因此，在傳接資料的網址，需更換成各自的伺服器IP。本專案設定gradle(Module:app)，minSdkVersion為23、targetSdkVersion為27。
  
  >注意：本專案只提供學術需求，若需要完整介面檔案，請傳送email至109753106@g.nccu.edu.tw，經評估後，將給予下載權限。
  
* ### unity
  >Unity環境使用Unity 2.2.2版本。

參考內容
----
* ### Real-time Facial Emotion Detection using deep learning
  >link: https://github.com/atulapra/Emotion-detection.git

補充說明
----
* ### document
  >document資料夾含有2019大專校院資訊應用服務創新競賽初賽文件、複賽海報及簡報，想知道更詳細內容可查看資料夾文件或是點選上述demo影片連結。
* ### 未完全部分
  >本專案經由測試後，seq2seq辨識及產生句子表現不佳，因此，最終只由rule-based方法進行對話功能。
