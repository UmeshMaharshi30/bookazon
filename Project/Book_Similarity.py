# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 17:42:55 2018

@author: umesh
"""

# -*- coding: utf-8 -*-

from os import system
import pandas
import numpy

# Load book attributes
columns = ["sepal length", "sepal width", "petal length", "petal width", "classname"];
book_data_file = "books.csv";
heuristic_func = [];
similarity_fil = "similarity.csv";



def get_all_books():
    books = pandas.read_csv(book_data_file, names=columns);
    # top 20 data
    print(books.head(20));
    return books;


def calculate_similarity():
    books = get_all_books();
    total_books = len(books);
    book_sim = numpy.zeros((total_books, total_books));
    total_attr = len(heuristic_func);
    for row in range(0, total_books):
        for col in range(0, total_books):
            b = books[col];
            heu_val = 0;
            if row != col: 
                for attr in range(0,total_attr):
                    if b[attr] == books[row]:
                        heu_val = heu_val + heuristic_func[attr];
            book_sim[row][col] = heu_val;
    numpy.savetxt(similarity_fil, book_sim, delimiter=",");
        


def main():
    system('clear');
    calculate_similarity();


if __name__ == '__main__':
    main()     