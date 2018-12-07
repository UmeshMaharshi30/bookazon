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
import book_similarity_giang

top_books = [];
books_finished_by_user = [];

def get_previous_authors(userid):
    rating_file = "../data set/ratings.csv";
    user_rating = pd.read_csv(rating_file, usecols=["id", "user_id"]);
    for index, row in user_rating.iterrows():
        if(row[1] == userid):
            if row[0] not in books_finished_by_user:
                books_finished_by_user.append(row[0]);
    print(len(books_finished_by_user));
    if len(books_finished_by_user) == 0:
        return -1;                
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


def fetch_books_name_map():
    books = "../data set/books.csv";
    books_name = pd.read_csv(books, usecols=["id", "title"]);
    books_map = {};
    for index, row in books_name.iterrows():
        books_map.update({str(row[0]) : row[1]});
    return books_map;

def start_bookazon():
    # get user id 
    userid = input("Please enter userid: ")
    print("Userid  entered " + str(userid));
    print("Fetching previous authors and books read");
    author = get_previous_authors(userid);
    if author == -1:
        print("Please enter a different user id. Insufficient data for the specified user");
        return;
    print("Finished fetching previous authors and books read");
    print("Author matched : " + author);
    print("Starting Author similarity");
    Book_from_author = author_similarity.recommend_books(author);
    print("Books recommend from author similarity");
    print(Book_from_author);
    ratings_filename = '../data set/ratings.csv'
    books_filename = '../data set/books.csv'
    print("Starting User similarity");
    books_from_user_similarity = User_Similarity.get_topn_books_from_similar_users(ratings_filename, books_filename, 5, 32748);
    print("Books recommend from User similarity");
    print(books_from_user_similarity);
    random_top_rated_books = [];
    ind = 0;
    while ind < 2:
        temp_book = secrets.choice(top_books);
        if temp_book not in random_top_rated_books and temp_book not in books_finished_by_user:
            random_top_rated_books.append(temp_book);
            ind += 1;
    print("Random top books");
    print(random_top_rated_books);
    print("Books recommended from books similarity");
    print("Total books read by the User " + str(len(books_finished_by_user)));
    books_from_books_sim = book_similarity_giang.book_similarity(secrets.choice(books_finished_by_user));
    print(books_from_books_sim);
    ans = [];
    # pick 3 books from book_sim, 3 from users_sim, 2 from toprated and 2 from author_sim
    ind = 0;
    
    while ind < 3 and ind < len(books_from_books_sim):
        temp_book = secrets.choice(books_from_books_sim);
        if temp_book not in ans and temp_book not in books_finished_by_user:
            ans.append(temp_book);
            ind += 1;
    
    ind = 0;
    
    while ind < 3 and len(books_from_user_similarity):
        temp_book = secrets.choice(books_from_user_similarity);
        if temp_book not in ans and temp_book not in books_finished_by_user:
            ans.append(temp_book);
            ind += 1;
    
    ind = 0;
    
    while ind < 3 and len(Book_from_author):
        temp_book = secrets.choice(Book_from_author);
        if temp_book not in ans and temp_book not in books_finished_by_user:
            ans.append(temp_book);
            ind += 1;
            
    for row in random_top_rated_books:
        ans.append(row);
        
    print("Top 10 books recommended by the system ");  
    print("By ids ...");
    print(ans);
    print("By names ...");
    print("If book id is more than 10000, we will ignore it");
    books_map = fetch_books_name_map();
    for bookid in ans:
        if str(bookid) in books_map:
            print(books_map[str(bookid)]);
        
    return;
    
if __name__ == '__main__':
    start_bookazon()      