from links import Links
from movies import Movies
from ratings import Ratings
from tags import Tags

# import os
# import sys
# import urllib
# import requests
# from bs4 import BeautifulSoup as soup
# import json
# import pytest
# import collections
# import functools
# import datetime
# import re


# Удалить перед сдачей
import timeit
import psutil


class Test:
    def __init__(self):
        pass

    def write_dataset_in_outputfile(self, filename, output_dict):
        try:
            with open(f'../output_dataset/{filename}.csv', 'w') as output_file:
                output_file.write("key,value")
                for key, value in output_dict:
                    output_file.write(f'{key()},{value()}')
        except FileNotFoundError as err:
            print(err)


def benchmark(function_name, class_name, path, num, args=None):
    stmt = f'{class_name.capitalize()}.{function_name}({args})'
    code = f'from {class_name} import {class_name.capitalize()}\n' \
           f'{class_name.capitalize()}("{path}")\n'
    times = timeit.timeit(stmt=stmt, setup=code, number=num)
    return times


def movie_class_bench(movies_path):
    movies_class = Movies(movies_path)
    print(movies_class.dist_by_release())
    # print(benchmark('dist_by_release', 'movies', movies_path, 100))

    mem_rss = psutil.Process().memory_info().rss / float(2 ** 30)
    mem_vms = psutil.Process().memory_info().vms / float(2 ** 30)
    cpu = psutil.Process().cpu_times()

    print(f'Peak Real Memory Usage = {mem_rss:0.3f} Gb')
    print(f'Peak Virtual Memory Usage = {mem_vms:0.3f} Gb')
    print(f'User Time + System Time = {cpu.user + cpu.system:0.2f}s')


def main():
    links_path = '../dataset/links.csv'
    movies_path = '../dataset/movies.csv'
    ratings_path = '../dataset/ratings.csv'
    tags_path = '../dataset/tags.csv'

    # movie_class_bench(movies_path)

    movies_class = Movies(movies_path, has_order=True)
    links_class = Links(links_path, movies_class.get_movies_title(), links_on=True)
    ratings_class = Ratings(ratings_path)
    tags_class = Tags(tags_path)

    # print("Movie class:")
    # print(movies_class.dist_by_release())
    # print(movies_class.dist_by_genres())
    # print(movies_class.most_genres(10))
    #
    # print("\nTag class:")
    # print(tags_class.most_words(10))
    # print(tags_class.longest(10))
    # print(tags_class.most_words_and_longest(10))
    # print(tags_class.most_popular(10))
    # print(tags_class.tags_with('war'))
    #
    # rating_movies_subclass = ratings_class.Movies(ratings_class, movies_class.get_movies_title())
    # print("\nRating class:")
    # print(rating_movies_subclass.dist_by_year())
    # print(rating_movies_subclass.dist_by_rating())
    # print(rating_movies_subclass.top_by_num_of_ratings(10))
    # print(rating_movies_subclass.top_by_ratings(30))
    # print(rating_movies_subclass.top_controversial(30))
    #
    # print("\nLink class:")
    # print(links_class.get_imdb(links_class.get_movies_id()[:5], ['Director', 'Budget', 'Runtime', 'Cumulative Worldwide Gross']))
    # print(links_class.top_directors(3))
    # print(links_class.most_expensive(3))
    # print(links_class.most_profitable(3))
    # print(links_class.longest(3))
    print(links_class.top_cost_per_minute(3))

    print("\nSystem resources:")
    mem_rss = psutil.Process().memory_info().rss / float(2 ** 30)
    mem_vms = psutil.Process().memory_info().vms / float(2 ** 30)
    cpu = psutil.Process().cpu_times()

    print(f'Peak Real Memory Usage = {mem_rss:0.3f} Gb')
    print(f'Peak Virtual Memory Usage = {mem_vms:0.3f} Gb')
    print(f'User Time + System Time = {cpu.user + cpu.system:0.2f}s')


if __name__ == '__main__':
    main()
