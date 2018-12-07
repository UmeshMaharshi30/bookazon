# -*- coding: utf-8 -*-
"""
Created on Sun Dec 02 17:42:55 2018

@author: Giang
"""

# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt



from sklearn.neighbors import NearestNeighbors

def book_similarity(book_id):
    books = pd.read_csv('../Cleansed/Final.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    books.columns = ['id', 'book_id', 'authors', 'original_publication_year', 'original_title', 'language_code',
                      'average_rating', 'ratings_count', '']

    ratings = pd.read_csv('../data set/ratings.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    ratings.columns = ['id', 'user_id', 'rating']

    categories = pd.read_csv('../Cleansed/book_tags.csv', sep=',', error_bad_lines=False, encoding="latin-1")
    categories.columns = ['book_id', 'tag_name']


    combine_book_rating = pd.merge(ratings, books, on='id')
    columns = ['original_title',  'authors', 'language_code', 'original_publication_year', 'average_rating', '']

    combine_book_rating = combine_book_rating.drop(columns, axis=1)
    #print(combine_book_rating.head())


    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    #print(combine_book_rating['ratings_count'].describe())

    #print(combine_book_rating['ratings_count'].quantile(np.arange(.8, 1, .01)))
    
    popularity_threshold = 0
    rating_popular_book = combine_book_rating.query('ratings_count >= @popularity_threshold')
    rating_popular_book.head()


    rating_popular_book = rating_popular_book.drop_duplicates(['user_id', 'book_id'])
    #print(rating_popular_book.head())
    rating_popular_book_pivot = rating_popular_book.pivot(index = 'book_id', columns = 'user_id', values = 'rating').fillna(0)
    #print(rating_popular_book_pivot.index)
    rating_popular_book_matrix = csr_matrix(rating_popular_book_pivot.values)
    #print(rating_popular_book_matrix)
    model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
    model_knn.fit(rating_popular_book_matrix)

    query_index = 0
    for i in range(len(rating_popular_book_pivot.index)):
        if rating_popular_book_pivot.index[i] == book_id:
            query_index = i
            #print('xxx')
            #print(query_index)
            break


    distances, indices = model_knn.kneighbors(rating_popular_book_pivot.iloc[query_index, :].values.reshape(1, -1), n_neighbors = 6)
    #print(distances)
    #print(indices)
    books_reco = [];
    for i in range(0, len(distances.flatten())):
        if i > 0:
            books_reco.append(rating_popular_book_pivot.index[indices.flatten()[i]]);
            #print('{0}: {1}, with distance of {2}:'.format(i, rating_popular_book_pivot.index[indices.flatten()[i]], distances.flatten()[i]))
    return books_reco;
#book_similarity(2767052)

'''
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

'''

plt.rc("font", size=15)
categories.tag_name.value_counts(sort=False).plot(kind='bar')
plt.title('Categories Distribution\n')
plt.xlabel('Categories')
plt.ylabel('Count')
plt.savefig('system1.png', bbox_inches='tight')
plt.show()

plt.rc("font", size=15)
ratings.rating.value_counts(sort=False).plot(kind='bar')
plt.title('Rating Distribution\n')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.savefig('system1.png', bbox_inches='tight')
plt.show()
'''