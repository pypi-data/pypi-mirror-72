#!/usr/bin/env python
# coding: utf-8

# In[11]:


import folium


# In[12]:


#vWorld Map
#api 인증키
key='AEFCF800-5FCC-39F3-B64E-E69FFB5B84C4'
maps = {
       'Vworld Base': folium.TileLayer(
           tiles = 'http://api.vworld.kr/req/wmts/1.0.0/%s/%s/{z}/{y}/{x}.png'%(key,'Base'),
           attr = 'vworld',
           name = 'vworld Base',
           overlay = False,
           control = True
       ),
       'Vworld Gray': folium.TileLayer(
           tiles = 'http://api.vworld.kr/req/wmts/1.0.0/%s/%s/{z}/{y}/{x}.png'%(key,'gray'),
           attr = 'vworld',
           name = 'vworld Gray',
           overlay = True,
           control = True,
           show = False
       ),
       'Vworld Midnight': folium.TileLayer(
           tiles = 'http://api.vworld.kr/req/wmts/1.0.0/%s/%s/{z}/{y}/{x}.png'%(key,'midnight'),
           attr = 'vworld',
           name = 'vworld Midnight',
           overlay = True,
           control = True,
           show = False
       ),
       'Vworld Hybrid': folium.TileLayer(
           tiles = 'http://api.vworld.kr/req/wmts/1.0.0/%s/%s/{z}/{y}/{x}.png'%(key,'Hybrid'),
           attr = 'vworld',
           name = 'vworld Hybrid',
           overlay = True,
           control = True,
           show = False
       ),
       'Vworld Satellite': folium.TileLayer(
           tiles = 'http://api.vworld.kr/req/wmts/1.0.0/%s/%s/{z}/{y}/{x}.jpeg'%(key,'Satellite'),
           attr = 'vworld',
           name = 'vworld Satellite',
           overlay = True,
           control = True,
           show = False
       )
   }
#Main Map Create
center = [37.640988, 127.193484]
zoom = 7


# In[13]:


def getMap() :
 my_map = folium.Map(location=center, zoom_start=zoom, tiles=None)    
 #vworld layer Add
 for m in maps:
    maps[m].add_to(my_map)
    
 #layer controll Add
 folium.LayerControl().add_to(my_map)

 return my_map


# In[ ]:


# display(my_map)


# In[ ]:


# define data for demonstration
# source = pd.DataFrame(
#     {
#         '시간': ['01', '02', '03'],
#         '수온': [100, 50, 120],
#     }
# )

# # create an altair chart, then convert to JSON
# chart = alt.Chart(source).mark_bar().encode(x='시간', y='수온')
# vis1 = chart.to_json()
# # create a marker, with altair graphic as popup
# circ_mkr = folium.CircleMarker(
#     location=(37.45198, 126.592111),
#     radius=20,
#     color='red',
#     fill=True,
#     fill_color='red',
#     fillOpacity=1.0,
#     opacity=1.0,
#     tooltip='인천',
#     popup=folium.Popup(max_width=400).add_child(folium.VegaLite(vis1, width=200, height=300))
# )

# # add to map
# circ_mkr.add_to(m)

