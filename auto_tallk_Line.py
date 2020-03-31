from LineFriend import LineFriend

import pickle

with open('pickle_file/Takahasi.binaryfile', 'rb') as f:
    friend = pickle.load(f)
while True:
    message=input('メッセージを入力: ')
    if message=="終わり":
        break
    sentence = friend.make_sentence(reply_to=message,replier=friend.name)
    print(sentence)

