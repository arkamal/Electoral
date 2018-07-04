#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 08:20:47 2018

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





def get_info(path):
        doc = pdf2image.convert_from_path(path)
        raw=[]
        rawtext=[]
        for page in range(2,len(doc)-1):
                print (page)
                img=np.array(doc[page])
                bg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                img = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY)[1]
                for i in range(10):
                    for j in range(3):
                        crop_img = img[200+i*188:200+(i+1)*188, 145+j*470:145+(j+1)*470]    #mp rolls
#                        crop_img = img[166+i*200:166+(i+1)*200, 64+j*518:64+(j+1)*518]     #up rolls
                        text= pytesseract.image_to_string(crop_img,lang="eng+hin")
                        new_text=''
                        for temp in range(len(text)):
                                t=ord(text[temp])
                                if t>=65 and t<=90 or t>=97 and t<= 122:
                                        continue       
                                new_text=new_text+text[temp]
                        text=new_text
                        s=text.splitlines()
                        for ii in range(len(s)): s[ii]=s[ii].strip()
                        s=list(filter(None,s))
                        if len(s)!=0:
                                print(s)
                                raw.append(s)
                                rawtext.append(text)
        return raw,rawtext

def cleanMP(raw):
        record=[]
        for i in range(len(raw)):
            d1={}
            try:
                if raw[i][0].find('ताम')==-1:
                    raw[i].remove(raw[i][0])
            except:
                print('Removed')
            try:
                d1['hname']=raw[i][0].split(':')[1].strip()#
                d1['name']=transliterate(raw[i][0].split(':')[1].strip(),DEVANAGARI,HK)
                d1['name']=d1['name'].replace('sinha','singh')
            except:
                d1['name']=''
            try:
                d1['hfather/husband']=raw[i][1].split(':')[1].strip()#
                d1['father/husband']=transliterate(raw[i][1].split(':')[1].strip(),DEVANAGARI,HK)
            except:
                d1['father/husband']=''
            try:
                d1['age']=''
                for x in range(len(raw[i][3])):
                    if ord(raw[i][3][x])>=48 and ord(raw[i][3][x])<=57:
                        d1['age']=d1['age']+raw[i][3][x]
                if len(d1['age'])!=2 : d1['age']=''
            except:
                d1['age']=''
            d1['sex']='M' if any('पुरूष' in myraw for myraw in raw[i]) else 'F'
#            print(d1)
            record.append(d1)
        return record

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
    
    


path='./filename.pdf'
raw,rawtext=get_info(path)
record=clean(raw)

currentPath=os.getcwd()
csv_file=currentPath+'/filename.csv'
csv_columns=['hname','name', 'hfather/husband','father/husband','age','sex']
WriteDictToCSV(csv_file,csv_columns,record)
