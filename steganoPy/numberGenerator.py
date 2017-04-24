#!/usr/bin/python3
# coding : utf-8
import time

class NumberGenerator():
    def __init__(self,size,size_txt, key = None):
        self.size = size
        self.size_txt = size_txt
        if(key):
            self.key = key
            print(self.key," ",self.size_txt)

        else:
            self.key = int(time.time())
            with open("key.txt","w") as f:
                f.write(str(self.key)+";"+str(self.size_txt))
        self.pixels_list = []
        self.generate_list()

    def generate_list(self):
        new_key = self.key
        i=0
        x=0
        y=0
        while(i<=self.size_txt):
            for j in range(2):
                new_key = (new_key * 9301 + 49297) % 233280
                if(j==0):
                    x=new_key%(self.size[0]-1)
                else:
                    y=new_key%(self.size[1]-1)
            if not ((x,y)) in self.pixels_list:
                self.pixels_list.append((x,y))
                i+=1
    def get_pixels_list(self):
        return self.pixels_list







