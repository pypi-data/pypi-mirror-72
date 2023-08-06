#!/usr/bin/env python
# coding: utf-8

# # Defining API 
# 
# 바다누리해양정보 서비스 (조위/수온/기온) Open API Call
# 
# **url**
# http://www.khoa.go.kr/oceangrid/khoa/takepart/openapi/openApiKey.do

# In[72]:


import requests
from pandas import Series, DataFrame
import pandas as pd
from datetime import datetime, timedelta
import json


# In[73]:


#open api url 인자
#데이터종류
data_types = {
    'tideObs':{ 'id':'tideObs', 'name':'조위'},
    'tideObsTemp':{ 'id':'tideObsTemp', 'name':'수온'},
    'tideObsAirTemp':{ 'id':'tideObsAirTemp', 'name':'기온'}, 
}
#인증키
service_key='zxOUtrRgW2bWzNEUuqSMA=='
#관측소
obs_codes = {
    'DT_0001':{'id':'DT_0001', 'name':'인천'},
    'DT_0002':{'id':'DT_0002', 'name':'평택'},
    'DT_0003':{'id':'DT_0003', 'name':'영광'},
    'DT_0004':{'id':'DT_0004', 'name':'제주'},
    'DT_0005':{'id':'DT_0005', 'name':'부산'},
    'DT_0006':{'id':'DT_0006', 'name':'묵호'},
    'DT_0007':{'id':'DT_0007', 'name':'목포'},
    'DT_0008':{'id':'DT_0008', 'name':'안산'},
    'DT_0009':{'id':'DT_0009', 'name':'포항'},
    'DT_0010':{'id':'DT_0010', 'name':'서귀포'}
}
#검색기준날짜
date = ''
#결과타입
result_type = 'json'


# ### Data Type Get API

# In[74]:


#정보타입 리스트
def getDataType():
 data_type_Id = []
 data_type_name = []
 for id in data_types:
    data_type_Id.append(data_types[id]['id'])
    data_type_name.append(data_types[id]['name'])
 data = { '해양정보' : data_type_name, '아이디' : data_type_Id }
 frame = DataFrame(data)
 display(frame)

#이름 to 코드
def get_data_type_code(data_type_name) :
    for id in data_types:
        if data_types[id]['name'] == data_type_name:
            return data_types[id]['id']


# ### Obs Code Get API

# In[75]:


#관측소 리스트
def getObsCode():
 obs_code = []
 obs_name = []
 for id in obs_codes:   
    obs_code.append(obs_codes[id]['id'])
    obs_name.append(obs_codes[id]['name'])
 data = { '관측소' : obs_name, '아이디' : obs_code }
 frame = DataFrame(data)
 display(frame)

#이름 to 코드
def get_obs_code(obs_name) :
    for id in obs_codes:
        if obs_codes[id]['name'] == obs_name:
            return obs_codes[id]['id']


# ### khoa Data Get API

# In[76]:


def getKhoaData(data_type_name, obs_name, date):
    if validation(data_type_name, obs_name, date) == False : 
        return False
    else :
        data_type_code = get_data_type_code(data_type_name)
        obs_code = get_obs_code(obs_name)
        url = 'http://www.khoa.go.kr/oceangrid/grid/api/%s/search.do?ServiceKey=%s&ObsCode=%s&Date=%s&ResultType=%s'%(data_type_code, service_key, obs_code, date, result_type)
        print('url: %s'%url)
        #request
        resp = requests.get(url);
        resp.raise_for_status();
        data = resp.json()
        
        return data;


# ### variable Validation API
# ##### :정보타입, 관측소, 날짜  validation

# In[77]:


def validation(data_type_name, obs_name, date):
    #정보타입 확인
    if check_dataType(data_type_name) == False :
        print('데이터타입이 틀립니다: ' + data_type_name )
        print('아래에서 선택해주세요!')
        getDataType()
        return False
    #관측소 확인
    if check_Obs(obs_name) == False :
        print('관측소가 틀립니다: ' + obs_name )
        print('아래에서 선택해주세요!')
        getObsCode()
        return False
      #날짜 확인
    try:
        a = datetime.strptime(date, '%Y%m%d')
    except ValueError:
        print('날짜형식이 틀렸습니다: ' + date)
        print('YYYYMMDD 형식으로 입력해주세요!')
        return False
     
    return True

#정보타입 확인
def check_dataType(data_type_name) :
    for id in data_types:
        if data_types[id]['name'] == data_type_name:
            return True
    return False

#관측소 확인
def check_Obs(obs_name) :
    for id in obs_codes:
        if obs_codes[id]['name'] == obs_name:
            return True
    return False


# In[79]:


# try: 
#     result = getKhoaData('조위', '평택', '20200620')
#     print(json.dumps(result, indent="\t"))
# except TypeError:    
#     print('인자를 확인해주세요')

