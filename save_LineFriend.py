import pickle
from LineFriend import LineFriend
import sys

def save_LineFriend(file_pass):
    friend=LineFriend(file_pass)
    with open('pickle_file/Takahasi.binaryfile','wb') as f:
        pickle.dump(friend,f)

if __name__ == "__main__":
    save_LineFriend('uploads/[LINE] 髙橋陵太とのトーク.txt')