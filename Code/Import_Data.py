# -*- coding:utf-8 -*-
"""
@author:Chen Qian
@file:Import_Data.py
@time:2020-02-1723:03
"""
import json
import pandas as pd
import time

def parse_song_list(song_list):
    data = json.loads(song_list)
    name = data['result']['name']
    tags = ",".join(data['result']['tags'])
    subscribed_count = data['result']['subscribedCount']
    playlist_id = data['result']['id']
    song_info = ''
    songs = data['result']['tracks']
    for song in songs:
        song_info += "|" + str(song['id']) + "," + song['name'] + ","+ song['artists'][0]['name'] + "," + str(song['popularity'])
    return pd.DataFrame({'name': [name], 'tags': [tags], 'subscribedCount': [subscribed_count], 'playlist_id': [playlist_id],'tracks': [song_info]})


def parse_file(file_in, file_out):
    result = pd.DataFrame(columns=['name', 'tags', 'subscribedCount', 'playlist_id', 'tracks'])
    count = 0
    with open(file_in, 'r', encoding='utf-8') as f:
        for line in f:
            result = result.append(parse_song_list(line),ignore_index=True)
            count += 1
            if count % 500 == 0:
                print(time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))+"Dealing with Playlist No. " + str(count))
    result.to_csv(file_out,encoding='utf-8')


if __name__=="__main__":
    file_in = "/Users/chen/学习/项目资料/机器学习实战项目/第01课/playlist_detail_all.json"
    file_out = "/Users/chen/学习/项目资料/机器学习实战项目/第01课/163_music_playlist.csv"
    parse_file(file_in,file_out)