# irina
import re
from collections import Counter


class Movies:
    # Analyzing data from movies.csv

    def __init__(self, path_to_the_file):
        try:
            with open(path_to_the_file, 'r', encoding='utf-8') as file:
                self.file_data = file.readlines()
        except FileNotFoundError as err:
            print(err)

    # def spit_file(self):
    #     file_list = []
    #     line_list = []
    #     for line in self.file_data:
    #         line = line.rstrip()
    #         line_list = line.split(',', maxsplit=1)
    #         line_list.append(line_list.pop(1).rsplit(',', maxsplit=1))
    #         print(line_list)

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
    def count_sort(self, lst):

        cnt = Counter(lst)
        dct = dict(cnt)
        dct_sorted_key = dict(sorted(dct.items(), key=lambda x: x[1], reverse=True))

        return dct_sorted_key

    # The method returns a dict or an OrderedDict where the keys are years and the values are counts.
    # You need to extract years from the titles. Sort it by counts descendingly.
    def dist_by_release(self):
        # irina code
        lines = self.split_line()
        years = [line[1][-5:-1] if line[1][-1] == ')' else 'no year' for line in lines]
        release_years = self.count_sort(years)
        print("Irina")
        print(release_years)

        # salavat code
        years_list = []
        for line in self.file_data:
            if re.findall(r'\(\d{4}\)', line):
                years_list.append(re.findall(r'\(\d{4}\)', line)[0].strip("()"))
            elif re.findall(r'\(\d{4}–\d{4}\)', line):
                years_list.append(re.findall(r'\(\d{4}–\d{4}\)', line)[0].strip("()"))
                print(years_list)
            else:
                years_list.append("year not specified")

        # years_list = [re.findall(r'\(\d{4}\)', line)[0][1:-1] if re.findall(r'\(\d{4}\)', line) or re.findall(r'\(
        # \d{4}–\d{4}\)', line) else "no year" for line in self.file_data[1:]]

        try:
            with open(f'../output_dataset/test.csv', 'w') as output_file:
                output_file.write("value\n")
                for value in years_list:
                    output_file.write(value)
                    output_file.write("\n")
        except FileNotFoundError as err:
            print(err)

        # print(years_list)
        release_years = Counter(years_list)
        # sub = Counter(years) == release_years
        # print(sub)

        return release_years

    # The method returns a dict where the keys are genres and the values are counts.
    # Sort it by counts descendingly.
    def dist_by_genres(self):
        # irina code
        genres_lst = []
        lines = self.split_line()
        for line in lines:
            genre = line[2].strip('()').split('|')
            for g in genre:
                genres_lst.append(g)
        genres = self.count_sort(genres_lst)
        print("Irina")
        print(genres)

        # salavat code
        genre_list = []
        for line in self.file_data[1:]:
            for genre in line.rstrip().rsplit(',', maxsplit=1)[1].split('|'):
                genre_list.append(genre)

        print(genre_list)

        genres = Counter(genre_list)
        # print(genres)
        return genres

    # The method returns a dict with top-n movies where the keys are movie titles and
    # the values are the number of genres of the movie. Sort it by numbers descendingly.
    def most_genres(self, n):
        movie_dict = dict()
        lines = self.split_line()

        for line in lines:
            if line[1][-1] == ')':
                key = line[1][:-7]
            else:
                key = line[1]
            value = len(line[2].strip('()').split('|'))
            # value = line[2].strip('()').count('|') + 1
            movie_dict[key] = value

        dct_sorted = dict(sorted(movie_dict.items(), key=lambda x: x[1], reverse=True))
        keys = list(dct_sorted.keys())[:n]
        values = list(dct_sorted.values())[:n]
        movies = dict(zip(keys, values))

        # print(movies)

        # movie_list = []
        # for line in self.file_data[1:]:
        #     temp_list = line.rstrip().rsplit(',', maxsplit=1)
        #     name = temp_list[0].split(',')[1]
        #     if re.findall(r'\(\d{4}\)', name):
        #         name = name[:-7].strip('"')
        #     movie_list.append([name, temp_list[1].count('|') + 1])
        #
        # movie_list.sort()
        # print(movie_list)

        return movies
