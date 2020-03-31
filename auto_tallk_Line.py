from LineFriend import LineFriend
import sys
file_pass=sys.argv[1]

friend=LineFriend(file_pass)

while True:
    message=input('メッセージを入力: ')
    if message=="終わり":
        break
    sentence = friend.make_sentence(reply_to=message,replier=friend.name)
    print(sentence)

