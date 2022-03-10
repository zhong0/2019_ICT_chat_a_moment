import pandas as pd #資料處理 pandas
import numpy as np #資料處理 numpy
import re
import linecache
import random
from ckip import CkipSegmenter
import os  # Files management
import math
import socket
import pymongo
import datetime

host, port = "", 8888
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

segmenter = CkipSegmenter()

ynDoc = pd.read_excel('ynResponse.xls',header = 0)
classify = pd.read_excel('classify.xls', header = 0)
activeEventClassify = pd.read_excel('activeClassify.xls',header = 0)
passiveEventClassify = pd.read_excel('passiveClassify.xls',header = 0)
pureEmotionResponse = pd.read_excel('pureEmotionResponse.xls',header = 0)
chkEventPkg = pd.read_excel('chkEventpkg.xls',header = 0)
favoriteResponse = pd.read_excel('favoriteResponse.xls',header = 0)
print(classify)

emotionRule = []
emotionLabel = []
eventRule = []
eventRuleLabel = []
eventsNum = 0
favoriteRule = []
favoriteLabel = []
ynRule = []
ynLabel = []

judgeFace = ""
fResult = ""

leafName = 0 #用來判斷第一層要走哪條路
oriLeafTagName = 'nothing'
chatbotTag = 'nothing'
classifyTag = ['被動事件','主動事件','情緒','喜好','一般']
trackLevel = 1
boolActiveEventField = [False,False,False]
boolPassiveEventField = [False,False,False,False]
boolEmotionField = [False,False,False]
nowRecord = [0]*7
boolNowRecord = [False,False,False,False,False,False,False]
#0:事件, #1:情緒, #2:時間, #3人, #4想法, #5想法, #6想法

def ifFaceCheck():
	with open('/var/www/html/faceEmoOnD/faceEmotionTrigger.txt','r') as f:
		yn = f.readline()
	return yn

def faceCheckResult():
	with open('/var/www/html/faceEmoOnD/faceEmotion.txt','r') as faceF:
		faceResult = faceF.read().split('\n')[1]
		print('FR is ',faceResult)
	return faceResult

def readRule(filename,sentenceRule,allLabel):
	with open(filename, 'r') as f:
		line = f.readline()
		while line:
			eachline = line.split()
			readLineLength = len(eachline)-1
			read_data = [str(x) for x in eachline[0:readLineLength]]
			label = eachline[-1]
			allLabel.append(label)
			sentenceRule.append(read_data)
			line = f.readline()
	return

readRule('allRule.txt',emotionRule,emotionLabel)
readRule('passiveEventRule.txt',eventRule,eventRuleLabel)
readRule('activeEventRule.txt',eventRule,eventRuleLabel)
readRule('judgefavoriteRule.txt',favoriteRule,favoriteLabel)
readRule('ynRule.txt',ynRule,ynLabel)

def cw(x):
	try:
		result = segmenter.seg(x).tok
		print(result)
	except:
		return
	return result

def favoriteResponseRule(inputTag):  #拿現有的tag對應出回應tag
	searchRule = []
	responseRule = []
	print("inputTag1:"+(str)(inputTag))
	count = 0
	with open('favoriteResponse.txt', 'r') as f:
		line = f.readline()
		while line:
			eachline = line.split()
			readLineLength = len(eachline)
			read_data = [str(x) for x in eachline[1:readLineLength]]
			searchRule.append(read_data)
			label = eachline[0]
			if(inputTag == label):
				responseRule = searchRule[count][:]
				print(responseRule)
				response = assembleSentence(favoriteResponse,responseRule)
				del searchRule
				del responseRule
				f.close()
				return response
			line = f.readline()
			count+=1
	return 'nothing'

def assembleSentence(file,rpr):
	response = ''
	chk = False
	for x in range(len(rpr)):
		for i in range(file.shape[1]):
			if(file.columns[i] == rpr[x]):
				while(1):
					print(len(file.loc[:,rpr[x]])-1)
					num = random.randint(0,len(file.loc[:,[rpr[x]]])-1)
					print(file.iloc[num,i])
					if(file.isnull().iloc[num,i] != True):
						response += (str)(file.iloc[num,i])
						break
	print(response)
	return response

def getEventQuestTag(eventTag):
	result = {
		'開心':'詢問開心事件',
		'難過':'詢問難過事件',
		'恐懼':'詢問恐懼事件',
		'生氣':'詢問生氣事件',
		'厭惡':'詢問厭惡事件'
	}
	return result.get(eventTag,None)

def getEmotion(no):
	result = {
		0:'開心',
		1:'難過',
		2:'恐懼',
		3:'生氣',
		4:'厭惡'
	}
	return result.get(no,None)

def getEventEmotion(eventTag):
	result = {
		'主動開心事件':'詢問開心情緒',
		'主動難過事件':'詢問難過情緒',
		'主動恐懼事件':'詢問恐懼情緒',
		'主動生氣事件':'詢問生氣情緒',
		'主動厭惡事件':'詢問厭惡情緒',
		'被動開心事件':'詢問開心情緒',
		'被動難過事件':'詢問難過情緒',
		'被動恐懼事件':'詢問恐懼情緒',
		'被動生氣事件':'詢問生氣情緒',
		'被動厭惡事件':'詢問厭惡情緒'
	}
	return result.get(eventTag,None)

def getEmotionTag(Tag):
	result = {
		'開心':'happyNum',
		'難過':'sadNum',
		'恐懼':'fearNum',
		'生氣':'angerNum',
		'厭惡':'hateNum'
	}
	return result.get(Tag,None)

def getCorrectTag(num):
	result = {
		2:'詢問事件時間',
		3:'詢問'+ (str)(nowRecord[1]) + '人物'
	}
	return result.get(num,None)

def getEmotionContent(num,userTag):
	result = {
		1:'詢問事件',
		2:'安撫回應'
	}
	if result.get(num,None) == '詢問事件':
		return getEventQuestTag(userTag)
	return result.get(num,None)

def getPassiveEventContent(num,userTag):
	result = {
		1:'事件情緒',
		2:'事件時間',
		3:'事件人物'
	}
	if result.get(num,None) == '事件情緒':
		return getEventEmotion(userTag)
	else:
		return getCorrectTag(num)

def getActiveEventContent(num,userTag):
	result = {
		1:'事件情緒',
		2:'事件時間'
	}
	if result.get(num,None) == '事件情緒':
		return getEventEmotion(userTag)
	else:
		return getCorrectTag(num)

eventsNum = 0
def connDB():
	global eventsNum
	time = datetime.datetime.now()
	date = (str)(time.year)+"-"+(str)(time.month)+"-"+(str)(time.day)
	myclient = pymongo.MongoClient("mongodb://28to27:27017/")
	mydb = myclient["userTest"]
	mycol = mydb["user"]
	condition = {"account":"zhong0"}
	user = mycol.find_one(condition)

	user['event'+(str)(eventsNum)] = nowRecord[0]
	user['eventEmotion'+(str)(eventsNum)] = nowRecord[1]
	user['eventTime'+(str)(eventsNum)] = nowRecord[2]
	user['eventPeople'+(str)(eventsNum)] = nowRecord[3]
	user['eventDate'+(str)(eventsNum)] = date
	user['allEventsNum'] = eventsNum+1

	eventsNum += 1
	mycol.update(condition,user)
	return

def inputEmotionToDB(tag):
	myclient = pymongo.MongoClient("mongodb://28to27:27017/")
	mydb = myclient["userTest"]
	mycol = mydb["user"]
	condition = {"account":"zhong0"}
	user = mycol.find_one(condition)
	user[getEmotionTag(tag)] += 1

	mycol.update(condition,user)
	return

def chkCol(sen,readfile): #產生詞分類的string陣列
	i=0
	j=1
	senList = []
	matchWord = False
	for word in sen:
		for i in range(readfile.shape[1]):
			j=1
			for j in range(readfile.shape[0]):
				if readfile.iloc[j,i]==word:
					print(readfile.columns[i])
					senList.append(readfile.columns[i])
					matchWord = True
					break
				j+=1
			if matchWord == True:
				matchWord = False
				break
	return senList

def cmpContent(verifySen,rule,label):
	senListLength = len(verifySen)
	matchCount = 0
	for totalRule in range(len(rule)):
		countRule = 0
		countSen = 0
		matchCount = 0
		while countSen < senListLength and countRule < len(rule[totalRule]):
			if verifySen[countSen] == rule[totalRule][countRule]:
				countRule+=1
				matchCount+=1
				print('senList',verifySen[countSen],'matchCount:',matchCount,'ruleLength',len(rule[totalRule]))
				if matchCount == len(rule[totalRule]):
					print(label[totalRule])
					return label[totalRule]
			if countSen == senListLength-1:
				countSen = 0
				countRule+=1
			else:
				countSen+=1
	return 'nothing'

def cmpEventContent(verifySen): #回傳事件那些tag
	detectEmotion = ''
	senListLength = len(verifySen) #使用者輸入的斷句長度
	matchCount = 0
	for totalEventRule in range(len(eventRule)):
		countRule = 0  #總共有幾條rule
		countSen = 0   #計算目前跑到使用者輸入的第幾個斷詞
		matchCount = 0 #符rule的斷詞數量
		while countSen < senListLength and countRule < len(eventRule[totalEventRule]):
			if verifySen[countSen] == eventRule[totalEventRule][countRule]:
				countRule+=1
				matchCount+=1
				print('senList',verifySen[countSen],'matchCount:',matchCount,'ruleLength',len(eventRule[totalEventRule]))
				if matchCount == len(eventRule[totalEventRule]):
					detectEmotion = eventRuleLabel[totalEventRule]
					countRule += 1
					matchCount = 0
					countSen = 0
					print("detectEmotion1:"+ detectEmotion)
					return detectEmotion
			if countSen == senListLength-1:
				countSen = 0
				countRule+=1
			else:
				countSen+=1
	return 'nothing'

def chkYN(sen):
	tag = cmpContent((chkCol(cw(sen),ynDoc)),ynRule,ynLabel)
	return tag

def chkEvent(sen): #如果走進第一層是事件
	global trackLevel
	global leafName
	print(trackLevel)
	tag = cmpEventContent(chkCol(cw(sen),passiveEventClassify))
	if tag != 'nothing':
		if trackLevel == 1:
			leafName = classifyTag[0]
		trackLevel += 1
		return tag
	else:
		tag = cmpEventContent(chkCol(cw(sen),activeEventClassify))
		if tag != 'nothing':
			if trackLevel == 1:
				leafName = classifyTag[1]
			trackLevel += 1
			return tag
		else:
			return tag

def chkEmotion(sen): #如果走進第一層是情緒
	global trackLevel
	global leafName
	print(trackLevel)
	tag = cmpContent((chkCol(cw(sen),classify)),emotionRule,emotionLabel)
	if tag != 'nothing':
		nowRecord[1] = tag
		boolNowRecord[1] = True
		if trackLevel == 1 and nowRecord[0] == 0:
			leafName = classifyTag[2]
			print(leafName)
		trackLevel += 1
	return tag

def chkFavorite(sen):
	tag = cmpContent((chkCol(cw(sen),favoriteResponse)),favoriteRule,favoriteLabel)
	return tag

#0:開心，1:難過，2:恐懼，3:生氣，4:厭惡
def pSimpleResponese(nowTag, no):
	global chatbotTag
	nowRecord[1] = getEmotion(no)
	boolNowRecord[1] = True
	print(nowRecord[1])
	sRes = chkResponseRule(readResponsePairing('allTagPairing.txt', nowTag+chatbotTag))
	return sRes

def positiveRes(nowTag):
	global chatbotTag
	if re.match(r'\S\S開心',chatbotTag) != None:
		return pSimpleResponese(nowTag,0)
	elif re.match(r'\S\S難過',chatbotTag) != None:
		return pSimpleResponese(nowTag,1)
	elif re.match(r'\S\S恐懼',chatbotTag) != None:
		return pSimpleResponese(nowTag,2)
	elif re.match(r'\S\S生氣',chatbotTag) != None:
		return pSimpleResponese(nowTag,3)
	elif re.match(r'\S\S厭惡',chatbotTag) != None:
		return pSimpleResponese(nowTag,4)
	return 'nothing'

def getLastTag(nowTag): #肯定or否定
	global chatbotTag
	if re.match(r'是否',chatbotTag) != None:
		if re.match(r'肯定',nowTag) != None:
			return positiveRes(nowTag)
	return 'nothing'

def getUserTag(sen): #得到使用者的tag
	global conn
	result = chkYN(sen) #先判斷是不是yesno回答
	if result != 'nothing':
		conn.send(getLastTag(result).encode("utf-8"))
		print('result:'+result)
		return result

	result = chkEvent(sen) #若不是的話，先順位一被動事件
	if result != 'nothing':
		print('result:'+ result)
		return result

	result = chkEmotion(sen) #順位二情緒
	if(judgeEmotionResult(result) != 'nothing'):
		inputEmotionToDB(result)
	print('resultInUserTag:'+(str)(result))
	if result != 'nothing':
		print('result:'+ result)
		return result

	result = chkFavorite(sen)
	if result != 'nothing': #順位三 喜好事件
		print('result:'+result)
		return result
	return 'nothing'

#順位 #1情緒,事件 #2 人,時  #3 想法  #4 其他
def responsePassiveEvent(userTag): #被動事件分支
	i = 0
	questList = []
	for count in range(len(boolNowRecord)):
		if boolNowRecord[count] == True:
			boolPassiveEventField[count] = True
	while i < len(boolPassiveEventField):
		if boolPassiveEventField[i] == False:
			questList.append(i)
			print('unAskedQuestion:'+(str)(i)+' ')
		i+=1
	if len(questList) != 0:
		if questList[0] == 1:
			getQuestionTag = getPassiveEventContent(1,userTag)
			print(getQuestionTag)
		else:
			getQuestion = random.choice(questList)
			getQuestionTag = getPassiveEventContent(getQuestion,userTag)
			print('getQuestionTag:'+ getQuestionTag)
			del questList
	else:
		getQuestionTag = responseThought(userTag)
	if getQuestionTag == None:
		return 'nothing'
	return getQuestionTag

def responseActiveEvent(userTag): #主動事件分支
	i = 0
	questList = []
	nowRecord[3] = '自己'
	for count in range(len(boolNowRecord)):
		if boolNowRecord[count] == True:
			boolActiveEventField[count] = True

	while i < len(boolActiveEventField):
		if boolActiveEventField[i] == False:
			questList.append(i)
		i+=1

	if len(questList) != 0:
		if questList[0] == 1: #如果情緒還沒被問過
			getQuestionTag = getActiveEventContent(1,userTag)
		else:
			getQuestion = random.choice(questList)
			getQuestionTag = getActiveEventContent(getQuestion,userTag)
		del questList

	else:
		getQuestionTag = responseThought(userTag)
	if getQuestionTag == None:
		return 'nothing'
	return getQuestionTag

def responseEmotion(userTag): #情緒分支
	i = 0
	questList = []
	boolEmotionField[0] = True
	if boolNowRecord[0] != 0:
		boolEmotionField[1] =True
	while i < len(boolEmotionField):
		if boolEmotionField[i] == False:
			print('問題：'+(str)(i))
			questList.append(i)
		i+=1
	print('第一個問題:'+(str)(questList[0]))
	if len(questList) != 0:
		if nowRecord[1] == '開心':
			getQuestionTag = getEmotionContent(1,userTag)
		else:
			getQuestion = random.choice(questList)
			getQuestionTag = getEmotionContent(getQuestion,userTag)
		del questList
	else:
		getQuestionTag = responseThought(userTag)
	if getQuestionTag == None:
		return 'nothing'
	return getQuestionTag

def responseThought(userTag): #想法
	i = 4
	while i<7:
		if boolNowRecord[i] == False:
			if i == 4:
				getQuestionTag = '首次事件想法'
				boolNowRecord[i] = True
				return getQuestionTag
			else:
				getQuestionTag = '再次事件想法'
				boolNowRecord[i] = True
				return getQuestionTag
		i+=1
	return 0

def chkResponseRule(inputTag):  #拿現有的tag對應出回應tag
	searchRule = []
	responseRule = []
	print("inputTag1:"+(str)(inputTag))
	count = 0
	with open('allResponse.txt', 'r') as f:
		line = f.readline()
		while line:
			eachline = line.split()
			readLineLength = len(eachline)
			read_data = [str(x) for x in eachline[1:readLineLength]]
			searchRule.append(read_data)
			label = eachline[0]
			if inputTag == label:
				responseRule = searchRule[count][:]
				print(responseRule)
				response = assembleSentence(pureEmotionResponse,responseRule)
				del searchRule
				del responseRule
				f.close()
				return response
			line = f.readline()
			count+=1
	return 'nothing'

def getFaceCheck(emoTag):
	result = {
		"開心":"Happy",
		"難過":"Sad",
		"恐懼":"Fearful",
		"生氣":"Angry",
		"厭惡":"Disgusted"
	}
	return result.get(emoTag,None)

def judgeEmotionResult(emoTag):
	if(faceCheckResult == 1):
		if(getFaceCheck(emoTag) == faceCheckResult()):
			return emoTag
		else:
			return 'nothing'
	else:
		return emoTag

def getAnxQuestion(qNum):
	result = {
		"anx1":"焦慮、煩躁、擔心或恐懼",
		"anx2":"覺得四周的事物都很怪異和不真實",
		"anx3":"突然感到恐慌",
		"anx4":"不安或感到大禍臨頭",
		"anx5":"整個人都很緊繃，有壓力或隨時崩潰",
		"anx6":"難以集中精神",
		"anx7":"思緒紛亂",
		"anx8":"恐怖幻想或白日夢",
		"anx9":"感覺隨時失控",
		"anx10":"害怕自己會瘋掉",
		"anx11":"害怕突然昏倒",
		"anx12":"害怕生病、心臟病或快要死亡",
		"anx13":"害怕恐怖的事情會發生",
		"anx14":"心悸或心跳加速",
		"anx15":"胸口疼痛或緊縮",
		"anx16":"手指或腳趾有刺痛或麻木感",
		"anx17":"胃痛或胃不舒服",
		"anx18":"心神不寧",
		"anx19":"肌肉緊繃",
		"anx20":"冒冷汗",
		"anx21":"發抖",
		"anx22":"雙腳不靈活",
		"anx23":"頭昏眼花或失平衡",
		"anx24":"發冷或發熱",
		"anx25":"疲憊、虛弱或容易精疲力盡"
	}
	return result.get(qNum,None)
def getAnxNum(qContent):
	result = {
		"焦慮、煩躁、擔心或恐懼":"anx1",
		"覺得四周的事物都很怪異和不真實":"anx2",
		"突然感到恐慌":"anx3",
		"不安或感到大禍臨頭":"anx4",
		"整個人都很緊繃，有壓力或隨時崩潰":"anx5",
		"難以集中精神":"anx6",
		"思緒紛亂":"anx7",
		"恐怖幻想或白日夢":"anx8",
		"感覺隨時失控":"anx9",
		"害怕自己會瘋掉":"anx10",
		"害怕突然昏倒":"anx11",
		"害怕生病、心臟病或快要死亡":"anx12",
		"害怕恐怖的事情會發生":"anx13",
		"心悸或心跳加速":"anx14",
		"胸口疼痛或緊縮":"anx15",
		"手指或腳趾有刺痛或麻木感":"anx16",
		"胃痛或胃不舒服":"anx17",
		"心神不寧":"anx18",
		"肌肉緊繃":"anx19",
		"冒冷汗":"anx20",
		"發抖":"anx21",
		"雙腳不靈活":"anx22",
		"頭昏眼花或失平衡":"anx23",
		"發冷或發熱":"anx24",
		"疲憊、虛弱或容易精疲力盡":"anx25"
	}
	return result.get(qContent,None)

def getDepQuestion(qNum):
	result = {
		"dep1":"覺得想哭",
		"dep2":"心情不好",
		"dep3":"比以前容易發脾氣",
		"dep4":"覺得很煩",
		"dep5":"不輕鬆、不舒服(不適快)",
		"dep6":"做事情無法專心",
		"dep7":"記憶力不好",
		"dep8":"不想吃東西",
		"dep9":"想事情或做事時比平常要緩慢",
		"dep10":"比以前沒信心",
		"dep11":"比較會往壞處想",
		"dep12":"想不開、甚至想死",
		"dep13":"對什麼事都失去興趣",
		"dep14":"自己很沒用",
		"dep15":"身體不舒服(如頭痛、頭暈、心悸、肚子不舒服等)",
		"dep16":"睡不好",
		"dep17":"胸口悶悶的",
		"dep18":"身體疲勞虛弱無力"
	}
	return result.get(qNum,None)

def getDepNum(qContent):
	result = {
		"覺得想哭":"dep1",
		"心情不好":"dep2",
		"比以前容易發脾氣":"dep3",
		"覺得很煩":"dep4",
		"不輕鬆、不舒服(不適快)":"dep5",
		"做事情無法專心":"dep6",
		"記憶力不好":"dep7",
		"不想吃東西":"dep8",
		"想事情或做事時比平常要緩慢":"dep9",
		"比以前沒信心":"dep10",
		"比較會往壞處想":"dep11",
		"想不開、甚至想死":"dep12",
		"對什麼事都失去興趣":"dep13",
		"自己很沒用":"dep14",
		"身體不舒服(如頭痛、頭暈、心悸、肚子不舒服等":"dep15",
		"睡不好":"dep16",
		"胸口悶悶的":"dep17",
		"身體疲勞虛弱無力":"dep18"
	}
	return result.get(qContent,None)

def chooseScaleQuestion(scaleType):
	myclient = pymongo.MongoClient("mongodb://28to27:27017/")
	mydb = myclient["userTest"]
	mycol = mydb["user"]
	condition = {"account":"zhong0"}
	user = mycol.find_one(condition)

	anxietyGrade = [0]*25
	anxietyName = []
	depressionGrade = [0]*18
	depressionName = []
	#print("userDEP:"+user["dep1"])
	for i in range(0,25):
		anxietyGrade[i] = user["anx"+(str)(i+1)]
		anxietyName.append(getAnxQuestion("anx"+(str)(i+1)))

	for j in range(0,18):
		depressionGrade[j] = user["dep"+(str)(j+1)]
		depressionName.append(getDepQuestion("dep"+(str)(j+1)))

	for i in range(0,24):
		for j in range(0,24):
			if anxietyGrade[j+1] < anxietyGrade[j]:
				tempN = anxietyName[j+1]
				temp = anxietyGrade[j+1]
				anxietyName[j+1] = anxietyName[j]
				anxietyGrade[j+1] = anxietyGrade[j]
				anxietyName[j] = tempN
				anxietyGrade[j] = temp

	for i in range(0,17):
		for j in range(0,17):
			if depressionGrade[j+1] < depressionGrade[j]:
				tempN = depressionName[j+1]
				temp = depressionGrade[j+1]
				depressionName[j+1] = depressionName[j]
				depressionGrade[j+1] = depressionGrade[j]
				depressionName[j] = tempN
				depressionGrade[j] = temp

	for i in range(0,25):
		print("anxietyName:"+anxietyName[i])

	for j in range(0,18):
		print("depressionName:"+depressionName[j])

	if re.match(r'詢問焦慮量表',scaleType):
		return "最近會" + anxietyName[24] + "嗎" +":"+getAnxNum(anxietyName[24])
	elif  re.match(r'詢問憂鬱量表',scaleType):
		return "最近會" + depressionName[17] + "嗎" +":"+getDepNum(depressionName[17])
	return '?'

def readResponsePairing(filename,oriTag):  #對應出tag
	global chatbotTag
	tagPairRule = []
	count = 0
	print("oriTag:"+ (str)(oriTag))
	with open(filename, 'r') as f:
		line = f.readline()
		while line:
			eachline = line.split()
			readLineLength = len(eachline)
			read_data = [str(x) for x in eachline[1:readLineLength]]
			tagPairRule.append(read_data)
			label = eachline[0]
			if oriTag == label:
				randomNum = random.randint(0,readLineLength-2)
				userTag = tagPairRule[count][randomNum]
				print("userTag:"+userTag)
				del tagPairRule
				f.close()
				chatbotTag = userTag
				print('userTag:'+userTag)
				return userTag
			line = f.readline()
			count+=1
	return 'nothing'

def chkPkg(sen,readfile): #檢查時間 人物
	global trackLevel
	global chatbotTag
	i=0
	j=1
	matchWord = False
	for word in sen:
		for i in range(readfile.shape[1]):
			j=1
			for j in range(readfile.shape[0]):
				if readfile.iloc[j,i]==word:
					if readfile.columns[i] == '時間副詞':
						nowRecord[2] = word
						boolNowRecord[2] = True
					if readfile.columns[i] == '他人主詞':
						nowRecord[3] = word
						boolNowRecord[3] = True
					matchWord = True
				j+=1
			if matchWord == True:
				matchWord = False
				break
	if boolNowRecord[2] and boolNowRecord[3]:
		trackLevel += 1
	return 'packageChecked'
def firstLevel(input,tag):
	global leafName
	global oriLeafTagName
	global chatbotTag
	chatbotResponse = ""
	if tag == 'nothing':
		leafName = classifyTag[4]
	print('leafName'+(str)(leafName))
	if leafName == classifyTag[0]:
		nowRecord[0] = input
		boolNowRecord[0] = True
		fResult = chkEmotion(input)
		#if(judgeEmotionResult(fResult) != 'nothing'):
			#inputEmotionToDB(fResult)
		chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt', responsePassiveEvent(oriLeafTagName)))
	elif leafName == classifyTag[1]:
		nowRecord[0] = input
		boolNowRecord[0] = True
		fResult = chkEmotion(input)
		#if(judgeEmotionResult(fResult) != 'nothing'):
			#inputEmotionToDB(fResult)
		chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt',responseActiveEvent(oriLeafTagName)))
	elif leafName == classifyTag[2]:
		nowRecord[1] = tag
		boolNowRecord[1] = True
		boolEmotionField[0] = True
		chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt',responseEmotion(oriLeafTagName)))
	elif leafName == classifyTag[3]:
		chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt',tag))
	elif leafName == classifyTag[4]:
		getLastTag = readResponsePairing('allTagPairing.txt',tag)
		if re.match(r'詢問焦慮量表',getLastTag) or re.match(r'詢問憂鬱量表',getLastTag):
			chatbotResponse = "Scale:" + chooseScaleQuestion(getLastTag)
		else:
			chatbotResponse = "Normal:" + chkResponseRule(getLastTag)
	return chatbotResponse

def setZero(inputTag,uInput):
	global oriLeafTagName
	global trackLevel
	oriLeafTagName = inputTag
	trackLevel = 1
	nowRecord[0] = uInput
	n = 1
	while n < 7:
		nowRecord[n] = 0
		boolNowRecord[n] = False
		n += 1
	return

def createResponse(user):
	global trackLevel
	global leafName
	global oriLeafTagName
	chatbotResponse = 'nothing'
	nowTag = 'nothing'
	if trackLevel == 1: #第一層
		nowTag = getUserTag(user)
		print('nowTag:'+ nowTag)
		chkPkg(cw(user),chkEventPkg)
		print(oriLeafTagName)
		oriLeafTagName = nowTag
		chatbotResponse = firstLevel(user,nowTag)
	elif trackLevel >= 2:
		nowTag = getUserTag(user)
		print("nowTag:"+nowTag)
		if re.match(r'nothing',nowTag):
			for i in range(7):
				nowRecord[i] = 0
				boolNowRecord[i] = False
			for i in range(3):
				boolActiveEventField[i] = False
			for i in range(4):
				boolPassiveEventField[i] = False
			leafName = classifyTag[4]
		matchCheckA = re.match(r'主動',nowTag)
		matchCheckP = re.match(r'被動',nowTag)

		if (nowTag == ('被動' + (str)(nowRecord[1]) + '事件')) and (nowRecord[0] == 0): #第一次偵測到被動事件
			leafName = classifyTag[0]
			nowRecord[0] = user
			boolNowRecord[0] = True
			boolPassiveEventField[0] = True
		elif (nowTag == ('主動' + (str)(nowRecord[1]) + '事件')) and (nowRecord[0] == 0): #第一次偵測到主動事件
			leafName = classifyTag[1]
			nowRecord[0] = user
			boolNowRecord[0] = True
			boolActiveEventField[0] = True
		elif matchCheckP != None and nowRecord[0] != 0: #已偵測到下一被動事件
			connDB()
			setZero(nowTag,user)
			m = 1
			while m < 4:
				boolPassiveEventField[m] = False
				m += 1
			leafName = classifyTag[0]

		elif matchCheckA != None and (nowRecord[0] != 0): #已偵測到下一主動事件
			connDB()
			setZero(nowTag,user)
			m = 1
			while m < 3:
				boolActiveEventField[m] = False
				m += 1
			leafName = classifyTag[1]

		print('trackLevel'+(str)(trackLevel))
		print('leafName:'+leafName)
		chkPkg(cw(user),chkEventPkg)
		print('oriLeafTagName:'+oriLeafTagName)
		if trackLevel == 1:
			trackLevel += 1
			chatbotResponse = firstLevel(user,'nothing')
		elif leafName == classifyTag[0]:
			fResult = chkEmotion(user)
			if(judgeEmotionResult(fResult) != 'nothing'):
				inputEmotionToDB(fResult)
			chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt',responsePassiveEvent(oriLeafTagName)))
		elif leafName == classifyTag[1]:
			fResult = chkEmotion(user)
			if(judgeEmotionResult(fResult) != 'nothing'):
				inputEmotionToDB(fResult)
			chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt',responseActiveEvent(oriLeafTagName)))
		elif leafName == classifyTag[2]:
			chatbotResponse = "Normal:" + chkResponseRule(readResponsePairing('allTagPairing.txt',responseEmotion(oriLeafTagName)))
		elif leafName == classifyTag[4]:
			trackLevel = 1
			for i in range(7):
				nowRecord[i] = 0
				boolNowRecord[i] = False
			for i in range(3):
				boolActiveEventField[i] = False
			for i in range(4):
				boolPassiveEventField[i] = False
			leafName = classifyTag[4]
			getLastTag = readResponsePairing('allTagPairing.txt',nowTag)
			if re.match(r'詢問焦慮量表',getLastTag) or re.match(r'詢問憂鬱量表',getLastTag):
				chatbotResponse = "Scale:" + chooseScaleQuestion(getLastTag)
			else:
				chatbotResponse = "Normal:" + chkResponseRule(getLastTag)
	return chatbotResponse

def recv():
	try:
		client.bind((host,port))
	finally:
		pass
	client.listen(10)
	print("Start...")
	while True:
		faceResult = ''
		global conn
		conn, addr = client.accept()
		print ("client with address: ", addr, " is connected.")
		data = conn.recv(1024).decode() #python2轉3 要先decode
		data = (str)(data)
		print(data)
		response = createResponse(data)
		conn.send(response.encode("utf-8"))
		conn.close()
	client.close()
recv()

'''run = 0
while run == 0:
	user = input("Input the statement:")
	checkTag = ''
	checkEmotionTag = ''
	print('Chatbot:' + createResponse(user))
	print(boolNowRecord)
	print(nowRecord)
'''
