from import_ import *

#檔案讀取
class Load_file():
	#讀取、關閉檔案
	def load_file(self, close_file=False):
		if os.path.exists('./data.json') == False:
			file = open('data.json', 'w+', encoding="utf-8")
			file.close()
			data_dict = {
				"oil_data" : 
					[
						{
							"92汽油" : "0",
							"95汽油" : "0",
							"98汽油" : "0",
							"日期" : "0",
							"調漲" : "0"
						}
					]
			}
			json.dump(data_dict, open('data.json', 'w+'), ensure_ascii=False)
			
		if os.path.exists('userid.json') == False:
			file = open('userid.json', 'w+', encoding="utf-8")
			file.close()
			json.dump({}, open('userid.json', 'w+'), ensure_ascii=False)
		
		if close_file == True:
			self.d.close()
			self.u.close()
			return True
		
		with open("data.json", 'r+') as self.d:
			self.data = json.load(self.d)
		
		with open("userid.json", 'r+') as self.u:
			self.userid = json.load(self.u)

#line bot 資料
class Line_api():
	def __init__(self):
		self.api = LineBotApi(
			'XI7nR5ztvkRzKMIGcbBbm5zxL7xj1uf4tTS5TrgltV93aCV1uCby0eUr0S0NHbgFNDMXIjK/E7vqqfAnjfYnDUbobs9e4WN4A+uSZboEuhDiwUIsZgplCfFAHyGsQd57M6uxLrZ5HwOCj6zyqOJ4jgdB04t89/1O/w1cDnyilFU=')
		self.handler = WebhookHandler('370d4ef98d73310f91550dbbc2fa4f40')
		
	#userid		  ->  傳送訊息到指定的user
	#message		 ->  要傳送的訊息
	#is_group		->  確認傳送訊息的對象是否為群組(未實作)
	#emojis		  ->  傳送的訊息是否要包含表情符號
	#specify_emoji   ->  傳送指定的表情符號
	def send_message(self, userid, message, is_group=False, emojis=False, specify_emoji="none"):
		if emojis == True:
			self.output_emoji_dict = []
			for i in range(len(message)):
				if message[i] == '1':
					message = self.replace_emoji(i, "053", message)
				elif message[i] == '2':
					message = self.replace_emoji(i, "054", message)
				elif message[i] == '3':
					message = self.replace_emoji(i, "055", message)
				elif message[i] == '4':
					message = self.replace_emoji(i, "056", message)
				elif message[i] == '5':
					message = self.replace_emoji(i, "057", message)
				elif message[i] == '6':
					message = self.replace_emoji(i, "058", message)
				elif message[i] == '7':
					message = self.replace_emoji(i, "059", message)
				elif message[i] == '8':
					message = self.replace_emoji(i, "060", message)
				elif message[i] == '9':
					message = self.replace_emoji(i, "061", message)
				elif message[i] == '0':
					message = self.replace_emoji(i, "062", message)
				elif message[i] == '.':
					message = self.replace_emoji(i, "094", message)
					
			self.api.push_message(userid, TextSendMessage(text=message, emojis=self.output_emoji_dict))
		elif emojis == False:
			self.api.push_message(userid, TextSendMessage(text=message))
			
	#emoji_id	 -> 從line developer抓下來的表情符號ID
	#emoji source :  https://developers.line.biz/en/docs/messaging-api/emoji-list/#line-emoji-definitions
	#for_index	-> message的索引位置
	#target_array -> 指定改變陣列
	def replace_emoji(self, for_index, emoji_id, target_array):
		data = {
			"index": -1,
			"productId": "5ac21a8c040ab15980c9b43f",
			"emojiId": "0"
			}
		data["index"] = for_index
		data["emojiId"] = emoji_id
		self.output_emoji_dict.append(data)
		return_str = target_array[:for_index] + '$' + target_array[for_index+1:]
		return return_str
	
class Web_crawler():
	def __init__(self):
		self.load_file = Load_file()
		self.line_api = Line_api()
		self.load_file.load_file()
		
	#查看爬取的資料是否與本地重複
	def check_duplicate_data(self, price_array, target_array):
		count = 0
		self.load_file.load_file()
		for i in range(3):
			if  self.load_file.data["oil_data"][0][target_array[i]] == price_array[i]:
				count += 1
				
		if count == 3:
			self.duplicate_data = True
			self.load_file.load_file("close")
			
		return False
	
	#查詢油價
	def check_oil_price(self, search_now=False):
		url = "https://www.cpc.com.tw/"
		price_array = []
		keyword = ["92汽油",
				   "95汽油",
				   "98汽油",
				   "日期",
				   "調漲"
				   ]
		
		output_str = ""
		self.duplicate_data = False
		
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument('--no-sandbox')

		driver = webdriver.Chrome(options=chrome_options)
		driver.get(url)
		
		#爬取資料
		price = driver.find_elements(By.CLASS_NAME, "price")
		since = driver.find_element(By.CLASS_NAME, "since")
		oil_status = driver.find_element(By.CLASS_NAME, "sys").text + driver.find_element(By.CLASS_NAME, "rate").text
		
		#價格陣列
		for i in range(3):
			price_array.append(float(price[i].text))

		#檢查資訊是否重複
		if search_now == False:
			self.check_duplicate_data(price_array, keyword)
		
		if self.duplicate_data == False:
			data = self.load_file.data
			for i in range(3):
				output_str += "目前" + keyword[i] + "價格:" + str(price_array[i]) + "\n"
				data["oil_data"][0][keyword[i]] = price_array[i]
				
			data["oil_data"][0][keyword[3]] = since.text
			data["oil_data"][0][keyword[4]] = oil_status
			json.dump(data, open('data.json', 'w', encoding="utf-8"), ensure_ascii=False)
			
			#重要!! 分兩次傳送是因為一次傳送訊息的emoji數量不能超過20個
			self.line_api.send_message('Ueea1498b70a1795aceac5537f1fa8d11', output_str, emojis=True)
			
			output_str = since.text + " " + oil_status + "元"
			self.line_api.send_message('Ueea1498b70a1795aceac5537f1fa8d11', output_str, emojis=True)
		else:
			print("data duplicate")
			
		#load_file(True)為關檔案
		self.load_file.load_file(True)	

#使用者輸入的回覆
class Chatbot():
	def __init__(self, api):
		self.load_file = Load_file()
		self.api = Line_api()
		
		self.load_file.load_file()
	
	def chating(self, id, text):
		if text == 'Hello World':
			self.greeting(id)
		elif text == '油價':
			crawler = Web_crawler()
			crawler.check_oil_price(True)
		else:
			self.unknown_message()
	
	#self.load_file.user -> userid.json
	#userid.json格式為 {userId : [打招呼次數, 使用者名稱]}
	def greeting(self, id):
		data = self.load_file.userid
		
		if id in self.load_file.userid:
			message = "你好,已經是第" + str(data[id][0]) + "次打招呼ㄌㄡ!"
			data[id][0] += 1
			json.dump(data, open('userid.json', 'w', encoding="utf-8"), ensure_ascii=False)
			self.api.send_message(id, message)
		else:
			message = "你好, 初次見面! 繃啾てす!"
			self.api.send_message(id, message)
			name = self.api.api.get_profile(id).__dict__["display_name"]
			data[id] = [2, name]
			json.dump(data, open('userid.json', 'w', encoding="utf-8"), ensure_ascii=False)
	
	#當使用者輸入未支援的指令時,發送提示
	def unknown_message(self):
		pass

app = Flask(__name__)
@app.route("/", methods=['POST'])
def get_reply():
	line_api = Line_api()
	chatbot = Chatbot(line_api.api)
	
	body = request.get_data(as_text=True)
	json_data = json.loads(body)
	try:
		signature = request.headers['X-Line-Signature']
		line_api.handler.handle(body, signature)
		#tk = json_data['events'][0]['replyToken']
		user_id = json_data['events'][0]["source"]['userId']
		text = json_data['events'][0]['message']['text']
		chatbot.chating(user_id, text)
	except Exception as e:
		print(e)
	return 'OK'

def jobs1():
	app.run()
	
def jobs2():
	while(True):
		crawler = Web_crawler()
		crawler.check_oil_price()
		time.sleep(86400) #one day = 86400
		#time.sleep(3)

def jobs3():
		subprocess.run([
			"ngrok", 
			"http", 
			"--domain=8ccb1e3131d3-15376459858684696283.ngrok-free.app", 
			"5000",
			"--log=stdout"
		])
	
if __name__ == "__main__":
	warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)
	#多執行緒工作
	jobs = []
	jobs.append(threading.Thread(target=jobs1))
	jobs.append(threading.Thread(target=jobs2))
	jobs.append(threading.Thread(target=jobs3))
	
	status = True
	print("Service starting...")
	for i in range(len(jobs)):
		try:
			jobs[i].start()
		except Exception as e:
			status = False
			print(e + "\nSomething went wrong...")
	
	if status:
		print("All process done!")
#change
