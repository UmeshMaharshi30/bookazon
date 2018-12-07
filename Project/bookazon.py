# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 20:18:04 2018

@author: umesh
This is the main file of the application
"""

from os import system
import pandas as pd
import numpy as np
from unidecode import unidecode
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import secrets

import author_similarity
import User_Similarity

top_books = [];
books_finished_by_user = [];

def get_previous_authors(userid):
    rating_file = "../data set/ratings.csv";
    user_rating = pd.read_csv(rating_file, usecols=["id", "user_id"]);
    books_finished_by_user = [];
    for index, row in user_rating.iterrows():
        if(row[1] == userid):
            if row[0] not in books_finished_by_user:
                books_finished_by_user.append(row[0]);
    author = get_author(secrets.choice(books_finished_by_user));
    return author;
    

def get_author(bookid):
    file_author_book_rating = "../Cleansed/authors_book_rating.csv";
    min_rating = 4.5;
    auth_book_rat_map = pd.read_csv(file_author_book_rating, usecols=["author", "bookid", "rating"]);
    authors = [];
    for index, row in auth_book_rat_map.iterrows():
        if(row[2] >= min_rating):
            top_books.append(row[1]);
        if row[1] == bookid:
            authors.append(row[0]);
    return secrets.choice(authors);


def start_bookazon():
    # get user id 
    userid = input("Please enter userid: ")
    print("Userid  entered " + str(userid));
    print("Fetching previous authors and books read");
    author = get_previous_authors(32748);
    print("Finished fetching previous authors and books read");
    print("Author matched : " + author);
    Book_from_author = author_similarity.recommend_books(author);
    print("Books recommend from author similarity");
    print(Book_from_author);
    ratings_filename = '../data set/ratings.csv'
    books_filename = '../data set/books.csv'
    books_from_user_similarity = User_Similarity.get_topn_books_from_similar_users(ratings_filename, books_filename, 5, 32748);
    print(books_from_user_similarity);
    random_top_rated_books = [];
    ind = 0;
    while ind < 2:
        temp_book = secrets.choice(top_books);
        if temp_book not in random_top_rated_books:
            random_top_rated_books.append(temp_book);
            ind += 1;
    print("Random top books");
    print(random_top_rated_books);
    print("Books recommended from books similarity");
    
    return;
    
if __name__ == '__main__':
    start_bookazon()      