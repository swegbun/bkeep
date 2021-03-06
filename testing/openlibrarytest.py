#!/usr/bin/env python3

import argparse
import requests

def isbn13to10(isbn):
    isbn = isbn[3:len(isbn) - 1]
    chkchr = 0
    index = 1
    for c in isbn:
        chkchr += int(c) * index
        index += 1
    chkchr %= 11

    if chkchr == 10:
        chkchr = 'X'

    isbn += str(chkchr)
    return isbn

def get_info(isbn):
    return requests.get('https://openlibrary.org/api/books?bibkeys=ISBN:' + isbn + '&jscmd=data&format=json').json()

def print_info(json_result, isbn):
    if 'ISBN:' + isbn not in json_result.keys():
        print("Record not found")
        return
    title = json_result['ISBN:' + isbn]['title']
    authors = ''
    if 'authors' in json_result['ISBN:' + isbn].keys():
        for author in json_result['ISBN:' + isbn]['authors']:
            authors += author['name'] + ', '

    authors = authors[:len(authors) - 2]
    print(title + '\t' + authors + '\t\t' + isbn + '\t')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i')
    args = parser.parse_args()
    isbn = args.i
    if isbn != None:
        if len(isbn) == 13:
            isbn = isbn13to10(isbn)
        if len(isbn) != 10:
            print("Invalid ISBN. Try removing dashes.")
            exit(-1)
        json_result = get_info(isbn)
        print_info(json_result, isbn)
    else:
        print('Must provide ISBN')
