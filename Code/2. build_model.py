# -*- coding:utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from surprise import SVD,KNNBasic,KNNWithMeans,KNNBaseline,CoClustering,NormalPredictor
from surprise import Dataset
from surprise import Reader
from surprise import dump
from surprise.accuracy import rmse,mse,mae
from surprise.model_selection import KFold

from sklearn.metrics import mean_squared_error

df = pd.read_csv("./Data/music_data_set.csv")

df = df.loc[(df['popularity'] >= 0) & (df['popularity'] <= 100)]
# A reader is still needed but only the rating_scale param is requiered.
reader = Reader(rating_scale=(1, 5))
max_min_scaler = lambda x : ((x-np.min(x))/(np.max(x)-np.min(x)))*4+1
df[['popularity']] = df[['popularity']].apply(max_min_scaler)

sns_hist = sns.distplot(df['popularity'])
fig = sns_hist.get_figure()
plt.xlabel("Rating")
plt.ylabel("Count")
fig.savefig('./rating_distribution.pdf',dpi=600,format='pdf')


# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(df[['playlist_id', 'song_id', 'popularity']], reader)

# define a cross-validation iterator
kf = KFold(n_splits=5)

def train(name, model):
    algo = model
    rmse_result = []
    mae_result = []
    result = []
    print("Training "+name)
    for trainset, testset in kf.split(data):
        algo.fit(trainset)
        predictions = algo.test(testset)

        rmse_result.append(rmse(predictions))
        mae_result.append(mae(predictions))

        dump.dump('./Model/{0}'.format(name), predictions, algo)

    predictions, algo = dump.load('./Model/{0}'.format(name))

    df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
    r_squared = 1 - mean_squared_error(df['rui'],df['est'])/np.var(df['rui'])
    result.append(np.mean(rmse_result))
    result.append(np.mean(mae_result))
    result.append(r_squared)

    print("Training " + name + " Completed")
    return result

def save_result(result,name,rmse,mae,r_squared):
    result = result.append(
        pd.DataFrame({'Model': [name], 'RMSE': [rmse], 'MAE': [mae],'R_Squared': [r_squared]}), ignore_index=True)
    return result

result_comparation = pd.DataFrame(columns=['Model', 'RMSE','MAE','R_Squared'])

temp = train("SVD", SVD())
result_comparation = save_result(result_comparation,"SVD",temp[0],temp[1],temp[2])

temp = train("k-NN", KNNBasic())
result_comparation = save_result(result_comparation,"k-NN",temp[0],temp[1],temp[2])

temp = train("Centered k-NN", KNNWithMeans())
result_comparation = save_result(result_comparation,"Centered k-NN",temp[0],temp[1],temp[2])

temp = train("k-NN Baseline", KNNBaseline())
result_comparation = save_result(result_comparation,"k-NN Baseline",temp[0],temp[1],temp[2])

temp = train("Co-Clustering", CoClustering())
result_comparation = save_result(result_comparation,"Co-Clustering",temp[0],temp[1],temp[2])

temp = train("Random", NormalPredictor())
result_comparation = save_result(result_comparation,"Random",temp[0],temp[1],temp[2])

result_comparation.to_csv("./comparation_result.csv",encoding='utf-8')
