# -*- coding: utf-8 -*-

import csv
from collections import defaultdict
from collections import Counter
import pandas as pd
from scipy import spatial

def import_ratings_data(filename):
    ratings_file = pd.read_csv(filename, header=0)
    #new_df = ratings_file[((ratings_file['user_id'] == 17329))]
    file_contents = ratings_file.iloc[:, 0:3].values
    return file_contents

def import_books_data(filename):
    books_file = pd.read_csv(filename, header = 0)
    books_contents = books_file.iloc[:, 0:21].values
    return books_contents    


def get_books_rated_by_User(userid, file_contents, books_read_by_user):
    books_and_ratings_by_user = defaultdict(dict)
    for row in file_contents: # read a row as {column1: value1, column2: value2,...}
        if(row[1] == userid):
            books_read_by_user.add(row[0])
            books_and_ratings_by_user[row[1]][row[0]] = row[2]
    return books_read_by_user, books_and_ratings_by_user
    
def get_users_rated_same_books(books_read_by_user, file_contents):
    related_users = defaultdict(dict)
    for row in file_contents:
        if(books_read_by_user.__contains__(row[0])):
            related_users[row[1]][row[0]] = row[2]
    return related_users

def cosine_similarity(user1, user2, related_users, books_and_ratings_by_user):
    data1 = []
    data2 = []
    user2_book_ratings = related_users[user2]
    for key in user2_book_ratings:
        data2.append(related_users[user2][key])
        data1.append(books_and_ratings_by_user[user1][key])
    result = 1 - spatial.distance.cosine(data1, data2)
    return result




def get_topn_books_from_similar_users(ratings_filename, books_filename, n, userid):
    
    file_contents = import_ratings_data(ratings_filename)  # import ratings file
    user1 = userid       # user for whom we want to find similar users
    books_read_by_user = set({})
    
    #getting books read and its rating by user and getting related users
    books_read_by_user, books_and_ratings_by_user = get_books_rated_by_User(user1, file_contents, books_read_by_user)
    related_users = get_users_rated_same_books(books_read_by_user, file_contents)
    
    #computing user similarity
    user_similarity_score = {}
    for user2 in related_users:
        result = cosine_similarity(user1, user2, related_users, books_and_ratings_by_user)
        user_similarity_score[user2] = result
    
    #get top 5 similar users and books read by them
    import heapq
    top5 = heapq.nlargest(5, user_similarity_score, key=user_similarity_score.get)
    books_read_by_top5 = {}
    for user in top5:
        for row in file_contents:
            if(top5.__contains__(row[1]) and row[0] not in books_read_by_user):
                books_read_by_top5[row[0]] = 0
            
    
    my_filtered_csv = pd.read_csv(books_filename, usecols=['id', 'ratings_5']) #importing books and their ratings
    
    #gettings ratings for books read by similar users
    for row in my_filtered_csv.itertuples():
        if(row[1] in books_read_by_top5):
            #print(row[0],row[1])
            books_read_by_top5[row[1]] = row[2]

    #getting top 5 rated books among the similar users
    top5_books = heapq.nlargest(n, books_read_by_top5, key=books_read_by_top5.get)
    return top5_books

ratings_filename = '../data set/ratings.csv'
books_filename = '../data set/books.csv'
#print(get_topn_books_from_similar_users(ratings_filename, books_filename, 5, 17329))