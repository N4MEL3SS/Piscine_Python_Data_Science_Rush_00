from links import Links
from movies import Movies
from ratings import Ratings
from tags import Tags
import timeit


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


def benchmark(name, num, rand_list):
    stmt = f'{name}({rand_list})'
    code = f'from __main__ import {name}'
    times = timeit.timeit(stmt=stmt, setup=code, number=num)
    return times

def main():
    links_path = '../dataset/links.csv'
    movies_path = '../dataset/movies.csv'
    ratings_path = '../dataset/ratings.csv'
    tags_path = '../dataset/tags.csv'

    links_class = Links(links_path)
    movies_class = Movies(movies_path)
    ratings_class = Ratings(ratings_path)
    tags_class = Tags(tags_path)

    print(movies_class.dist_by_release())
    # print(movies_class.dist_by_genres())
    # print(movies_class.most_genres(10))


if __name__ == '__main__':
    main()
