#!/usr/bin/env python
# coding: utf-8

# # Defining API 
# 
# vworld Map에 조위/수온/기온을 그래프로 표시
# 
# **내부 라이브러리**
# * `map-basemap` &rarr; vworld map
# * `khoa-khoaOpenApi` &rarr; 바다누리행양정보 서비스 oepn api call

# In[6]:


# from khoa import khoaOpenApi
# from map import basemap
from . import khoaOpenApi
from . import basemap
import folium
import pandas as pd
import altair as alt
from datetime import datetime, timedelta


# #### 관측소 마커 생성

# In[7]:


def set_oceandata_marker(data_type, obs_code, obs_location, cur_date, time, ocean_data):
 #get Map
 map = basemap.getMap()  
 #데이터 to JSON
 source = pd.DataFrame(
     {
         '시간' : time,
         data_type : ocean_data
     }
 )
 #차트 생성
 title= cur_date + ':T'
 y = data_type + ':Q'
 chart = alt.Chart(source).mark_line().encode(x='시간', y=alt.Y(y, scale=alt.Scale(zero=False)),column=title)
 chart.configure_header(
    titleColor='green',
    titleFontSize=14
 )
 #차트 to JSON 변환
 vis1 = chart.to_json()
 #마커 및 팝업 생성
 circ_mkr = folium.CircleMarker(
    location=obs_location,
    radius=20,
    color='red',
    fill=True,
    fill_color='red',
    fillOpacity=1.0,
    opacity=1.0,
    tooltip=obs_code,
    popup=folium.Popup(max_width=400).add_child(folium.VegaLite(vis1, width=270, height=180))
 )
 # add to map
 circ_mkr.add_to(map)

 return map


# #### 지도 위에 해양정보 그리기

# In[8]:


def draw_oceandata(data_type, obs_code, date) :
 #해양정보 및 관측소 요청
 result = khoaOpenApi.getKhoaData(data_type, obs_code, date)
 #관측소
 obs_location = (result['result']['meta']['obs_lat'], result['result']['meta']['obs_lon'])
 #지정일
 cur_date = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
 #다음날
 next_date = datetime.strptime(date, '%Y%m%d') + timedelta(days=1)
 #조위/수온/기온 key 구하기
 keys = [key for key in result['result']['data'][0]]
 for k in keys:
    if k != 'record_time':
        key = k     
 #시간 및 해양정보 리스트
 time = []
 ocean_data = []      
    
 for i in result['result']['data']:
    dt = datetime.strptime(i['record_time'], '%Y-%m-%d %H:%M:%S')
    if dt.minute == 0:
        ocean_data.append(i[key])
        if dt.month == next_date.month and dt.day == next_date.day :
            time.append(24)
        else :
            time.append(dt.hour)  
    
 map = set_oceandata_marker(data_type, obs_code, obs_location, cur_date, time, ocean_data)

 return map


# ### 지도 to html

# In[9]:


def oceandata_to_html(data_type, obs_code, date) :
    print('-- oceandata_to_html start')
    map = draw_oceandata(data_type, obs_code, date)
    map.save( data_type + '_' + obs_code + '_' + date +'.html')
    print('-- oceandata_to_html end')


# ### 지도 display

# In[10]:


def display_oceandata(data_type, obs_code, date):
    map = draw_oceandata(data_type, obs_code, date)
    display(map)

