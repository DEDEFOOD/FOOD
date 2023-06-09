# 코사인 유사도

from konlpy.tag import Komoran
import numpy as np
from numpy import dot
from numpy.linalg import norm


# 코사인 유사도 계산
def cos_sim(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1) * norm(vec2))
# 코사인 유사도 계산하는 함수
# norm : 벡터 크기 계산
# dot : 벡터 내적 계산

# TDM 만들기
def make_term_doc_mat(sentence_bow, word_dics):
    freq_mat = {}

    for word in word_dics:
        freq_mat[word] = 0

    for word in word_dics:
        if word in sentence_bow:
            freq_mat[word] += 1

    return freq_mat
# 문장에서 추출한 단어 사전을 기준으로 문장에 해당 단어들이 얼마나 
# 포함되어 있는지 나타내는 단어 문서 행렬 함수



# 단어 벡터 만들기
def make_vector(tdm):
    vec = []
    for key in tdm:
        vec.append(tdm[key])
    return vec
# 토큰들의 출현 빈도 데이터를 벡터로 만들어주는 함수


# 문장 정의
sentence1 = '6월에 뉴턴은 선생님의 제안으로 트리니티에 입학하였다'
sentence2 = '6월에 뉴턴은 선생님의 제안으로 대학교에 입학하였다'
sentence3 = '나는 맛잇는 밥을 뉴턴 선생님과 함께 먹었습니다.'


# 헝태소분석기를 이용해 단어 묶음 리스트 생성
komoran = Komoran()
bow1 = komoran.nouns(sentence1)
bow2 = komoran.nouns(sentence2)
bow3 = komoran.nouns(sentence3)

# 단어 묶음 리스트를 하나로 합침
bow = bow1 + bow2 + bow3


# 단어 묶음에서 중복제거해 단어 사전 구축
word_dics = []
for token in bow:
    if token not in word_dics:
        word_dics.append(token)
# 중복된 단어를 제거해 새로운 단어 사전 구축


# 문장 별 단어 문서 행렬 계산
freq_list1 = make_term_doc_mat(bow1, word_dics)
freq_list2 = make_term_doc_mat(bow2, word_dics)
freq_list3 = make_term_doc_mat(bow3, word_dics)
print(freq_list1)
print(freq_list2)
print(freq_list3)
# 각 문장마다 단어 문서 행렬을 만든다


# 코사인 유사도 계산
doc1 = np.array(make_vector(freq_list1))
# 각 문장마다 벡터를 생성해 넘파이 배열로 변환
doc2 = np.array(make_vector(freq_list2))
doc3 = np.array(make_vector(freq_list3))
# 유사도 계산
r1 = cos_sim(doc1, doc2)
r2 = cos_sim(doc3, doc1)
print(r1)
print(r2)



'''
{'6월': 1, '뉴턴': 1, '선생님': 1, '제안': 1, '트리니티': 1, '입학': 1, '대학교': 0, '맛': 0, '밥': 0, '선생': 0, '님과 함께': 0}
{'6월': 1, '뉴턴': 1, '선생님': 1, '제안': 1, '트리니티': 0, '입학': 1, '대학교': 1, '맛': 0, '밥': 0, '선생': 0, '님과 함께': 0}
{'6월': 0, '뉴턴': 1, '선생님': 0, '제안': 0, '트리니티': 0, '입학': 0, '대학교': 0, '맛': 1, '밥': 1, '선생': 1, '님과 함께': 1}
0.8333333333333335
0.18257418583505536


유사도를 보다 정밀하게 측정

'''