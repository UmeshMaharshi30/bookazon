# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 17:42:55 2018

@author: umesh
"""

# -*- coding: utf-8 -*-

from os import system
import pandas as pd
import numpy

# Load book attributes
columns = ["id","book_id","authors","original_publication_year","original_title","language_code","average_rating","ratings_count"];
book_data_file = "../Cleansed/Final.csv";
heuristic_func = [0,0,10,3,0,2,4,0];
similarity_file = "similarity.csv";
book_tag_file = "../data set/book_tags.csv";



def get_all_books():
    books = pd.read_csv(book_data_file, usecols=range(0,8));
    # top 20 data
    #print(books.loc[0]);
    return books;


def calculate_similarity():
    books = get_all_books();
    total_books = len(books);
    book_sim = numpy.zeros((total_books, total_books));
    total_attr = len(heuristic_func);
    book_tags = setup_tags();
    for row in range(0, total_books):
        for col in range(row + 1, total_books):
            b = books.loc[col];
            match_book = books.loc[row];
            heu_val = 0;
            if row != col: 
                for attr in range(0,total_attr):
                    if attr == 6:
                        heu_val = heu_val + (heuristic_func[attr] * match_book[columns[attr]]);
                    elif b[columns[attr]] == match_book[columns[attr]]:
                        heu_val = heu_val + heuristic_func[attr];
                    #print(heu_val);    
            book_sim[row][col] = heu_val + get_tag_match_value(book_tags, row, col);
        print("row", row, "done");    
    df = pd.DataFrame(book_sim)
    df.to_csv(similarity_file, header=None);
        

def setup_tags():
    book_tags = pd.read_csv(book_tag_file);
    #print(book_tags)
    #print(book_tags.loc[book_tags["goodreads_book_id"] == 1]);
    return book_tags;


def get_tag_match_value(all_book_tags, row_book, col_book):
    total_col_tags = all_book_tags.loc[all_book_tags["goodreads_book_id"] == col_book + 1];
    total_row_tags = all_book_tags.loc[all_book_tags["goodreads_book_id"] == row_book + 1];
    matched = 0;
    if (len(total_col_tags) > 0 and len(total_row_tags) > 0):
        for index, row in total_col_tags.iterrows():
            if len(total_row_tags.loc[total_row_tags["tag_id"] == row["tag_id"]]) > 0:
                matched = matched + 1;
    if(len(total_col_tags) > 0):
        matched = ((matched)/len(total_col_tags))*10;        
    return matched;        

def main():
    system('clear');
    #get_all_books();
    #setup_tags();
    calculate_similarity();


if __name__ == '__main__':
    main()     
