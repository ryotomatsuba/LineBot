import re
import MeCab
from collections import deque
import random
class LineFriend:
    def __init__(self,talk_file_pass):

        self.name=re.findall('(?<=\[LINE\] ).*?(?=とのトーク)',talk_file_pass)[0]
        with open(talk_file_pass, encoding='utf-8') as f:
            self.raw_talk_text = f.read()
        self.remarks =[sentence.split("\t") for sentence in self.raw_talk_text.split("\n") if len(sentence.split("\t"))==3]
        #remarks=[['12:33', '松葉 亮人', 'んー'], ['12:33', '松葉 亮人', 'じゃあ2500っていっとけば'], ['16:32', '髙橋陵太', 'そうだな']]
        self.talking_with=self.name_talking_with()
        self.sentences=self.remarks2ones_sentences(self.name)
        self.sentence_model=self.make_sentence_model(self.sentences)
        self.reply_model=self.make_reply_model(sender=self.talking_with,replier=self.name)
        greeting=self.make_sentence(replier=self.name,sentence_model=self.sentence_model,reply_model=self.reply_model)
        print(greeting)
    def remarks2ones_sentences(self,person_name):
        sentences=[remark[2] for remark in self.remarks if remark[1]==person_name]
        return sentences
    def name_talking_with(self):#トークファイルの会話相手の名前を取得
        names=set([remark[1] for remark in self.remarks if remark[1]!=self.name])
        names.discard('')
        if len(names)>1:
            print("あなたは　：",names)
        else:
            return names.pop()
    def wakati_sentence(self,sentence):#文を単語ごとに分ける
        #['明日', 'は', '晴れ', 'か', 'なあ', '\n']
        if sentence in ["[スタンプ]","[写真]"]:
            return [sentence,"\n"]
        t = MeCab.Tagger("-Owakati")
        parsed_text =t.parse(sentence)
        wordlist = parsed_text.rstrip("\n").rstrip(" ").split(" ")+['\n']
        return wordlist
    def make_sentence_model(self,ones_sentences):#LineFriendが文章を作るのに使う辞書
        #次のような辞書を作りたい{ ("今日", "は") : ["いい", "晴れ", "雨", ・・・] ,("は", "いい") : ["天気","気分","天気", ・・・],("いい","天気"):["です","だ","だ",・・・], ・・・}
        sentence_model = {}
        queue = deque([], 2)#2個しか入らないリストみたいなもの
        for sentence in ones_sentences:
            queue.append("[Begin]")#queue=["[Begin]",]
            for markov_value in self.wakati_sentence(sentence):
                if len(queue) == 2:
                    markov_key = tuple(queue)      
                    if markov_key not in sentence_model:
                        sentence_model[markov_key] = []
                    sentence_model[markov_key].append(markov_value)
                queue.append(markov_value)#次の処理に移る。
            
            queue.clear()
        return sentence_model
    def make_reply_model(self,sender,replier):#senderからrecieverへの返信用辞書
        #作成するのは{'ゆく': ['ご飯'], 'な': ['微']}といったような辞書
        reply_model={}
        for i in range(len(self.remarks)-1):
            sender_remark=self.remarks[i]
            replier_remark=self.remarks[i+1]
            if sender_remark[1]==sender and replier_remark[1]==replier:
                last_sender_sentence=self.wakati_sentence(sender_remark[2])[-2]
                if last_sender_sentence not in reply_model.keys():
                    reply_model[last_sender_sentence]=[]
                reply_model[last_sender_sentence].append(self.wakati_sentence(replier_remark[2])[0])
        return reply_model
    def make_sentence(self,replier=None,reply_to=None,sentence_model=None,reply_model=None,max_words = 100): 
        if not replier:
            replier=self.talking_with
        if not sentence_model:
            sentence_model=self.sentence_model
        if not reply_model:
            reply_model=self.reply_model
        sentence=""
        if reply_to:
            last_of_reply_to=self.wakati_sentence(reply_to)[-2]
        
        if reply_to and last_of_reply_to in [key for key in reply_model.keys()]:
            key_candidates = [key for key in sentence_model.keys() if key[0] == "[Begin]" and key[1] in reply_model[last_of_reply_to]]
        else:
            key_candidates = [key for key in sentence_model.keys() if key[0] == "[Begin]"]
        if not key_candidates:
            print("Not find Keyword")
            print("reply_model　for %"%last_of_reply_to,reply_model[last_of_reply_to])
            return
        markov_key = random.choice(key_candidates)
        queue = deque(list(markov_key), 2)
        sentence = "".join(markov_key)
        for _ in range(max_words):
            markov_key = tuple(queue)
            next_word = random.choice(sentence_model[markov_key])
            sentence += next_word
            queue.append(next_word)
            if next_word == "\n":
                return sentence.strip().strip('[Begin]')


