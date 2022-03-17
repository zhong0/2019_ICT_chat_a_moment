# An AI Chatbot of Metal Analysis and Accompanying

Demo Video: https://youtu.be/q21peUzfRBU
* International ICT Innovative Services Awards 2019 (IP Group) - Excellent work
* International ICT Innovative Services Awards 2019 (AWS Group) - Nominated

Introduction
----
* ### Chat for Accompanyding
  >Our project is aim to let user pour out their emotion in anytime. Users can not only understand their emotion codition but also obtain the sense of relief. However, we designed the chatting framework based on conitive behavior therapy (CBT). The chatbot would gradully figure out the user's emotion and thought for the events that they had been occurred. Moreover, the chatbot will automatically detect and record the details, such as the event, time, emotion, the relationship. The user can review their codition in the future.

* ### Emotion Analysis
  >There'are short-term and long-term tracking of emotion analysis. During the chatting, the chatbot would detect the keywords of five emotion, happiness, sadness, anger, fear, disgust, as the short-term tracking. Since it's hard to understand the complicated emotion in text, we developed the voice chatting fuction using the front camera on mobile phone to detect the emotion on face. The result will show with pie chart to users. However, the long-term tracking contains anxious and depression tendency. In addition to detecing keywords of emotion and extremely negative utterances, the anxious and depression scale quesion will be appearing during chatting. Moreover, our system combined the wristband to our system to detect pysical codition, such as heart rate, calories, walk distance and step. Based on these information, the system can track the long-term situation completely. 

* ### Virtual Pet Interaction
  >Our system designed a virtual pet to enhance the sense of accompanying. The interaction operation contains dragging, clicking, fedding, and so on. The virtual pet has the action as if the people, such as jumping, walking, swagging, etc. Moreover, it has its own emotion. When the user hasn't interacted with it for a long time, the virtual pet will be more and more depression, and can be recognized on its face. These designs are aim to let the chatbot to reflect the emotion similar to people and expect user to increasing the usage of our system.

Techniques
----
* ### Data
  >Our system is based on NoSQL database, which have the capability to contain more complicated data fromat and much data. According to the official document of Mongo DB, we ran a Docker with the official image in the server, and follow the commands to establish database. Owing to un-relational database, we just need to simply design the columns, such as scale question, initial score of emotion, etc., as the initial data when adding the new user.

* ### Data Passing
  >The php files are used as the static data passing, such as user informationo, long-term emotion score, and so on. We ran another Docker with php-apache image to do the data passing. The Mongo DB commands were written in the php files. The php files used the POST method to receive the data from the Android side to achieve the operation like query, update, delete. If there's a value need to send back to Android, it will pack the data to Json format and return it with echo command. However, Python was doing the instant data passing, such as face detection, utterance emotion detection. Therefore, there's another Docker with Python to receive the information of user side. It helped to connect to database and update the data with Socket method.
 
* ### Conversation Detection and Generation
  >Our system contains voice and text chatting function. The voice conversation will convert to the text with Speech-to-Text API in Android Studio, and then make a detection on utterances. During the detection process, Python will read the rule-based content, such as the rule file (.txt) and the vocabulary attributes (.xls), to figure out the main event of the conversation. Then, the decision tree will help the chatbot to generate the following conversation content based on CBT concepts. Also, the utterances generation process are used the rule-based method. In the conversation, the chatbot will mainly detect the event, time and relationship, and the emotion patterns are included to the emotion scores.
 
* ### 面部情緒辨識
  >將Open CV模組匯入Android檔案內，使用手機前置鏡頭擷取圖片回傳至Python模型達成面部情緒辨識，為壓縮圖檔大小及縮短辨識時間，我們將鏡頭所拍攝的彩色圖片，轉換成黑白圖片再做辨識，模型以tensorflow建立。其功能於語音聊天過程當中，會不斷偵測當前情緒，並將偵測結果從Android傳至Python計算，最後回傳至Mongo DB紀錄。

* ### 穿戴裝置
  >我們使用研鼎智能GoLife Care-X HR手環協助本專案偵測生理狀況，包含心跳、消耗卡路里、行走距離，以衡量長期活動量，進而評估其情緒狀態。將其公司所開發之SDK匯入Android檔案，應用於本專案當中。

* ### 使用者介面
  >本專案首頁及寵物互動介面為Unity開發，其餘以Android Studio開發。兩者結合方式為將Android Studio檔案設定為lib檔並打包為aar檔，再引入Android Studio匯出apk檔。Unity和Android Studio之間的溝通以static call方式進行參數傳遞、呼叫。Android以XML繪製Layout，Java編寫介面操作，其包含CardView、RecyclerView、Camera、PieChart等，並嵌入Open CV Module、Unity Library、GoLife Care SDK，結合多功能於使用者端，以Volley Library傳接資料，利用Gson於Java語言中接收來自php的Json格式的資料。
  

Environment
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

* ### unity
  >Unity環境使用Unity 2.2.2版本。

* ### android
  >依照官方說明下載Android Studio，從Android Studio開啟本專案檔案，若電腦尚未下載Java需依照環境提示安裝，並同步Gradle，完成專案設定。目前本專案之雲端伺服器IP已關閉，因此，在傳接資料的網址，需更換成各自的伺服器IP。本專案設定gradle(Module:app)，minSdkVersion為23、targetSdkVersion為27。
  
  >注意：本專案只提供學術需求，若需要完整介面檔案，請傳送email至109753106@g.nccu.edu.tw，經評估後，將給予下載權限。
  


Supplement
----
* ### Real-time Facial Emotion Detection using deep learning
  >link: https://github.com/atulapra/Emotion-detection.git

補充說明
----
* ### document
  >document資料夾含有2019大專校院資訊應用服務創新競賽初賽文件、複賽海報及簡報，想知道更詳細內容可查看資料夾文件或是點選上述demo影片連結。
* ### 未完成部分
  >本專案經由測試後，seq2seq辨識及產生句子表現不佳，因此，最終只由rule-based方法進行對話功能。
