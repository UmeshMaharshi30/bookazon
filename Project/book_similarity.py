# -*- coding: utf-8 -*-
"""
Created on Sun Dec 02 17:42:55 2018

@author: Giang
"""

# -*- coding: utf-8 -*-

from os import system
import pandas as pd
import numpy as np
from unidecode import unidecode
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from difflib import SequenceMatcher

import csv
import pandas as pd

book_info = "../data set/book_info.csv"

book_tag_file = "../data set/book_tags.csv"

book_file = "../data set/books.csv"

rating = "../data set/ratings.csv"

book_info_cleansed = "../giang/book_info_cleansed.csv"
genres = ["Art", "Biography", "Business", "Christian", "Classics", "Comics", "Cookbooks", "Crime", "Fantasy", "Fiction",
          "Historical Fiction", "History", "Manga", "Mystery", "Poetry", "Psychology"]

auth_cols = ["author", "Art", "Biography", "Business", "Christian", "Classics", "Comics", "Cookbooks", "Crime",
             "Fantasy", "Fiction", "Historical Fiction", "History", "Manga", "Mystery", "Poetry", "Psychology"]

cleaned_tags = []

author_list = []
'''
def author_name_preprocessing():
    authors = pd.read_csv(book_info, usecols=["authors"])
    for author in authors.iterrows():
        #print(author[1].authors)
        count = 0
        for i in range(len(author[1].authors)):
            if author[1].authors[i] is ',':
                count += 1

        author_list.append([author[1].authors.split(',')[j].lstrip(' ') for j in range(count+1)])

    print(author_list)

    with open(book_info_cleansed, 'w', newline='', encoding="utf8") as writeFile:
        writer = csv.writer(writeFile)
        #for i in range(len(author_list)):
        writer.writerows(author_list)



author_name_preprocessing()
'''
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt

books = pd.read_csv('../data set/books.csv', sep=',', error_bad_lines=False, encoding="latin-1")
books.columns = ['id', 'book_id', 'best_book_id', 'work_id', 'books_count', 'isbn', 'isbn13', 'authors',
                 'original_publication_year', 'original_title', 'title', 'language_code', 'average_rating',
                 'ratings_count', 'work_ratings_count', 'work_text_reviews_count', 'ratings_1', 'ratings_2',
                 'ratings_3', 'ratings_4', 'ratings_5', 'image_url', 'small_image_url']
users = pd.read_csv('../BX-CSV-Dump/BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('../data set/ratings.csv', sep=',', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['id', 'user_id', 'rating']

combine_book_rating = pd.merge(ratings, books, on='id')
columns = ['book_id', 'best_book_id', 'work_id', 'books_count', 'isbn', 'isbn13', 'authors',
           'original_publication_year', 'original_title', 'language_code', 'average_rating',
           'ratings_count', 'work_ratings_count', 'work_text_reviews_count', 'ratings_1', 'ratings_2', 'ratings_3',
           'ratings_4', 'ratings_5', 'image_url', 'small_image_url']
combine_book_rating = combine_book_rating.drop(columns, axis=1)
print(combine_book_rating.head())

combine_book_rating = combine_book_rating.dropna(axis = 0, subset = ['title'])

book_ratingCount = (combine_book_rating.
     groupby(by = ['title'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'ratingCount'})
     [['title', 'ratingCount']]
    )
print(book_ratingCount.head())

rating_with_totalRatingCount = combine_book_rating.merge(book_ratingCount, left_on = 'title', right_on = 'title', how = 'left')
print(rating_with_totalRatingCount.head())

pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(book_ratingCount['ratingCount'].describe())

print(book_ratingCount['ratingCount'].quantile(np.arange(.95, 1, .001)))

popularity_threshold = 100
rating_popular_book = rating_with_totalRatingCount.query('ratingCount >= @popularity_threshold')
rating_popular_book.head()


rating_popular_book = rating_popular_book.drop_duplicates(['user_id', 'title'])
rating_popular_book_pivot = rating_popular_book.pivot(index = 'title', columns = 'user_id', values = 'rating').fillna(0)
rating_popular_book_matrix = csr_matrix(rating_popular_book_pivot.values)

from sklearn.neighbors import NearestNeighbors

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(rating_popular_book_matrix)

query_index = np.random.choice(rating_popular_book_pivot.shape[0])
distances, indices = model_knn.kneighbors(rating_popular_book_pivot.iloc[query_index, :].reshape(1, -1), n_neighbors = 6)

for i in range(0, len(distances.flatten())):
    if i == 0:
        print('Recommendations for {0}:\n'.format(rating_popular_book_pivot.index[query_index]))
    else:
        print('{0}: {1}, with distance of {2}:'.format(i, rating_popular_book_pivot.index[indices.flatten()[i]], distances.flatten()[i]))