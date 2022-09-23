#  salavat
import datetime
from collections import Counter


class Ratings:
    # Analyzing data from ratings.csv

    def __init__(self, path_to_the_file, has_order=True):
        self.path_file = path_to_the_file

        if has_order:
            try:
                with open(path_to_the_file, 'r', encoding='utf-8') as file:
                    self.file_data = file.readlines()
            except FileNotFoundError as err:
                print(err)

    def file_open(self):
        try:
            with open(self.path_file, 'r', encoding='utf-8') as file:
                for line in file:
                    yield line
        except FileNotFoundError as err:
            print(err)

    def get_file(self):
        return self.file_data

    def lst_sort(self, lst, key, reverse=False):
        return dict(sorted(Counter(lst).items(), key=lambda x: x[key], reverse=reverse))

    class Movies:
        def __init__(self, ratings):
            self.ratings = ratings

        # The method returns a dict where the keys are years and the values are counts.
        # Sort it by years ascendingly. You need to extract years from timestamps.
        def dist_by_year(self):
            years = []
            for line in self.ratings.file_data[1:]:
                timestamp = int(line.rsplit(',', maxsplit=1)[1].rstrip())
                data = datetime.datetime.fromtimestamp(timestamp)
                years.append(str(data)[:4])

            # years = [str(datetime.datetime.fromtimestamp(int(line.rsplit(',', maxsplit=1)[1].rstrip())))[:4] for
            # line in self.ratings.file_data[1:]]

            ratings_by_year = self.ratings.lst_sort(years, 0)

            return ratings_by_year

        # The method returns a dict where the keys are ratings and the values are counts.
        # Sort it by ratings ascendingly.
        def dist_by_rating(self):
            ratings_list = []
            for line in self.ratings.file_data[1:]:
                ratings_list.append(line.rsplit(',', maxsplit=2)[1].rstrip())

            ratings_distribution = self.ratings.lst_sort(ratings_list, 1)

            return ratings_distribution

        # The method returns top-n movies by the number of ratings.
        # It is a dict where the keys are movie titles and the values are numbers.
        # Sort it by numbers descendingly.
        def top_by_num_of_ratings(self, n):
            top_movies = {}

            return top_movies

        # The method returns top-n movies by the average or median of the ratings.
        # It is a dict where the keys are movie titles and the values are metric values.
        # Sort it by metric descendingly.
        # The values should be rounded to 2 decimals.
        def top_by_ratings(self, n, metric=True):  # average
            top_movies = {}

            return top_movies

        # The method returns top-n movies by the variance of the ratings.
        # It is a dict where the keys are movie titles and the values are the variances.
        # Sort it by variance descendingly.
        # The values should be rounded to 2 decimals.
        def top_controversial(self, n):
            top_movies = {}

            return top_movies

    # In this class, three methods should work.
    # The 1st returns the distribution of users by the number of ratings made by them.
    # The 2nd returns the distribution of users by average or median ratings made by them.
    # The 3rd returns top-n users with the biggest variance of their ratings.
    # Inherit from the class Movies. Several methods are similar to the methods from it.
    class Users:
        pass
