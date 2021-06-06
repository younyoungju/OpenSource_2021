#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import pytesseract
import numpy as np
import os
import pdftotext

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# In[11]:


#최종 코드 함수

#my_file = 이미지 파일 경로 이름
def tes_ocr(my_file):
    file_path = os.path.splitext(my_file)[1]
    if file_path=='.png' or file_path=='.jpg':
        image_file = cv2.imread(my_img)
        img_gray = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
        gray_to_text = pytesseract.image_to_string(img_gray, lang='kor')
      
        #text_file = 텍스트 파일 저장 경로
        f = open(text_file, 'w', encoding='UTF-8')
        f.write(gray_to_text)
        f.close()
    if file_path=='pdf':
        with open(my_file, "rb") as f:
            text_file=pdftotext.PDF(f)
    
    return text_file


# In[ ]:




