# -*- coding:utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from __future__ import (absolute_import, division, print_function, unicode_literals)
import csv

import pandas as pd

from surprise import dump

def playlist_data_preprocessing():
    csv_reader = csv.reader(open('./Data/playlist_id_to_name.csv'))
    id_name_dic = {}
    name_id_dic = {}
    for row in csv_reader:
        id_name_dic[row[1]] = row[2]
        name_id_dic[row[2]] = row[1]
    return id_name_dic, name_id_dic

predictions_knn, algo_knn = dump.load('./Model/k-NN Baseline')

df_knn = pd.DataFrame(predictions_knn, columns=['uid', 'iid', 'rui', 'est', 'details'])

print("Upload function dictionary from playlist id to playlist name...")
id_name_dic, name_id_dic = playlist_data_preprocessing()
print("Build dictionary successful...")

current_playlist_id = '363476047'
print('Current playlist id：' + current_playlist_id)

current_playlist_name = id_name_dic[current_playlist_id]
print('Current playlist name：' + current_playlist_name)

playlist_inner_id = algo_knn.trainset.to_inner_uid(int(current_playlist_id))
print('Current playlist training id：' + str(playlist_inner_id))

playlist_neighbors = algo_knn.get_neighbors(playlist_inner_id, k=5)
playlist_neighbors_id = (algo_knn.trainset.to_raw_uid(inner_id) for inner_id in playlist_neighbors)

# Transform playlist id to name
playlist_neighbors_name = (id_name_dic[str(playlist_id)] for playlist_id in playlist_neighbors_id)
print("The top 5 related playlist to <", current_playlist_name, '> is：\n')
for playlist_name in playlist_neighbors_name:
    print(name_id_dic[playlist_name],playlist_name)


