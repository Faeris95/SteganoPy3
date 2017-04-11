#!/usr/bin/python3
# coding : utf-8
import random
from collections import Counter
class NumberGenerator():
    def __init__(self,size,sizeTxt, key = None):
        self.size = size
        self.size_txt = sizeTxt
        if(key):
            self.key = key
        else:
            self.key = random.randrange(1000000000000,2000000000000)
            with open("key.txt","w") as f:
                f.write(str(self.key))

    def generate_list(self):
        pixels_list=[]
        new_key = self.key
        i=0
        while(i<self.size_txt):
            new_key = new_key * 1103515245 + 12345;
            new_key = (new_key // 65536) % 32768;
            if not ((new_key%self.size[0],new_key%self.size[1])) in pixels_list:
                pixels_list.append((new_key%self.size[0],new_key%self.size[1]))
                i+=1

        print(Counter(pixels_list))
        print(len(pixels_list))






