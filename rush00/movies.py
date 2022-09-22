#irina
from collections import Counter


class Movies:
    """
    Analyzing data from movies.csv
    """

    def __init__(self, path_to_the_file):
        try:
            with open(path_to_the_file, 'r') as file:
                self.file_data = file.readlines()
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

    def count_sort(self, lst):
        """
        Makes a dictionary from a list where keys are list items and the values are counts
        Sorts it by counts descendingly
        """
        cnt = Counter(lst)
        dct = dict(cnt)
        dct_sorted_key = dict(sorted(dct.items(), key=lambda x: x[1], reverse=True))
        return dct_sorted_key

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        lines = self.split_line()
        years = [line[1][-5:-1] if line[1][-1] == ')' else 'no year' for line in lines]
        release_years = self.count_sort(years)
        # print(release_years)
        return release_years

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres_lst = []
        lines = self.split_line()
        for line in lines:
            genre = line[2].strip('()').split('|')
            for g in genre:
                genres_lst.append(g)
        genres = self.count_sort(genres_lst)
        # print(genres)
        return genres

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """

        movie_dict = dict()
        lines = self.split_line()
        for line in lines:
            if line[1][-1] == ')':
                key = line[1][:-7]
            else:
                key = line[1]
            value = len(line[2].strip('()').split('|'))
            movie_dict[key] = value
        dct_sorted = dict(sorted(movie_dict.items(), key=lambda x: x[1], reverse=True))
        keys = list(dct_sorted.keys())[:n]
        values = list(dct_sorted.values())[:n]
        movies = dict(zip(keys, values))
        # print(movies)
        return movies
