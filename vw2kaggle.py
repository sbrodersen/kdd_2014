#!/usr/bin/python
'''
file for kaggle competition KDD cup 2014 
http://www.kaggle.com/c/kdd-cup-2014-predicting-excitement-at-donors-choose/

author: sonja brodersen sonja.brodersen@gmail.com
 
usage: python vw2kaggle < infile > outfile
'''
import math
import sys

def main(argv):
    headerline = "projectid,is_exciting"
    print headerline
    for line in sys.stdin.readlines():
        row = line.strip().split(" ")
        print "%s,%f"%(row[1],zygmoid(float(row[0])))

def zygmoid(x):
    #I know it's a common Sigmoid feature, but that's why I probably found
    #it on FastML too: https://github.com/zygmuntz/kaggle-stackoverflow/blob/master/sigmoid_mc.py
    return 1 / (1 + math.exp(-x))


if __name__ == "__main__":
    main(sys.argv[1:])
    