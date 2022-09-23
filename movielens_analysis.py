import re
import datetime
from collections import Counter
from collections import defaultdict


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

    def get_movies_title(self):
        movie_title_dict = {}

        for line in self.file_data:
            movie_id = line[:line.find(',')]
            title = line[line.find(',') + 1:line.rfind(',')].strip('" ')

            if re.findall(r'\(\d{4}\)', title):
                title = title[:-7]
            elif re.findall(r'\(\d{4}–\d{4}\)', title):
                title = title[:-12]

            movie_title_dict[movie_id] = title

        return movie_title_dict

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


class Ratings:
    # Analyzing data from ratings.csv

    def __init__(self, path_to_the_file, has_order=True):
        self.path_file = path_to_the_file
        self.header = ('userId,movieId,rating,timestamp')
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

    def get_file(self):
        return self.file_data

    def lst_sort(self, lst, key, reverse=False):
        return dict(sorted(Counter(lst).items(), key=lambda x: x[key], reverse=reverse))

    class Movies:
        def __init__(self, ratings, movie_title=None):
            self.ratings = ratings
            self.movie_title = movie_title

        # The method returns a dict where the keys are years and the values are counts.
        # Sort it by years ascendingly. You need to extract years from timestamps.
        def dist_by_year(self):
            years = []
            for line in self.ratings.file_data:
                timestamp = int(line.rsplit(',', maxsplit=1)[1].rstrip())
                data = datetime.datetime.fromtimestamp(timestamp)
                years.append(str(data)[:4])

            ratings_by_year = self.ratings.lst_sort(years, 0)

            return ratings_by_year

        # The method returns a dict where the keys are ratings and the values are counts.
        # Sort it by ratings ascendingly.
        def dist_by_rating(self):
            ratings_list = []
            for line in self.ratings.file_data:
                ratings_list.append(line.rsplit(',', maxsplit=2)[1].rstrip())

            ratings_distribution = self.ratings.lst_sort(ratings_list, 1)

            return ratings_distribution

        # The method returns top-n movies by the number of ratings.
        # It is a dict where the keys are movie titles and the values are numbers.
        # Sort it by numbers descendingly.
        def top_by_num_of_ratings(self, n):
            movies_id = []
            for line in self.ratings.file_data:
                movies_id.append(line.split(',', maxsplit=2)[1].rstrip())
            # print(movies_id)

            top_movies = {}
            for key, value in Counter(movies_id).most_common(n):
                if self.movie_title.get(key):
                    top_movies[self.movie_title[key]] = value
                else:
                    raise Exception("Undefined movieID!")

            return top_movies

        def median(self, lst):
            sorted_lst = sorted(lst)
            lst_len = len(lst)
            index = (len(lst) - 1) // 2

            if lst_len % 2:
                return sorted_lst[index]
            else:
                return (sorted_lst[index] + sorted_lst[index + 1]) / 2.0

        # The method returns top-n movies by the average or median of the ratings.
        # It is a dict where the keys are movie titles and the values are metric values.
        # Sort it by metric descendingly.
        # The values should be rounded to 2 decimals.
        def top_by_ratings(self, n, metric='average'):
            id_rates = []
            movies = {}

            for line in self.ratings.file_data:
                info = line.split(',')
                id_rates.append((info[1], info[2]))

            id_rat_dict = collections.defaultdict(list)
            for i in range(len(id_rates)):
                id_rat_dict[id_rates[i][0]].append(float(id_rates[i][1]))

            if metric == 'average':
                for k, v in id_rat_dict.items():
                    movies[k] = round(sum(v) / len(v), 2)
            elif metric == 'median':
                for k, v in id_rat_dict.items():
                    movies[k] = round(self.median(v), 2)
            else:
                raise ValueError('No such metric')

            y = {}
            for k in movies.keys():
                y[self.movie_title[k]] = movies[k]

            x = {k: v for k, v in sorted(y.items(), key=lambda item: item[1], reverse=True)}
            top_movies = dict(Counter(x).most_common(n))

            return top_movies

        def variance(self, data):
            mean = sum(data) / len(data)
            deviations = [(x - mean) ** 2 for x in data]

            return sum(deviations) / len(data)

        # The method returns top-n movies by the variance of the ratings.
        # It is a dict where the keys are movie titles and the values are the variances.
        # Sort it by variance descendingly.
        # The values should be rounded to 2 decimals.
        def top_controversial(self, n):
            id_rates = []
            movies = {}

            for line in self.ratings.file_data:
                info = line.split(',')
                id_rates.append((info[1], info[2]))

            id_rat_dict = defaultdict(list)

            for i in range(len(id_rates)):
                id_rat_dict[id_rates[i][0]].append(float(id_rates[i][1]))

            for k, v in id_rat_dict.items():
                movies[k] = round(self.variance(v), 2)

            y = {}

            for k in movies.keys():
                y[self.movie_title[k]] = movies[k]

            x = {k: v for k, v in sorted(y.items(), key=lambda item: item[1], reverse=True)}
            top_movies = dict(Counter(x).most_common(n))

            return top_movies

    # In this class, three methods should work.
    # The 1st returns the distribution of users by the number of ratings made by them.
    # The 2nd returns the distribution of users by average or median ratings made by them.
    # The 3rd returns top-n users with the biggest variance of their ratings.
    # Inherit from the class Movies. Several methods are similar to the methods from it.
    class Users:
        pass

