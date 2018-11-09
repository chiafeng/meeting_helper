#!/usr/bin/env python3
import os
from flask import Flask, request, render_template

from audio2text import *
from keyword_extract import *

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024

app_root = os.path.dirname(os.path.abspath(__file__))
# path for uploaded files
file_dir = app_root + "/files"

# first page
@app.route("/")
def index():
	# show html template
	return render_template("index.html")

# result page when user upload their files
@app.route("/result", methods=['POST'])
def result():
	# check file_dir
	if not os.path.isdir(file_dir):
		os.mkdir(file_dir)

	# save uploaded file
	file = request.files.get("file")		# use getlist("file") to get multiple files
	dest = file_dir + "/" + file.filename
	print(dest)
	file.save(dest)

	# pass file path to my function
	page = service(dest)

	# return result on web page (HTML format)
	return page

# process the file here
def service(filepath):
	#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "????.json"
	
	# upload file
	gcs_header = "gs://"
	target_bucket = "speech_test_kyuc"
	target_blob_name = os.path.basename(filepath)
	print("uploading...")
	upload_blob(target_bucket, filepath, target_blob_name)

	# transcribe to text
	gcs_link = gcs_header + target_bucket + '/' + target_blob_name
	print(gcs_link)
	print("transcribing to text...")
	import time
	start = time.time()
	text = transcribe_gcs(gcs_link)
	end = time.time()
	print("cost time: {}s".format(end - start))
	if len(text) == 0:
		print("Warn: No text from audio!!")
	print(text)

	# extract entity from text
	print("extracting entity...")
	entities = entities_text(text)

	# prepare data for wordcloud
	mapping = []
	entity_pool = set()
	js_list = "[]"
	if entities is not None:
		for entity in entities:
			# remove duplicates and single word
			if len(entity.name) > 1 and entity.name not in entity_pool:
				entity_pool.add(entity.name)
				mapping.append([entity.name, entity.salience * 100])
		js_list = repr(mapping)
	print(js_list)
	print("Done")

	# show html template
	return render_template("result.html", mapping=js_list)

@app.route("/123", methods=['GET'])	
def fake_result():
	file_name = "大亂鬥"
	text = \
"""A 所以，我們這次浪費這麼多時間到底是要做什麼
B 就那個啊
A 哪個
B 最後決定的名字 (自己配音小叮噹拿道具音效
A ....
A ....
B 你說點話 不要讓我尷尬
A 話
B ....
B ....
B 不然這樣好了，你問我這個東西有什麼功能，讓我能繼續接下去，求你!
A 痾.....不要
B 我們這次做的東西呢，最主要的用途就是讓你開會的時候如果不小心神遊去了彼方，還有一層後盾!
A 那如果開會的時候，你一直在講廢....我是說，有的人講話技巧比較差，比較不會講重點的話
B 也有幫助!使用我們這套軟體絕對藥到病除
A 喔~
B 快點，你快點問我我們的產品有什麼功能!
A 所以這產品有...
B 我們的產品會自動幫你把開會紀錄畫重點!!!!
  大家回憶一下，國高中大學的時候，每本參考書都用螢光筆塗得滿滿的，每一張白色的紙每次都要被你畫成整張亮綠色 粉紅色 或是醜到不行的怪怪橘色
  那時候的我們，是多麼的痛苦啊...
  好不容易脫離了學生生涯，進入了職場
  沒想到!!
  開會的時候還要一直記重點!!
  而且開會的時候還沒有文本可以給你慢慢看
  不管台上的人講話鏗鏘有力，還是小聲地讓你想送他下地獄
  都是一閃而過!!
  你一個恍神就是沒聽到!!
  怎麼辦?交給我們!最後決定的名字搞定你的每場會
  幫你做成文字紀錄
  幫你畫重點
  讓你每一次的下班都巴不得明天趕快回來上班!
  每一次開會結束都想要預定下個小時的會議室再開一場會!!
A (敷衍地拍手)
B 痾...對..反正就是這樣
A (敷衍地拍手)"""
	freq =\
"""88	英語
87	http
68	請求
42	伺服器
34	協定
33	方法
27	資源
26	web
21	用戶
20	網路
19	一個
19	編輯
17	戶端
17	語意
16	版本
15	用戶端
14	protocol
14	個請求
14	狀態
14	資訊
13	使用
12	GET
12	TCP
12	或者
12	指定
12	連接
11	例如
11	傳輸
11	支援
11	資料
11	這個
10	Semantic
10	作用
10	的請求
10	程式
9	RFC
9	URI
9	副作用
9	的資
9	網際網路
9	請求方法
8	API
8	代理
8	可以
8	回應
8	應用
8	應答
7	主題
7	傳送
7	其他
7	可能
7	執行
7	安全
7	定的
7	序列
7	描述
7	標準
7	狀態碼
7	的方
7	連結
7	錯誤
6	Transfer
6	server
6	內容
6	冪等
6	多個
6	定版本
6	應當
6	某個
6	的資源
6	請求序列
6	連線
6	都是
5	HEAD
5	IETF
5	W3C
5	file
5	html
5	hypertext
5	sip
5	代理伺服器
5	協定中
5	因此
5	所有
5	持續
5	採用
5	方式
5	檔案
5	沒有
5	版本號
5	用於
5	的方法
5	第一
5	能夠
5	處理
5	訊息
5	請求的
5	資源的
5	這個請求
5	閱論編
4	Application
4	DELETE
4	OPTIONS
4	Open
4	POST
4	PUT
4	aaa
4	data
4	scheme
4	不應
4	不支援
4	任何
4	伺服器傳
4	作為
4	其中
4	協定版本
4	參見
4	多個請求
4	實現
4	應的
4	持久
4	持續連線
4	接收
4	操作
4	更多
4	本體
4	發出
4	發布
4	空行
4	網路協定
4	網頁
4	規則
4	語意網
4	請求資
4	返回
4	這些
4	這個請求序列
4	通常
4	進行
3	CONNECT
3	DOM
3	Found
3	HTML5
3	HTTPS
3	IP
3	James
3	OK
3	Portlet
3	TRACE
3	W3.org
3	WebSocket
3	identifier
3	interface
3	ldap
3	resource
3	一種
3	上傳
3	伺服器應
3	但是
3	例子
3	修改
3	傳送請求
3	傳遞
3	允許
3	元資
3	全球資訊網
3	其它
3	列的
3	協定的
3	取代
3	可以在
3	可能會
3	向指定
3	安全方法
3	定版本號
3	定義
3	客戶
3	工作
3	工程
3	必須
3	應用程式
3	應該
3	成的
3	或者其
3	戶端請求
3	持久連
3	指定的
3	指定資源
3	提供
3	支援的
3	收到
3	方法都
3	是一
3	最佳化
3	服務
3	格式
3	次請求
3	比如
3	減少
3	瀏覽器
3	理程式
3	產生
3	當然
3	發起
3	的協定
3	的請求方法
3	相關
3	知識
3	短語
3	第一個
3	管道
3	而不
3	若干
3	請求時
3	請求資訊
3	請求頭
3	超文本傳輸協定
3	通訊
3	重複
3	開放
3	預設
3	顯示
2	Access
2	Apache
2	Audio
2	CRLF
2	Client-side
2	Database
2	Engineering
2	Force
2	GMT
2	Geolocation
2	Google
2	Hendler
2	Host
2	IDL
2	Internet
2	JSGI
2	JSON-LD
2	N-Triples
2	Notation
2	OSI
2	PATCH
2	PSGI
2	Passenger
2	Phusion
2	Rack
2	Reasons
2	SQL
2	SSL
2	Server-side
2	Task
2	Turtle
2	Version
2	WebCL
2	Wide
2	XML
2	address
2	bolo
2	dict
2	events
2	feed
2	ftp
2	geo
2	gopher
2	handler
2	images
2	imap
2	info
2	information
2	irc
2	javascript
2	logo.gif
2	mailto
2	message
2	mod_jk
2	mod_lisp
2	mod_mono
2	mod_parrot
2	mod_perl
2	mod_proxy
2	mod_python
2	mod_ruby
2	mod_wsgi
2	network
2	nntp
2	origin
2	pop
2	referer
2	rtsp
2	service
2	snmp
2	software
2	ssh
2	tag
2	telnet
2	tunnel
2	video
2	webcal
2	worker
2	www.google.com
2	wyciwyg
2	xfire
2	xmpp
2	一個空行
2	一個請求
2	不必
2	不應當
2	不支援對應的請求
2	並沒有
2	中的
2	中間
2	主條目
2	主要
2	之後
2	也就是
2	事實上
2	交握
2	代理程式
2	以及
2	伺服器上
2	伺服器中
2	伺服器傳送
2	伺服器在處理某個
2	伺服器應答
2	作為其
2	個檔案
2	個用戶端
2	個請求做成的請求
2	個請求後
2	個連接
2	假如
2	傳回
2	傳輸層
2	儲存
2	允許客戶端
2	元資料
2	分塊傳輸編碼
2	刪除
2	到伺服器
2	到的
2	則在
2	功能
2	加密
2	動態
2	協定例子
2	協定概述
2	參考
2	取得
2	名稱
2	向伺服器
2	向指定資源
2	周期
2	器的
2	回應的
2	因此也
2	在不
2	在多個
2	在於
2	在網
2	在請求
2	在通訊中指定版本
2	執行這個
2	壓縮
2	外部連結
2	如在
2	如某個
2	媒體資
2	字組成
2	它的
2	安全的
2	官方
2	定義了
2	容器
2	容的
2	對應的請求方法的
2	層協定
2	已經
2	干個請求做成的請
2	序列的
2	廣泛
2	建立
2	式的
2	引入了
2	很多
2	應用層
2	應當被
2	應當返回狀態碼
2	應的請求方法的時
2	應答的
2	成功
2	我們稱這個
2	或者其它
2	戶端在
2	所有的
2	持久連接
2	指令碼
2	指定埠
2	指定的資源
2	按鈕
2	接受
2	控制
2	描述狀態的短語
2	描述邏輯
2	提交
2	提姆
2	援對應的請求方法
2	搜尋
2	擴充
2	支援對應的請求方
2	數字
2	方案
2	方法應
2	方法都是
2	於該
2	是一個
2	是冪等的
2	是在
2	時間
2	有副作用
2	本文
2	架構
2	柏內茲
2	標識
2	正式發
2	此外
2	求做成的請求序列
2	活躍
2	測試
2	源伺服器
2	無法
2	版本號的
2	狀態程式碼
2	用到
2	用戶代理
2	用戶端發起一個
2	用戶端請求
2	用的
2	由於
2	當前
2	發生
2	的一個
2	的傳
2	的內容
2	的區別
2	的協定版本
2	的實現
2	的情況下
2	的應用
2	的操作
2	的方式
2	的是
2	的標準
2	的狀態
2	的第一
2	的結果
2	的語意
2	的請求方法的時候
2	目錄
2	相同或者
2	相關主題
2	空格
2	符合
2	第一行
2	管理
2	管道方式
2	組織
2	統一資源
2	維基
2	網路上
2	網路應用程式
2	網際網路協定
2	網際網路工程任務
2	網頁瀏覽器
2	繼續
2	能是
2	自訂
2	若干個請求做成的
2	著一
2	行的
2	表示
2	被伺服器接收
2	該資源
2	認為
2	認證
2	語法
2	請求伺服器
2	請求做成的請求序
2	請求已
2	請求行
2	資料庫
2	路負
2	送多個請求
2	這一
2	這些請求
2	這個方法可
2	通常是
2	通訊中指定版本號
2	通過
2	連線的
2	部份
2	部分
2	都是可選的
2	都是向
2	重新
2	錯誤或者
2	開發
2	除了
2	際網路工程任務組
2	需要
2	頭欄位
2	頻寬
2	類似協定"""
	mapping = []
	for line in freq.split('\n'):
		pair = line.split('\t')
		pair.reverse()
		mapping.append(pair)
	js_list = repr(mapping)
	return render_template("result.html", mapping=js_list, org_text=text, fname=file_name)

	
if __name__ == "__main__":
	# start up the web server
	app.run(port=8080, debug=True)