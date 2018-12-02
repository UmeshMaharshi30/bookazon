# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 20:15:49 2018

@author: umesh
"""

from os import system
import pandas as pd
import numpy as np
from unidecode import unidecode
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

book_file = "../data set/books.csv";
tag_clean_file = "../Cleansed/tags.csv";
tag_file = "../data set/tags.csv";
book_tag_file = "../data set/book_tags.csv";
book_tag_clean_file = "../Cleansed/book_tags.csv";
genres = ["Art", "Biography", "Business", "Chick Lit", "Children's", "Christian", "Classics", "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Gay and Lesbian", "Graphic Novels", "Historical Fiction", "History", "Horror", "Humor and Comedy", "Horror", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports", "Thriller", "Travel", "Young Adult"];
auth_cols = ["author", "Art", "Biography", "Business", "Chick Lit", "Children's", "Christian", "Classics", "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Gay and Lesbian", "Graphic Novels", "Historical Fiction", "History", "Horror", "Humor and Comedy", "Horror", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports", "Thriller", "Travel", "Young Adult" ];
tag_cols = ["tag_id", "tag_name"];
book_cols = ["id", "authors"];
author_gen = "../Cleansed/authors.csv";
author_class = "../Cleansed/authors_class.csv";

cleaned_tags = [];

def clean_all_tags():
    tags = pd.read_csv(tag_file, usecols=tag_cols);
    for index, row in tags.iterrows():
        for gen in genres:
            if ( gen.casefold() in row[tag_cols[1]].casefold()):
                cleaned_tags.append(Tag(row[tag_cols[0]], gen));
                break;
    #print(len(cleaned_tags));  
    with open(tag_clean_file, 'w') as file_handler:
        file_handler.write("{}\n".format(tag_cols[0] + ',' + tag_cols[1]))
        for item in cleaned_tags:
            file_handler.write("{}\n".format(str(item.id) + ',' + item.name))

def pre_process_book_tag_file():
    tags = get_all_tags();
    cleaned_book_tags = [];
    book_tags = pd.read_csv(book_tag_file);
    for index, row in book_tags.iterrows():
        if(row[2] in tags):
            cleaned_book_tags.append(Book(row[0], row[2], tags[row[2]]));
    with open(book_tag_clean_file, 'w') as file_handler:
        file_handler.write("{}\n".format("book_id" + ',' + "tag_name"))
        for item in cleaned_book_tags:
            file_handler.write("{}\n".format(str(getattr(item, "bookid")) + ',' + str(getattr(item, "tagname"))));

def get_all_tags():
    clean_tags = pd.read_csv(tag_clean_file, usecols=tag_cols);
    tags = {};
    for index, row in clean_tags.iterrows():
        tags.update({row[0] : row[1]});
    return tags;    

def process_authors():
    books = pd.read_csv(book_file, usecols=book_cols);
    authors = {};
    book_author = {};
    for index, book in books.iterrows():
        book_author.update({str(book[0]) : book[1].split(",")});
        #print(book_author[str(book[0])]);
        for col_auth in book[1].split(","):
            col_auth = unidecode(col_auth.strip());
            if(col_auth not in authors):
                authors.update({col_auth : Author(col_auth)});     
    print(len(authors));
    book_tags = pd.read_csv(book_tag_clean_file, usecols=["book_id", "tag_name"]);
    for index, row in book_tags.iterrows():
        #print(row[0], row[1]);
        if str(row[0]) in book_author:
            #print(book_author[str(row[0])]);
            for aut in book_author[str(row[0])]:
                aut = unidecode(aut.strip());
                if aut in authors:
                    gen_arr = getattr(authors[aut], "genres");
                    gen_arr[genres.index(row[1])] = gen_arr[genres.index(row[1])] + 1;    
    with open(author_gen, 'w') as file_handler:
        file_handler.write("{}\n".format("author" + ',' + ','.join(genres)))
        for item in authors:
            file_handler.write("{}\n".format(unidecode(getattr(authors[item], "name")) + "," + ','.join(map(str, normalize(getattr(authors[item], "genres"))))));

def normalize(gen_arr):
    total_books = 0;
    for c in gen_arr:
        total_books = total_books + c;
    if total_books > 0:
        for i in range(0, len(gen_arr)):
            gen_arr[i] = gen_arr[i]/total_books;
    return gen_arr;        
 
def k_cluster_author():   
    # given an author find his k nearest neighbors
    authors = pd.read_csv(author_gen, usecols=auth_cols);
    author_data = [];
    clusters = 10;
    for index, row in authors.iterrows():
        gen_data = [0]*len(genres);
        for gen_name in range(0 ,len(genres)):
            gen_data[gen_name] = row[genres[gen_name]];
        author_data.append(gen_data);
    author_data = np.array(author_data);
    kmeans = KMeans(n_clusters=clusters, algorithm="elkan")
    kmeans.fit(author_data)
    #print(kmeans.cluster_centers_)
    y_km = kmeans.fit_predict(author_data);
    plt.figure(figsize=(10,8));
    plt.title("Author Clustering Using KMeans Model", fontdict={'fontsize':20});
    plt.tick_params(axis='both', labelsize=16);
    plt.scatter(author_data[y_km ==1,0], author_data[y_km == 1,1], s=50, c='black')
    plt.scatter(author_data[y_km ==2,0], author_data[y_km == 2,1], s=50, c='blue')
    plt.scatter(author_data[y_km ==3,0], author_data[y_km == 3,1], s=50, c='cyan')
    plt.scatter(author_data[y_km ==4,0], author_data[y_km == 4,1], s=50, c='pink')
    plt.scatter(author_data[y_km ==5,0], author_data[y_km == 5,1], s=50, c='green')
    plt.scatter(author_data[y_km ==6,0], author_data[y_km == 6,1], s=50, c='grey')
    plt.scatter(author_data[y_km ==7,0], author_data[y_km == 7,1], s=50, c='orange')
    plt.scatter(author_data[y_km ==8,0], author_data[y_km == 8,1], s=50, c='violet')
    plt.scatter(author_data[y_km ==9,0], author_data[y_km == 9,1], s=50, c='indigo')
    plt.scatter(author_data[y_km ==0,0], author_data[y_km == 0,1], s=50, c='red')
    stats_data = [0]*clusters;
    with open(author_class, 'w') as file_handler:
        file_handler.write("{}\n".format("author" + ',' + "class"))
        for index,row in authors.iterrows():
            #print(row["author"]);
            stats_data[y_km[index]] = stats_data[y_km[index]] + 1;
            file_handler.write("{}\n".format(row["author"] + "," + str(y_km[index])));
    print(stats_data);
    
    
class Author:
  def __init__(self,name):
    self.name = name
    self.genres = [0]*len(genres);
    
    
class Book:
  def __init__(self, bookid, tagid, tagname):
    self.tagname = tagname;
    self.bookid = bookid
    self.tagid = tagid
    
class Tag:
  def __init__(self, id, name):
    self.id = id
    self.name = name


def main():   
    #clean_all_tags();
    #pre_process_book_tag_file();
    #process_authors();
    k_cluster_author();

if __name__ == '__main__':
    main()       