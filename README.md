# An AI Chatbot of Mental Analysis and Accompanying

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
 
* ### Utterances Detection and Generation
  >Our system contains voice and text chatting function. The voice conversation will convert to the text with Speech-to-Text API in Android Studio, and then make a detection on utterances. During the detection process, Python will read the rule-based content, such as the rule file (.txt) and the vocabulary attributes (.xls), to figure out the main event of the conversation. Then, the decision tree will help the chatbot to generate the following conversation content based on CBT concepts. Also, the utterances generation process are used the rule-based method. In the conversation, the chatbot will mainly detect the event, time and relationship, and the emotion patterns are included to the emotion scores.
 
* ### Face Emotion Detection
  >We imported Open CV module to the Android file. The front camera of cellphone will capture the picture and return it to the detection model to achieve face emotion detection. To reduce the image size and the detectiono time, we convert the piture to gray. However, the model is established by tensoflow with Python. The function is only enable during voice conversation. It continuously detected the current emotion and return the result from Android to Python. After calculating, it will record the data to Mongo DB.

* ### Wearing Device
  >The GoLife Care-X HR wristband which is conducted by GOYOURLIFE INC. assisted our system to detect the pysical statistics, such as heart rate, calories, walking distance to estimate the amout of activity. Moreover, it may provide some statistics to evaluate the emotion codition. We import the SDK which had been developed by the company to our Android file. 

* ### User Interface
  >Our homepage and virtual pet interaction is developed by Unity, and others are developed with Android Studio. We set the Unity file to lib and pach it to aar format, and then import to Android Studio. The final apk file was exported from Android Studio. The communicationo between Unity and Android Studio is via static call method to pass and call the parameters. In Android project file, the layout was generated by XML, and the operation was coded with Java. The technique contains CardView, RecyclerView, Camera, PieChart, etc. Moreover, the project was embedded Open CV Module, Unity Library, Go Life Care SDK to combine various functions to user. The system passed the data via Volley Library, and used the Gson to depack the Json format data in Java.
  

Environment
----
* ### database
  >We ran the Docker on Ubuntu os environment. The image file was released by Mongo DB official. Its repository with the tag is mongo:last. The host port was set as 28017, and the container port was defalut port 27017.
  
  >Command：docker run -d -p 28017:27017 --name 28to27 mongo:latest

* ### php
  >Create another Docker in the same server. The repository with the tag of the image is php:5-apache. Then, it should link to the above Docker. The host port was set as 8020, and the container port was 80. It's necessary to install related packages, and make the php files in it.
  
  >Command：docker run -d -p 8020:80 --link 28to27 --name php-mongo php:5-apache <br>

  >Environment Setting：
  >* apt-get install openssl libssl-dev libcurl4-openssl-dev
  >* pecl install mongo
  >* echo "extension=mongo.so" > /usr/local/etc/php/conf.d/mongo.ini

* ### rule-based
  >Build a new Docker. Also, The repository with the tag of the image is php:5-apache. Then, it also link to 28to27 Docker. The host port was set as 7070, which was avaliable to let external network connect, and the container port was 8888. It's necessary to install Python environment and other packages, and make the rule-based files in it.
  
  >Command：docker run -d -p 7070:8888 --link 28to27 --name connectPython php:5-apache

  >Environment Setting：
  >* apt-get install python3
  >* apt-get install python3-pip
  >* pip install requests, ckip-segamentor, pandas, pymongo, xlrd

* ### face detection
  >Build a new Docker. The repository with the tag of the image is tensorflow/tensorflow:1.5.0-py3. The host port was set as 7072, which was avaliable to let external network connect, and the container port was 8082. Then, we binded the faceEmotionDockere file to the Docker, and moved the Emotion-detection-master to the Docker. It's also necessary to install the related packages.
  
  >Command：docker run -d -v ~/faceEmotionDocker:/notebooks/faceEmoOnD -p 7072:8082 --name testTensorflow tensorflow/tensorflow:1.5.0-py3
  
  >Environment Setting：
  >* docker cp Emotion-detection-master/ testTensorflow:/notebooks
  >* pip install opencv-python, keras==2.2.4

* ### unity
  >The version of Unity is 2.2.2.

* ### android
  >Download Android Studio first according to the official document, and open our project files from Android Studio. If your pc doesn't contain Java environment, you need to follow the hints to download it. Also, you should synchronous the gradle file with our project. Our server is closed. Therefore, you should modified all the IP links in the projects to your own settings. The setting of minSdkVersion is 23 and targetSdkVersion is 27 in our project.
  
  >Notification: Our project only provides to academic needs. If you need to download the user interface file, please feel free to contact us via send the e-mail to 109753106@g.nccu.edu.tw. We would authorize the access after estimating.

Reference
----
* ### Real-time Facial Emotion Detection using deep learning
  >link: https://github.com/atulapra/Emotion-detection.git

Supplement
----
* ### document
  >The document file contains the introduction document for the preliminary contest of International ICT Innovative Services Awards 2019. Also, the poster and presentation ppt for finals are attached. All the documents are written in Chinese. If you want to understand our systems work in details, you can access the demo video via above link.
* ### Uncompleted Part
  >After implement, we found it was worse to detect and generate utterances with seq2seq method. Therefore, the system only conducts the conversation function with rule-based methods.
