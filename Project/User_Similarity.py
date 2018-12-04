# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
from collections import Counter
import pandas as pd

def import_ratings_data(filename):
    ratings_file = pd.read_csv(filename, header=0)
    new_df = ratings_file[((ratings_file['user_id'] == 17329))]
    file_contents = ratings_file.iloc[:, 0:3].values
    return file_contents



file_contents = import_ratings_data('C:/Users/anurag/Desktop/Project572/bookazon/data set/ratings.csv')
     # read rows into a dictionary format
    

books_read_by_user = set({})

def get_books_rated_by_User(userid):
    for row in file_contents: # read a row as {column1: value1, column2: value2,...}
        if(row[1] == userid):
            books_read_by_user.add(row[0])
    return books_read_by_user
    
def get_users_rated_same_books(books_read_by_user):
    related_users = defaultdict(dict)
    for row in file_contents:
        if(books_read_by_user.__contains__(row[0])):
            related_users[row[1]][row[0]] = row[2]
    return related_users

books_read_by_user = get_books_rated_by_User(17329)
related_users = get_users_rated_same_books(books_read_by_user)
print(len(related_users))

