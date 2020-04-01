import pickle
from LineFriend import LineFriend
import sys
from werkzeug.utils import secure_filename

def save_LineFriend(file_pass):
    friend=LineFriend(file_pass)
    with open('pickle_file/yoru.binaryfile','wb') as f:
        pickle.dump(friend,f)

if __name__ == "__main__":
    #save_LineFriend('uploads/[LINE] 髙橋陵太とのトーク.txt')
    save_LineFriend('uploads/[LINE] YUKI HIROTAとのトーク.txt')