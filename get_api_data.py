# -*- coding: utf-8 -*-
"""
Created on Sun May 14 17:12:15 2017

@author: George Pastakas
"""

import os
os.chdir('C:/Users/user/Desktop/imperialdataforce')

from deezer_api import DeezerAPI
import pandas as pd

# create API object
api = DeezerAPI()

# import training and test set
train = pd.read_csv('DATA/train.csv')
test = pd.read_csv('DATA/test.csv')
        
### 1. Extract User data

"""
User ids are anonymized, thus they don't respond to actual user id numbers
from the site. 
"""

### 2. Extract Artist data

# create a set with all unique artists' IDs
artists = set(train.artist_id).union(test.artist_id)

artist_data = []
for artist in artists:
    # for each artist create a dict with:
    # artist_id, nb_album, nb_fan, radio
    d = {'artist_id':artist}
    # if any of these attributes is missing, fill with None value
    for att in ['nb_album', 'nb_fan', 'radio']:
        try:
            val = api.get(endpoint = 'artist', id_ = str(artist))[att]
        except:
            val = None
        # add to dictionary
        d[att] = val
    # append dictionary to list
    artist_data.append(d)

df = pd.DataFrame(artist_data)
df.to_csv('artist_add_data.csv', index = False)
### 3. Extract Comment data

""""
The user ids in the dataset do not correspond to real user uds, thus we cannot
attribute comments to users.
"""
    
# Add extra artist data to initial training and test set
extra_artist = pd.read_csv('artist_add_data.csv')

train_extra = pd.merge(train, extra_artist, on = 'artist_id', sort = False)
test_extra = pd.merge(test, extra_artist, on = 'artist_id', sort = False)

# write new datasets to .csv files 
train_extra.to_csv('DATA/train_extra.csv', index = False)
test_extra.to_csv('DATA/test_extra.csv', index = False)




