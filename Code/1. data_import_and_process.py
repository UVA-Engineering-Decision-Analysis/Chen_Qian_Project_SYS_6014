# -*- coding:utf-8 -*-

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
    result = pd.DataFrame(columns=['name', 'tags', 'subscribedCount', 'playlist_id', 'tracks'])
    count = 0
    with open("./Data/netease_playlist_original_data.json", 'r', encoding='utf-8') as f:
        for line in f:
            result = result.append(parse_song_list(line), ignore_index=True)
            count += 1
            if count % 500 == 0:
                print(time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time())) + "Dealing with Playlist No. " + str(count))

    data_list_1 = result
    data_1 = data_list_1.drop('tracks', axis=1).join(
        data_list_1['tracks'].str.split('|', expand=True).stack().reset_index(level=1, drop=True).rename('Songs'))
    data_1 = data_1.dropna(subset=['Songs'], how='any')
    data_1 = data_list_1.drop('Songs', axis=1).join(
        data_list_1['Songs'].str.split(',', expand=True).stack().reset_index(level=1, drop=True))

    data_list_2 = data_1
    data_2 = data_list_2.dropna(subset=['Songs'], how='any')

    data_list_3 = data_2

    data_3 = data_list_3['Songs'].str.split(',', expand=True)
    data_list_3['song_id'] = data_3[0]
    data_list_3['song_name'] = data_3[1]
    data_list_3['artists'] = data_3[2]
    data_list_3['popularity'] = data_3[3]

    data_list_3 = data_list_3.drop('Songs', axis=1)
    data_list_3 = data_list_3.drop('Unnamed: 0', axis=1)
    data_list_3 = data_list_3.drop('Unnamed: 0.1', axis=1)
    data_list_3 = data_list_3.drop('Unnamed: 0.1.1', axis=1)

    data_list_3.to_csv("./Data/Processed_data_set.csv", encoding='utf-8')

    # In this case, this data set is so huge that my computer cannot build the model.
    # So I just choose the first 500000 rows data, which is enough for training
    sample_data = data_list_3.head(500000)
    data_set = sample_data[['playlist_id', 'song_id', 'popularity']]

    data_set.loc[:, 'playlist_id'] = pd.to_numeric(data_set['playlist_id'], downcast='signed', errors='coerce')
    data_set.loc[:, 'song_id'] = pd.to_numeric(data_set['song_id'], downcast='signed', errors='coerce')
    data_set.loc[:, 'popularity'] = pd.to_numeric(data_set['popularity'], errors='coerce')
    data_set = data_set.dropna(axis=0, how='any')
    data_set['playlist_id'] = data_set['playlist_id'].astype('int')
    data_set['song_id'] = data_set['song_id'].astype('int')
    data_set['popularity'] = data_set['popularity'].astype('int')

    data_set.to_csv("./Data/music_data_set.csv",encoding='utf-8')