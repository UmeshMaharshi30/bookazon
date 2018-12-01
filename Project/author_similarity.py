# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 20:15:49 2018

@author: umesh
"""

from os import system
import pandas as pd
import numpy


book_file = "../data set/books.csv";
tag_clean_file = "../Cleansed/tags.csv";
tag_file = "../data set/tags.csv";
book_tag_file = "../data set/book_tags.csv";
book_tag_clean_file = "../Cleansed/book_tags.csv";
genres = ["Art", "Biography", "Business", "Chick Lit", "Children's", "Christian", "Classics", "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Gay and Lesbian", "Graphic Novels", "Historical Fiction", "History", "Horror", "Humor and Comedy", "Horror", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports", "Thriller", "Travel", "Young Adult"];
tag_cols = ["tag_id", "tag_name"];
book_cols = ["id", "authors"];

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
            cleaned_book_tags.append(Book(row[0], row[2]));
    with open(book_tag_clean_file, 'w') as file_handler:
        file_handler.write("{}\n".format("book_id" + ',' + "tag_id"))
        for item in cleaned_book_tags:
            file_handler.write("{}\n".format(str(getattr(item, "bookid")) + ',' + str(getattr(item, "tagid"))));

def get_all_tags():
    clean_tags = pd.read_csv(tag_clean_file, usecols=tag_cols);
    tags = {};
    for index, row in clean_tags.iterrows():
        tags.update({row[0] : row[1]});
    return tags;    

def process_authors():
    books = pd.read_csv(book_file, usecols=book_cols);
    authors = {};
    for index, book in books.iterrows():
        if(book[1] not in authors):
            authors.update({book[1] : Author(book[1])});    

class Author:
  def __init__(self,name):
    self.name = name
    self.genres = [0]*len(genres);
    
    
class Book:
  def __init__(self, bookid, tagid):
    self.bookid = bookid
    self.tagid = tagid
    
class Tag:
  def __init__(self, id, name):
    self.id = id
    self.name = name


def main():   
    #clean_all_tags();
    #process_authors();
    pre_process_book_tag_file();

if __name__ == '__main__':
    main()       