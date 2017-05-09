# -*- coding: utf-8 -*-
"""
Created on Sat May  6 22:52:47 2017

@author: siowmeng
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime


trainData = pd.read_csv('train.csv')

uniqueGenres = np.unique(trainData['genre_id'].as_matrix())
uniqueUsers = np.unique(trainData['user_id'].as_matrix())

genreMatrix = np.empty((len(uniqueUsers), len(uniqueGenres)))
genreMatrix[:] = np.NaN
genreDF = pd.DataFrame(genreMatrix, index = uniqueUsers, columns = uniqueGenres)

# Populate Genre-User Table with 0, 1 and NaN
trainDataMatrix = trainData.loc[:, ['genre_id', 'user_id', 'is_listened']].as_matrix()

for i in range(trainDataMatrix.shape[0]):
    print(i)
    genre = trainDataMatrix[i, 0]
    user = trainDataMatrix[i, 1]
    listen = trainDataMatrix[i, 2]
    if np.isnan(genreDF.loc[user, genre]):
        genreDF.loc[user, genre] = listen
    else:
        if (listen == 1) and (genreDF.loc[user, genre] == 0):
            genreDF.loc[user, genre] = listen

# Write Matrix to CSV for future reading
genreDF.to_csv('genreDF2.csv')

genreDF = pd.read_csv('genreDF.csv', index_col = 0)
genreDF.columns = pd.to_numeric(genreDF.columns)
genreNormalized = genreDF.copy()
genreNormalized[np.isnan(genreNormalized)] = 0

testData = pd.read_csv('test.csv', index_col = 'sample_id')

# Perform prediction
listPrediction = []
starttime = datetime.now()
#for i in range(testData.shape[0]):
for i in range(10000, testData.shape[0]):
    #if i % 1000 == 0:
        #print(i)
    print(i)
    predictGenre = testData.loc[i, 'genre_id']
    predictUser = testData.loc[i, 'user_id']
    k = 5 # Use the weighted average of 5 most similar users' ratings
    prediction = 0.5
    if predictGenre not in uniqueGenres:
        print("No such genre found in training")
    if predictUser not in uniqueUsers:
        print("No such user found in training")
    
    n = 5
    rowIdx = np.where(~np.isnan(genreDF[predictGenre].as_matrix()))[0]
    genreCol = np.where(genreDF.columns.values == predictGenre)[0]
    if len(rowIdx) == 0:
        print("No scoring for this genre found, use default 0.5 probability")
    else:
        if len(rowIdx) < k:
            n = len(rowIdx)
            print("Less than ", k, " rows found in the genre Matrix")
        
        similarRows = genreNormalized.loc[rowIdx, :].as_matrix()
        currRow = genreNormalized.loc[predictUser, :].as_matrix()
        
        #currRowNorm = currRow - np.nanmean(currRow)
        #currRowNorm[np.isnan(currRowNorm)] = 0
        #similarRowsNorm = (similarRows.transpose() - np.nanmean(similarRows, axis = 1)).transpose()
        #similarRowsNorm[np.where(np.isnan(similarRowsNorm))] = 0
        
        # Use Cosine Simlarity between rows
        similarityScore = cosine_similarity([currRow], similarRows)[0]
        
        idxMostSim = similarityScore.argsort()[-n:][::-1]
        simMostSim = similarityScore[idxMostSim]
        listenMostSim = similarRows[idxMostSim, genreCol]
        
        simSum = np.sum(simMostSim)
        if np.sum(simMostSim) == 0:
            prediction = np.mean(listenMostSim)
        else:
            prediction = np.dot(simMostSim, listenMostSim) / simSum
        
    listPrediction.append(prediction)

endtime = datetime.now()

print("Start Time: ", starttime)
print("End Time: ", endtime)

# Write to submission CSV file
listSampleID = [x for x in range(testData.shape[0])]
resultsArray = np.array([listSampleID, listPrediction]).transpose()
resultDF = pd.DataFrame(resultsArray, columns = ['sample_id', 'is_listened'])
resultDF['sample_id'] = resultDF['sample_id'].astype('int')
resultDF.to_csv('submission.csv', index = False)
