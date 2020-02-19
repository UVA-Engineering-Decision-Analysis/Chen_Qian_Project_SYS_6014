# -*- coding:utf-8 -*-
"""
@author:Chen Qian
@file:Data_Process.py
@time:2020-02-1802:00
"""
import pandas as pd


data_list_1 = pd.read_csv("/Users/chen/学习/项目资料/机器学习实战项目/第01课/163_music_playlist.csv")
data_1 = data_list_1.drop('tracks', axis=1).join(data_list_1['tracks'].str.split('|', expand=True).stack().reset_index(level=1, drop=True).rename('Songs'))
data_1 = data_1.dropna(subset=['Songs'],how='any')
data_1 = data_list_1.drop('Songs', axis=1).join(data_list_1['Songs'].str.split(',', expand=True).stack().reset_index(level=1, drop=True))


data_list_2 = data_1
data_2 = data_list_2.dropna(subset=['Songs'],how='any')


data_list_3 = data_2

data_3 = data_list_3['Songs'].str.split(',',expand=True)
data_list_3['song_id']=data_3[0]
data_list_3['song_name']=data_3[1]
data_list_3['artists']=data_3[2]
data_list_3['popularity']=data_3[3]

data_list_3 = data_list_3.drop('Songs', axis=1)
data_list_3 = data_list_3.drop('Unnamed: 0', axis=1)
data_list_3 = data_list_3.drop('Unnamed: 0.1', axis=1)
data_list_3 = data_list_3.drop('Unnamed: 0.1.1', axis=1)

data_list_3.to_csv("/Users/chen/学习/项目资料/机器学习实战项目/第01课/Processed_data_set.csv",encoding='utf-8')
