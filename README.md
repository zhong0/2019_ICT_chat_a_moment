# An AI Chatbot of Mental Analysis and Accompanying

Video: https://youtu.be/q21peUzfRBU
* International ICT Innovative Services Awards 2019 (IP Group) - Excellent work
* International ICT Innovative Services Awards 2019 (AWS Group) - Nominated

Introduction
----
* ### Chat for Accompanying
  > Our project is aim to let user pour out their emotion in anytime. Users can not only understand their emotion condition but also obtain a sense of relief. However, we designed the conversation framework based on cognitive behavior therapy (CBT) concepts. The chatbot will gradually figure out the user's emotion and thought for the events which they had been occurred. It will automatically detect and record the events in details to let the user can review their stories in the future.

* ### Emotion Analysis
  >We divide the emotion analysis to short-term and long-term tracking. In the conversation, the chatbot will detect the keywords for five emotions, including happiness, sadness, anger, fear, disgust, as one of the short-term tracking scores. Since it's possible to be hard to understand the complicated emotion in text only, we developed the voice chatting function combining the front camera on mobile phone to detect the emotion on face. The tracking result will present with a pie chart to users. However, the long-term tracking contains anxious and depression tendencies. In addition to detecting keywords of emotion and extremely negative utterances, the questions of anxious and depression scales will be appearing during conversation sometimes. Moreover, our system combined the wristband, which can detect physical statistics, including heart rate, calories, walk distance and steps, to our system. Based on the information, the system can analyze the long-term condition comprehensively.

* ### Virtual Pet Interaction
  > Our system is designed a virtual pet to enhance a sense of accompanying. The interaction operation with the virtual pet contains dragging, clicking, feeding, and so on. Also, the virtual pet has the action as if the people, such as jumping, walking, swagging, etc. Moreover, it has its own emotion. When the user hasn't interacted with it for a long time, the virtual pet will be more and more depressed and the user can recognize the emotion on its face. These designs are aim to let the chatbot to reflect the emotion similar to human and expect to increasing the using attractiveness to our system.

Techniques
----
* ### Data
  >Our system is based on NoSQL database, which has much capability to preserve more complicated data format and much data. According to the official document from Mongo DB, we ran a docker with the official image, and followed the commands to establish database. Owing to un-relational database framework, we just needed to simply design the attributes, such as questions in scales, initial score of each emotion, etc., as the initial data when adding the new user.

* ### Data Transmission
  >The php files are used as the static data passing, such as user information, long-term emotion score, and so on. We ran another docker using php-apache image to do the data passing. The Mongo DB commands were written to the php files. We applied the POST method in php files to receive the data from the Android side to achieve the database manipulation like querying, updating, deleting, etc. If we need to send the value to Android side, it will be packed to Json format and be returned by echo command. However, the instant data passing, including face detection and utterance emotion detection, was coded with Python. Therefore, another docker with Python environment will receive the data from the user, and connect to the database with Socket method.
 
* ### Utterances Detection and Generation
  >Our system contains voice and text chatting function. The voice conversation will convert the sound to the text with Speech-to-Text API in Android Studio. The system makes a detection on utterances with Python. During the detection, the system will read the rule-based content, including the rule file (.txt) and the vocabulary attributes (.xls), to figure out the main event of the conversation. Moreover, the chatbot will generate the following conversation contents with decision tree constructed by CBT concepts. Also, the utterances generation process is applied by the rule-based method. In the conversation, the chatbot will mainly detect the event, occurred time, relationship, and the emotion patterns as the variables to result the emotion scores.
 
* ### Face Emotion Detection
  >We imported Open CV module to the Android file. The front camera of cellphone will capture the pictures as the input to the predicting model to achieve instant face emotion detection. To reduce the image size and the predicting time, we convert the pictures to grayscale. The model is established by tensorflow with Python. This function only operates during voice conversation and continuously detects the current emotion and sends the result from Android to the server. After calculating, the data will be updated to the database.

* ### Wearing Device
  >The GoLife Care-X HR wristband which is conducted by GOYOURLIFE INC. assisted our system to estimate the amount of activity by detecting the physical statistics, such as heart rate, calories, walking distance, etc. We imported the SDK which provided by the company to our Android file. It provides those statistics to assist our system to evaluate the emotion condition.

* ### User Interface
  >Our homepage and virtual pet interaction were developed by Unity, and others were developed with Android Studio. We exported the Unity project and opened it in Android Studio. Then, we converted the Unity project to a library and complied it to an aar file. Further, in Android Studio, the main project imported Unity aar file should inherit UnityPlayerActivity. The communication between Unity and Android Studio is via UnitySendMessage and static call method to transmit the parameters. In Android project, the layout was generated by XML, and the operation was coded with Java. The technique contains CardView, RecyclerView, Camera, PieChart, etc. Moreover, the project was embedded Open CV Module, Unity Library, Go Life Care SDK to display various functions to user. Volley library was applied to pass the data. Gson library helped in Java to parse the Json format data from php files. 

Environment
----
* ### database
  >We ran the docker on Ubuntu os. The image was released by Mongo DB official. Its repository with the tag is mongo:last. The host port was set as 28017, and the container port was default port 27017.
  
  >Command：docker run -d -p 28017:27017 --name 28to27 mongo:latest

* ### php
  >Create another docker container in the same server. The repository with the tag of the image is php:5-apache. Then, link to the above docker. The host port was set as 8020, and the container port was 80. It's necessary to install related packages, and make the php files in it.
  
  >Command：docker run -d -p 8020:80 --link 28to27 --name php-mongo php:5-apache <br>

  >Environment Setting：
  >* apt-get install openssl libssl-dev libcurl4-openssl-dev
  >* pecl install mongo
  >* echo "extension=mongo.so" > /usr/local/etc/php/conf.d/mongo.ini

* ### rule-based
  >Build a new docker container. The repository with the tag of the image is also php:5-apache. Then, it also needs to link to 28to27 docker container. The host port was set as 7070, which was available to let external network connect, and the container port was 8888. It's necessary to install Python environment and other packages, and move the rule-based files to it.
  
  >Command：docker run -d -p 7070:8888 --link 28to27 --name connectPython php:5-apache

  >Environment Setting：
  >* apt-get install python3
  >* apt-get install python3-pip
  >* pip install requests, ckip-segamentor, pandas, pymongo, xlrd

* ### face detection
  >Build a new docker container. The repository with the tag of the image is tensorflow/tensorflow:1.5.0-py3. The host port was set as 7072, which was available to let external network connect, and the container port was 8082. Then, we mount the faceEmotionDockere dictionary to the docker container, and moved the Emotion-detection-master to it. It's also necessary to install the related packages.
  
  >Command：docker run -d -v ~/faceEmotionDocker:/notebooks/faceEmoOnD -p 7072:8082 --name testTensorflow tensorflow/tensorflow:1.5.0-py3
  
  >Environment Setting：
  >* docker cp Emotion-detection-master/ testTensorflow:/notebooks
  >* pip install opencv-python, keras==2.2.4

* ### unity
  >Download Unity with the version 2.2.2 on official website.

* ### android
  >Download Android Studio first according to the official document, and open our project files by Android Studio. If your pc doesn't contain Java environment, you should follow the hints from Android Studio environment to download it. Also, you should synchronize the gradle file with our project. Unfortunately, Our server is closed. Therefore, you should modify all the IP links in the projects to your own settings. The setting of minSdkVersion is 23 and targetSdkVersion is 27 in our project.
  
  >Notification: Our project only provides to academic purpose. If you need to download the user interface file, please feel free to contact us via the e-mail 109753106@g.nccu.edu.tw. We would authorize the access after an assessment.

Reference
----
* ### Real-time Facial Emotion Detection using deep learning
  >https://github.com/atulapra/Emotion-detection.git

Supplement
----
* ### document
  >The document file contains the introduction document for the preliminary contest of International ICT Innovative Services Awards 2019. Also, the poster and presentation ppt for finals are attached. All the documents are written in Chinese. If you want to understand our systems work in details, you can access the demo video via above link.

* ### Uncompleted Part
  >After implement, we found it is hard to detect and generate utterances well with seq2seq method. Therefore, we only release the conversation function with rule-based methods.
