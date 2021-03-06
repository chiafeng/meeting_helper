from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import six

import jieba
import jieba.analyse

def jieba_keyword(text):
	jieba.set_dictionary('dict.txt')
	jieba.analyse.set_stop_words("stop_words.txt")

	# TF-IDF
	tags = jieba.analyse.extract_tags(text, topK=20, withWeight=True, allowPOS=('a', 'e', 'eng', 'i', 'j', 'l', 'n', 'ns', 'nr', 'nt', 'nz', 't', 'vn', 'v', 'un'))
	for tag in tags:
		print(u'{:<16}\t{:8}'.format(tag[0], tag[1]))

	print('=' * 20)

	# TextRank
	tags = jieba.analyse.textrank(text, topK=20, withWeight=True, allowPOS=('a', 'e', 'eng', 'i', 'j', 'l', 'n', 'ns', 'nr', 'nt', 'nz', 't', 'vn', 'v', 'un'))
	for tag in tags:
		print(u'{:<16}\t{:8}'.format(tag[0], tag[1]))

	print('=' * 20)
	# part of speech
	import jieba.posseg as pseg
	words = pseg.cut(text)
	for word, flag in words:
		print('({}, {}) '.format(word, flag), end='')

def entities_text(text):
    """Detects entities in the text."""
    if len(text) == 0:
        return None

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    for entity in entities:
        print(u'{:<16}\t{:8}\t{}'.format(entity.salience, entity.name, entity_type[entity.type]))
        """print('=' * 20)
                                print(u'{:<16}: {}'.format('name', entity.name))
                                print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
                                print(u'{:<16}: {}'.format('metadata', entity.metadata))
                                print(u'{:<16}: {}'.format('salience', entity.salience))
                                print(u'{:<16}: {}'.format('wikipedia_url',
                                      entity.metadata.get('wikipedia_url', '-')))"""

    return entities


if __name__ == '__main__':
    text = """台大好我想在這個我是一個音樂工作者的更準確的時候我是一名饒舌歌手我在大學時候我就讀的是台大電機系畢業然後我也是一直亂傳數學一個阿宅男朋友聽到的問我說你覺得這樣愛你很衝突嗎這樣他看到看到這個影片一樣兩個概念很對立嗎I
    P撕裂痕是否抓住這兩個學業和音樂的時候雙頭的馬車全素的奔馳江省著拉著活活被分屍講但我最後專輯有做一些結論
    刺青
    我在想去刺青我想在左手和右手分別是上兩個不一樣的圖騰我朋友聽不了啦就是先吃裡面然後再慢慢往外次最後才知道露出來那邊看到的地方你知道他幾近還是我跟他們講完我的理由以後他們好像也沒有說服了所以我跟他講講看我想要在左手
    這是這句的韻律操我們用數學物理的明確的把它三個元素講出來第一個就是有不一樣的隱藏者是我講話有時候可以嗎有時候很快就是每一個字的不同的影響會組成這個韻律應該就是有時候我會想要強調智慧好像去或是情緒低落的時候說要講一
    術的成就上面是在左手上網裡面試然後把我在學術的成就上次在我的右手往裡面吃這樣
    在有沒睡喔那我要看一下左手是三個東西到底是什麼東西應該很無線這是三個數學符號教我變大玩一下思想實驗好了她先猜猜看這東西分別代表什麼東西聆聽我專輯不要給你那是什麼空還是代表示重重生從零開始代表是什麼可能是不熟悉數學
    最後會跟他分享一下我要帶他看這個月前面就是我們的右手我在我這個我在研究到底在做什麼東西啊其實我在做的研究室跟語音合成相關語音合成什 烈的過程分裂他會從一開始的單一個體就是裡面他會染色體複製中銀行南紡錘絲專頁的那個值得吃到飽後然後往外擴散變成是激將分裂為二但還是唯一的個體就像是上面這個樣子看看有無限所以前就是一開始的個體在正中間行程是到板無線就2概念的拉當然我在不一樣的狀況下我可以改變這個商城的價格我可以改成就是在強調主持的時候我便我喜歡火影忍者不是他喜歡火影忍者為什麼要改變瘦時不是風影忍者這樣子今天我要的話我可能反過來變成往上移除天要告白我先這就是不同
    扯到我今天主要想分享是中間的主線任務出現概念分別是林無名火災凶宅和
    現白肌撕裂的跟他分享的想要講的主題就是在夢和現實世間夢想和現實之間的拉扯你是怎麼樣得到平衡取得交給您為國家講說當我還沒有開始做的時候會很多憧憬很多衝進發師兄在作主打歌裡面就在講自己自己覺得自己好像又可以做音樂又可IP撕裂痕是否抓住這兩個學業和音樂的時候雙頭的馬車全素的奔馳江省著拉著活活被分屍講但我最後專輯有做一些結論 韻律學就是我們可以用很科學的方式分解我們的PO那接下來我要講為什麼饒舌歌聽起來會像饒舌不像數來寶就
    最後會跟他分享一下我要帶他看這個月前面就是我們的右手我在我這個我在研究到底在做什麼東西啊其實我在做的研究室跟語音合成相關語音合成什麼來就是間給電腦看大量的文字以後讓電腦去學出來怎麼樣去講這句話最早的就讓你的會議通Siri生日都初音樂做越好那我在做的研究領域中又是更這裡面的水果在做韻律鞋的部分是什麼呢我今天舉個例子監我說他好我是熊仔很高興來到tetris我這句的韻律教室能就會 
    這是這句的韻律操我們用數學物理的明確的把它三個元素講出來第一個就是有不一樣的隱藏者是我講話有時候可以嗎有時候很快就是每一個字的不同的影響會組成這個韻律應該就是有時候我會想要強調智慧好像去或是情緒低落的時候說要講一
    我的一種做法師是誰說玩樂的小孩不會變壞好至少有像蛇一個做法我們隨便想一個450000元的小孩不會變壞的三個的話我去觀察他原本的運本的刪掉價格他又沒事是誰說玩音樂的小孩不會變壞別個玩音樂的起來的小孩下去不 
    江華柯南大家聽不太懂會變成怪怪的為什麼是因為他們的應該沒有寫好字因為是在其他語言中不要吵這個概念因為我們的語言有平上去入也就是得等一個音聲調不同但是我們又不能直接去唸這些聲調為什麼我舉例如果今天我姐念說我喜歡火影2
    這樣的東西我已經改變是誰說玩音樂的小孩不會變壞跟播中文音樂下載變成貼好像有在炒熱氣氛的感覺有沒有水就是如何活用那個應力學來幫助你的手變得更厲害學院派這就是我在兩個領域中的少的嬌妻喝就是迴避問題喔你就是想要拿這些小y話我們通常會有高到低所以我們會喜歡
    火影忍者當然我在不一樣的狀況下我可以改變這個商城的價格我可以改成就是在強調主持的時候我便我喜歡火影忍者不是他喜歡火影忍者為什麼要改變瘦時不是風影忍者這樣子今天我要的話我可能反過來變成往上移除天要告白我先這就是不同
    我這個是在講什麼意思呢就是像他一台看到 
    有嗎還是沒有發現我們就要找這個交期囉有聽過佛是什麼嗎然後說自己很厲害自己的超酷播很平淡但是我是什麼東西就是給你去了誰歌詞你要怎麼把他唱出來就是說那我朋友的啊他講得很好他說的就是文字的旋律
    吃牛怎麼唱這個文字嗎不是說我們去掉文字以後剩下來的東西不是蚊子的旋律的風是什麼就是沒錯打破它概念出來就是韻律學就是我們可以用很科學的方式分解我們的PO那接下來我要講為什麼饒舌歌聽起來會像饒舌不像數來寶就是因為我沒有2號11巷音樂了一個做法一個PO之後我不去管我原本的英高我就常聽說現在很流行的Windows授他們的是任何人都可能
    烈的做法我可以先想好一個PO之後我不去管我原本的英高我就常聽說現在很流行的Windows授他們的是任何人都可能有沒有歌詞是張清芳忙了金曲獎躺著中槍了這個我可能就會忘記聽你就會你沒有辦法聽得懂我在講什麼東西甚至少聽音樂的3種
    最後我希望未來我可以在左手的事情越是越裡面有什麼事情也越吃越裡面跟他相反最後才是在中間集合作是一個
    我的一種做法師是誰說玩樂的小孩不會變壞好至少有像蛇一個做法我們隨便想一個450000元的小孩不會變壞的三個的話我去觀察他原本的運本的刪掉價格他又沒事是誰說玩音樂的小孩不會變壞別個玩音樂的起來的小孩下去不會變壞天我不去壓
    這樣的東西我已經改變是誰說玩音樂的小孩不會變壞跟播中文音樂下載變成貼好像有在炒熱氣氛的感覺有沒有水就是如何活用那個應力學來幫助你的手變得更厲害學院派這就是我在兩個領域中的少的嬌妻喝就是迴避問題喔你就是想要拿這些小you are unique你就是你你 現實的啦這個東西只是聽錯了吧好了東西我跟他之後分享一段我在我的專輯裡面的行中間的歌詞它上面寫說是肝的問題不是你想成為誰而是最真的你要怎麼活得最美不必落入世俗對你的分類you are unique你就是你 
    未成分裂
    我這個是在講什麼意思呢就是像他一台看到那個圖上面寫的然後這個手提供載他為什麼你會有被拉扯的感覺呢因為是因為有很多的刻板印象外在的標籤說要是歌手就是應該要耍酷老師的歌手就是應該要戴帽子老師都說不能夠瀏海可能下載你就 
    是要在圖書館你就是不能出出來你就是不准聽音樂就是這些都是屬於對你的分類嗎可是我今天回來問我自己 
    我不是你認為的老師都是我也不是你認為的阿宅我就是我我就是熊仔這些是我喜歡的東西所以今天你跟你們有現場有人跟我一樣感到迷惘覺得你這兩個領域中被被拉扯找不到兩個領域中的交給你只要問你自己你是不是真的很熱愛你在做的這兩 
    件事情如果你真的很熱愛你就是你你為什麼分裂你不需要找到這兩件事情要交給因為你對這兩件事情的熱愛就是交 
    這就是為什麼你要去做這些事情你不需要管45對你的分類you are you need你就是你以為成分裂
    最後我希望未來我可以在左手的事情越是越裡面有什麼事情也越吃越裡面跟他相反最後才是在中間集合作是一個
    保有技術也有藝術的一個作品謝大家維修"""

    """整體看起來，雖然 Jieba 在一些小地方斷得沒有其他的好，但應該算是效果最符合預期的一個了，而且它好安裝又跑得快，單純做斷詞的話應該會是我的首選。

    第二個大概會選擇 HanLP，斷詞的結果也還算漂亮，雖然不好安裝，但執行速度算是跟 Jieba 相差不多。第三個會是 SnowNLP，雖然覺得它斷詞不夠漂亮，但因為它有情緒分析以及文章分類的功能，覺得往後應該還是會有不得不用它的時候。

    最後一個才是 Stanford NLP，斷得不漂亮，只要碰到沒聽過的詞，似乎傾向把它們拆成一個一個字，而且又難安裝，執行速度也慢，功能也沒有前兩個多……所以中文自然語言處理可能不會用到它，不過它英文的做出來的某些效果其實還不錯，所以英文的話也許還是有考慮的機會。"""
    entities_text(text)
    print('=' * 20)
    jieba_keyword(text)