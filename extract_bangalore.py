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
	record=[]
	skipped=[]
	c=0
	for page in range(2,len(doc)-1):
	    img=np.array(doc[page])
	    bg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	    img = cv2.threshold(bg, 127, 255, cv2.THRESH_BINARY)[1]

	    for i in range(10):
		for j in range(3) :
		    d={}
		    crop_img = img[132+i*200:132+(i+1)*200, 55+j*501:55+(j+1)*501]    #mp rolls
		    
	

		    text=pytesseract.image_to_string(crop_img,lang="eng")
		    text=text.replace('Name','')
		    text=text.replace('Father\'s','')
		    text=text.replace('Husband\'s','')
		    text=text.replace('House No.','')
		    text=text.replace(':','')
		    text=text.replace('=','')
		    text=text.replace('!','')
		    text=text.replace('.',' ')
		    s=text.splitlines()
		    for ii in range(len(s)): s[ii]=s[ii].strip()
		    s=list(filter(None,s))
	#           print(s)
		    raw.append(s)
		    try:
		        
		        d['name']=s[1]
		        d['father/husband']=s[2]
		        d['house']=s[3]
		        d['age']=[int(p) for p in s[4].split() if p.isdigit()]
		        d['sex']='M' if any('Male' in mys for mys in s) else 'F'
		        record.append(d)
	#	        print(d)
		    except:
		        skipped.append(s)
	return record

def WriteDictToCSV(csv_file,csv_columns,dict_data):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)

path='filename.pdf'
record=get_info(path)
currentPath=os.getcwd()
csv_file=currentPath+'/filename.csv'
csv_columns=['name','father/husband','house','age','sex']
WriteDictToCSV(csv_file,csv_columns,record)
