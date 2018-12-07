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
import secrets

book_file = "../data set/books.csv";
tag_clean_file = "../Cleansed/tags.csv";
tag_file = "../data set/tags.csv";
book_tag_file = "../data set/book_tags.csv";
book_tag_clean_file = "../Cleansed/book_tags.csv";
book_filtered_tag_clean_file = "../Cleansed/book_filter_tags.csv";
genres = ["Art", "Comics", "Cookbooks", "Fantasy", "History", "Poetry", "Psychology"];
auth_cols = ["author", "Art", "Comics", "Cookbooks", "Fantasy", "History", "Poetry", "Psychology"];
tag_cols = ["tag_id", "tag_name"];
book_cols = ["id", "authors"];
author_gen = "../Cleansed/authors.csv";
author_class = "../Cleansed/authors_class.csv";
file_author_book_rating = "../Cleansed/authors_book_rating.csv";

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


def remove_duplicates_tags():
    tags = pd.read_csv(book_tag_clean_file, usecols=["book_id", "tag_name"]);
    filtered_tags = {};
    for index, row in tags.iterrows():
        if str(row[0]) not in filtered_tags:
            filtered_tags.update({str(row[0]) : [row[1]]});
        else:
            if(row[1] not in filtered_tags[str(row[0])]):
                filtered_tags[str(row[0])].append(row[1]);
    with open(book_filtered_tag_clean_file, 'w') as file_handler:
        file_handler.write("{}\n".format("book_id" + ',' + "tag_name"))
        for item in filtered_tags:
            for gen in filtered_tags[str(item)]:
                file_handler.write("{}\n".format(str(item) + "," + gen));  



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
    #print(len(authors));
    book_tags = pd.read_csv(book_filtered_tag_clean_file, usecols=["book_id", "tag_name"]);
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
    gen_count = [0]*len(genres);
    clusters = 10;
    for index, row in authors.iterrows():
        gen_data = [0]*len(genres);
        for gen_name in range(0 ,len(genres)):
            gen_data[gen_name] = row[genres[gen_name]];
            gen_count[gen_name] = gen_count[gen_name] + row[genres[gen_name]]; 
        author_data.append(gen_data);
    author_data = np.array(author_data);
    kmeans = KMeans(n_clusters=clusters, algorithm="elkan")
    kmeans.fit(author_data)
    #for ind_i in range(0, len(genres)):
    #    print(genres[ind_i] + " " + str(gen_count[ind_i]));
    #print(gen_count);
    plt.figure(figsize=(12,8));
    plt.xticks(rotation=90)
    plt.title("Genre Distribution", fontdict={'fontsize':20});
    plt.tick_params(axis='both', labelsize=16);
    plt.bar(range(0, len(gen_count)),gen_count, tick_label=genres)
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
    
    
def write_author_book_rating_map():
    books = pd.read_csv(book_file, usecols=["id", "authors", "average_rating"]);
    print(books.head(5));
    with open(file_author_book_rating, 'w') as file_handler:
        file_handler.write("{}\n".format("author,bookid,rating"))
        for index,row in books.iterrows():
            for col_auth in row[1].split(","):
                col_auth = unidecode(col_auth.strip());
                file_handler.write("{}\n".format(col_auth + "," + str(row[0]) + "," + str(row[2])));    
    
def get_authors_from_clusters(author_name, k):
    authors = pd.read_csv(author_class, usecols=["author", "class"]);
    simil_authors = [];
    auth_class = -1;
    class_author_map = {};
    for index, row in authors.iterrows():
        if(row[0] ==  author_name):
            auth_class = row[1];
        if str(row[1]) not in class_author_map:
            class_author_map.update({str(row[1]) : [row[1]]});
        else:
            if row[0] not in class_author_map[str(row[1])]:
                class_author_map[str(row[1])].append(row[0]);
    if auth_class == -1:
        print("Author not found");
        return simil_authors;                
    ind = 0;
    while ind < k and k < len(class_author_map[str(auth_class)]):
        aut = secrets.choice(class_author_map[str(auth_class)]);
        if((aut != author_name) and (aut not in simil_authors)):
            simil_authors.append(aut);
            ind += 1
    return simil_authors;            
                 
def recommend_books(author_name):
    books_recommended = [];
    sim_auth_count = 5;
    sim_book_count = 10;
    similar_authors = get_authors_from_clusters(author_name, sim_auth_count);
    auth_book_rat_map = pd.read_csv(file_author_book_rating, usecols=["author", "bookid", "rating"]);
    for index, row in auth_book_rat_map.iterrows():
        if(row[0] in similar_authors):
            if(row[2] > 0):
                books_recommended.append(row[1]);
    #print(books_recommended);
    if(len(books_recommended) < sim_book_count):
        return books_recommended;
    ind = 0;
    random_books = [];
    while ind < sim_book_count:
        temp_book = secrets.choice(books_recommended);
        if temp_book not in random_books:
            random_books.append(temp_book);
            ind += 1;
    return random_books;            
    
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
    #remove_duplicates_tags();
    #process_authors();
    k_cluster_author(); 
    #recommend_books("Suzanne Collins");
    
if __name__ == '__main__':
    main()       