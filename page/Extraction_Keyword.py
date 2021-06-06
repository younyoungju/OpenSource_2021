#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#my_file = 이미지 파일 경로 이름
def ocr_text(my_file):
    import cv2
    import pytesseract
    import numpy as np
    import os
    import pdftotext

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    
    file_path = os.path.splitext(my_file)[1]
    if file_path=='.png' or file_path=='.jpg':
        image_file = cv2.imread(my_img)
        img_gray = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
        my_text = pytesseract.image_to_string(img_gray, lang='kor')

    if file_path=='pdf':
        with open(my_file, "rb") as f:
            text_file=pdftotext.PDF(f)
        my_text = text_file.read()
    
    return my_text


# In[72]:


#텍스트 import , encoding
#text = upload_files("input_text1.txt")

def upload_files(file_name):
    print("upload_files")
    with open(file_name) as file_object:
        texts = file_object.read()
        #texts = open(file_name,"r", encoding='euc-kr')
    return texts


# In[73]:


def preprocessing_text(texts):
    #초기 실행시 아래 pip 다 실행해야함!
#     !pip install git+https://github.com/ssut/py-hanspell.git
#     !pip install konlpy
#     !pip install krwordrank
    #오류 발생시 : https://data-scientist-brian-kim.tistory.com/79 침고
    
    print("preprocessing_text")
    from hanspell import spell_checker
    from tqdm.notebook import tqdm
    from konlpy.tag import Twitter
    from collections import Counter
    from krwordrank.hangle import normalize


    nlpy = Twitter()
    
#     lines = [line.rstrip('\n') for line in texts]
    lines = texts.splitlines()
    nouns_word = [] #명사 단어 추출
    normalized_lines = []
    for each_line in tqdm(lines):
        each_line = each_line.replace("\x0c", "") #json을 로드 하면서 생기는 특수문자 제거
        each_line = normalize(each_line, english=True, number=True) #특수문자 제거
        each_line = spell_checker.check(each_line).checked #맞춤법 틀린게 있다면 고쳐줌
        nouns_word = nouns_word + nlpy.nouns(each_line) # 명사 단어 추출
        normalized_lines.append(each_line)
    
    return lines, nouns_word, normalized_lines

#lines : text를 단순히 \n 기준으로 split 한 것
#nouns_word : 각 문장에서 명사 단어
#normaliezed_lines : 맞춤범 검사, 특수 기호 제거 된 문장


# In[74]:


#추출된 명사에서 빈도수 세기
def count_noun(nouns_word):
    print("count_noun")
    import pandas as pd
    from collections import Counter
    count = Counter(nouns_word)

    tag_count = []
    tags = []

    #길이가 2부터 49까지인 단어 
    for n, c in count.most_common():
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2 and len(tags) <= 49:
            tag_count.append(dics)
            tags.append(dics['tag'])
        
    noun_count_df = pd.DataFrame(tag_count)
    
    return noun_count_df

#컬럼이 tag와 count로 된 dataframe 변환


# In[75]:


#한글 단어의 중요도 순위 측정
def extract_krwordrank(normalized_lines, noun_count_df):
    import pandas as pd 
    
    print("extract_krwordrank")
    from krwordrank.word import KRWordRank

    wordrank_extractor = KRWordRank(
        min_count = min(noun_count_df["count"]), # 단어의 최소 출현 빈도수
        max_length = max(noun_count_df["tag"].str.len()), # 단어의 최대 길이
        verbose = True
        )

    beta = 0.85    # PageRank의 decaying factor beta
    max_iter = 10

    #keywords는 filtering이 적용된 L parts
    #rank는 substriing graph의 substring에 대한 구마
    #graph는 substring graph
    keywords, rank, graph = wordrank_extractor.extract(normalized_lines, beta, max_iter)
    
    keyword_df = pd.DataFrame(list(keywords.items()),columns=['word', 'rank'])
    
    return keyword_df


# In[76]:


def make_wordlists(noun_count_df,keyword_df):
    print("make_wordlists")
    #["count"]>0 수를 조정하여 빈칸 채울 단어 갯수나 난이도를 조정할 수 있음
    frequency_noun_list = noun_count_df[noun_count_df["count"]>0]["tag"].tolist()
    keyword_list = keyword_df["word"].tolist()
    return frequency_noun_list,keyword_list


# In[77]:


#frequency_noun_list 기준으로 빈칸을 생성했을 때

def __test_by_frequency_noun__(frequency_noun_list):
    print("__test_by_frequency_noun__")
    test_by_frequency_noun = []
    for each_line in lines:
        for word in each_line.split():
            if word in frequency_noun_list:
                each_line = each_line.replace(word, "□"*len(word))
        test_by_frequency_noun.append(each_line)
        
    return test_by_frequency_noun


# In[78]:


# keyword_list 기준으로 빈칸을 생성했을 때
def __test_by_keyword_list__(keyword_list):
    print("__test_by_keyword_list__")
    test_by_keyword_list = []
    for each_line in lines:
        for word in each_line.split():
            if word in keyword_list:
                each_line = each_line.replace(word, "□"*len(word))
        test_by_keyword_list.append(each_line)
    
    return test_by_keyword_list


# In[91]:


# 한 문장에 3개 이상 빈칸이 오지 않도록 갯수 조정

def __test_limit_count__(lines, frequency_noun_list,keyword_list, keyword_df):
    import pandas as pd
    print("__test_limit_count__")
    test_limit_count = []
    for each_line in lines:
        replace_word = []
        for word in each_line.split(' '):
            if word in keyword_list:
                replace_word.append(word)

        #한 문장에 빈칸이 3개 이상일때
        if len(replace_word) > 2:
            A = pd.DataFrame()
            pattern = '|'.join(replace_word)
            A = keyword_df[keyword_df['word'].str.contains(pattern, case=False)]
            replace_word = A[:3].word

        for i in replace_word:
            each_line = each_line.replace(i,"□"*len(i))

        test_limit_count.append(each_line)
        
    return test_limit_count


# In[92]:


def __main__():
    print("__main__")
    #input_file = 파일 경로
    texets = ocr_text(input_file)

    lines, nouns_word, normalized_lines = preprocessing_text(texts)
    noun_count_df = count_noun(nouns_word)
    keyword_df = extract_krwordrank(normalized_lines, noun_count_df)
    frequency_noun_list,keyword_list = make_wordlists(noun_count_df,keyword_df)
    test_by_keyword_list = __test_by_frequency_noun__(frequency_noun_list)
    #print(test_by_keyword_list)
    test_by_keyword_list= __test_by_keyword_list__(keyword_list)
    #print(test_by_keyword_list)
    test_limit_count = __test_limit_count__(lines, frequency_noun_list,keyword_list, keyword_df)
    #print(test_limit_count)
    
    #text_file = 텍스트 파일 저장 경로
    f = open(text_file, 'w', encoding='UTF-8')
    f.write(test_limit_count)
    f.close()
    


# In[93]:


def __check__():
    print("되나")


# In[94]:


__main__()


# In[ ]:




