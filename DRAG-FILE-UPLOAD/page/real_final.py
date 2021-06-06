#!/usr/bin/env python
# coding: utf-8

# In[5]:


#내 드라이브에 있는 파일 google drive에 업로드
from google.colab import files
myfile = files.upload()


# In[6]:


import io
import os
import pandas as pd
import numpy as np

file_name = list(myfile.keys())[0]

texts = open(file_name,"r", encoding='euc-kr')


# In[7]:


get_ipython().system('pip install git+https://github.com/ssut/py-hanspell.git')
get_ipython().system('pip install konlpy')
get_ipython().system('pip install krwordrank')

from hanspell import spell_checker
from tqdm.notebook import tqdm
from konlpy.tag import Twitter
from collections import Counter
from krwordrank.hangle import normalize


nlpy = Twitter()

lines = [line.rstrip('\n') for line in texts] #txt 파일을 개행문자 기준으로 splig

nouns_word = [] #명사 단어 추출
normalized_lines = []
for each_line in tqdm(lines):
    each_line = each_line.replace("\x0c", "") #json을 로드 하면서 생기는 특수문자 제거
    each_line = normalize(each_line, english=True, number=True) #특수문자 제거
    each_line = spell_checker.check(each_line).checked #맞춤법 틀린게 있다면 고쳐줌
    nouns_word = nouns_word + nlpy.nouns(each_line) # 명사 단어 추출
    normalized_lines.append(each_line)


# In[8]:


normalized_lines


# In[9]:


# 명사의 빈도수 계산
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


# In[10]:


import pandas as pd
noun_count_df = pd.DataFrame(tag_count)


# In[11]:


#명사 중 가장 긴 단어의 문자열 길이 
print("최장 단어 길이 ", max(noun_count_df["tag"].str.len()))
#명사 중 최소 출현 빈도 수
print("최소 출현 빈도 수 ", min(noun_count_df["count"]))


# In[12]:


frequency_noun_list = noun_count_df[noun_count_df["count"]>0]["tag"].tolist()


# In[13]:


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


# In[14]:


keyword_df = pd.DataFrame(list(keywords.items()),columns=['word', 'rank'])


# In[15]:


keyword_list = keyword_df["word"].tolist()


# In[16]:


test_by_frequency_noun = []
for each_line in lines:
    for word in each_line.split():
        if word in frequency_noun_list:
            each_line = each_line.replace(word, "□"*len(word))
    test_by_frequency_noun.append(each_line)


# In[17]:


test_by_frequency_noun


# In[18]:


test_by_keyword = []
for each_line in lines:
    for word in each_line.split():
        if word in keyword_list:
            each_line = each_line.replace(word, "□"*len(word))
    test_by_keyword.append(each_line)


# In[19]:


test_by_keyword


# In[22]:


test_restrict_count = []
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

    test_restrict_count.append(each_line)


# In[23]:


test_restrict_count


# In[24]:


lines


# In[ ]:




