# irina
import re
from collections import Counter


class Movies:
    # Analyzing data from movies.csv

    def __init__(self, path_to_the_file, has_order=True):
        self.path_file = path_to_the_file
        self.header = ('movieId,title,genres')
        if has_order:
            self.file_data = self.file_open_ordinary()
            self.file_data = [self.file_data[i].rstrip('\n') for i in range(0, len(self.file_data))]
        else:
            self.file_data = self.file_open_generator()

    def file_open_generator(self):
        try:
            with open(self.path_file, 'r', encoding='utf-8') as file:
                if file.readline().rstrip() != self.header:
                    raise Exception("File structure error!")
                for line in file:
                    yield line.rstrip("\n")
        except FileNotFoundError as err:
            print(err)

    def file_open_ordinary(self):
        try:
            with open(self.path_file, 'r', encoding='utf-8') as file:
                if file.readline().rstrip() != self.header:
                    raise Exception("File structure error!")
                return file.readlines()
        except FileNotFoundError as err:
            print(err)

    def split_line(self):
        def split_one(row):
            l = []
            line = row.split(',')
            l.append(line[0])
            l.append(row.split('\"')[1])
            l.append(line[-1])
            return (l)

        lines = []
        for row in self.file_data:
            line = row[:-1].split(',')
            if len(line) > 3:
                lines.append(split_one(row[:-1]))
            else:
                lines.append(line)

        return [[l.strip() for l in line] for line in lines][1:]

    # Makes a dictionary from a list where keys are list items and the values are counts
    # Sorts it by counts descendingly
    def lst_sort(self, lst, reverse=False):
        return dict(sorted(Counter(lst).items(), key=lambda x: x[1], reverse=reverse))

    def dict_sort(self, dct, reverse=False):
        return dict(sorted(dct.items(), key=lambda x: x[1], reverse=reverse))

    # The method returns a dict or an OrderedDict where the keys are years and the values are counts.
    # You need to extract years from the titles. Sort it by counts descendingly.
    def dist_by_release(self):
        years_list = []
        for line in self.file_data:
            if re.findall(r'\(\d{4}\)', line):
                years_list.append(re.findall(r'\(\d{4}\)', line)[0].strip("()"))
            elif re.findall(r'\(\d{4}–\d{4}\)', line):
                years_list.append(re.findall(r'\(\d{4}–\d{4}\)', line)[0].strip("()"))
            else:
                years_list.append("year not specified")
        release_years = self.lst_sort(years_list, reverse=True)

        return release_years

    # The method returns a dict where the keys are genres and the values are counts.
    # Sort it by counts descendingly.
    def dist_by_genres(self):
        genre_list = []
        for line in self.file_data:
            for genre in line.rstrip().rsplit(',', maxsplit=1)[1].split('|'):
                genre_list.append(genre)

        genres = self.lst_sort(genre_list, reverse=True)

        return genres

    # The method returns a dict with top-n movies where the keys are movie titles and
    # the values are the number of genres of the movie. Sort it by numbers descendingly.
    def most_genres(self, n):
        lines = self.split_line()

        most_genres = []
        for line in lines:
            if line[1][-1] == ')':
                key = line[1][:-7]
            else:
                key = line[1]
            value = line[2].strip('()').count('|') + 1
            most_genres.append([key, value])

        most_genres.sort(key=lambda x: x[1], reverse=True)
        movies = dict(most_genres[:n])
        return movies
