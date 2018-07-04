#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 15:37:36 2018

@author: arka
"""

import PIL
from PIL import Image,ImageFilter
import cv2
import pytesseract
import pdf2image
import numpy as np
from sanscript import transliterate
import csv
import os


def WriteDictToCSV(csv_file,csv_columns,dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)



def get_info(path):
    doc = pdf2image.convert_from_path(path)
    
    raw=[]
    record=[]
    skipped=[]
    c=0
    for page in range(2,len(doc)-1):
        img=np.array(doc[page])
        bg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY)[1]
    #    cv2.imwrite('a.jpg',image)
        for i in range(10):
            for j in range(3) :
                d={}
                crop_img = img[174+i*198:174+(i+1)*198, 59+j*500:55+(j+1)*500-109]
                
    #            image=Image.fromarray(crop_img)
    #            image.show()
                text=pytesseract.image_to_string(crop_img,lang="hin")
    #           
                s=text.splitlines()
                for ii in range(len(s)): s[ii]=s[ii].strip()
                s=list(filter(None,s))
    #            print(s)
                raw.append(s)
                try:
                    if s[0].find('नाम')==-1:
                        s.remove(s[0])
                    d['name']=s[0].split(':')[1].strip()
                    d['father/husband']=s[1].split(':')[1].strip()
                    d['house']=s[2].split(':')[1].strip()
                    d['age']=[int(p) for p in s[3].split() if p.isdigit()][0]
                    d['sex']='M' if any('पुरुष' in mys for mys in s) else 'F'
                    record.append(d)
                    print(d)
                except:
                    skipped.append(s)
    return record


path='filename.PDF'
record=get_info(path)
currentPath=os.getcwd()
csv_file=currentPath+'/filename.csv'
csv_columns=['name','father/husband','house','age','sex']
WriteDictToCSV(csv_file,csv_columns,record)           
