import re
import datetime
from collections import Counter
from collections import defaultdict
from random import choices
from bs4 import BeautifulSoup
import requests


# -------------------------------#
#         Movies class          #
# -------------------------------#


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


# -------------------------------#
#        Ratings class          #
# -------------------------------#


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
                years.append(int(str(data)[:4]))

            ratings_by_year = self.ratings.lst_sort(years, 0)

            return ratings_by_year

        # The method returns a dict where the keys are ratings and the values are counts.
        # Sort it by ratings ascendingly.
        def dist_by_rating(self):
            ratings_list = []
            for line in self.ratings.file_data:
                ratings_list.append(float(line.rsplit(',', maxsplit=2)[1].rstrip()))

            ratings_distribution = self.ratings.lst_sort(ratings_list, 0)

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

            id_rat_dict = defaultdict(list)
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
    class Users(Movies):

        def __init__(self, ratings, movie_title=None):
            self.ratings = ratings
            self.movie_title = movie_title

        # The 1st returns the distribution of users by the number of ratings made by them.
        def users_rating_count(self):
            users_id = []
            for line in self.ratings.file_data:
                users_id.append(int(line.split(',', maxsplit=1)[0].rstrip()))
            ratings_user = self.ratings.lst_sort(Counter(users_id), 1, False)
            return ratings_user

        # The 2nd returns the distribution of users by average or median ratings made by them.
        def users_metric_count(self, metric='average'):
            users_rates = []
            users = {}

            for line in self.ratings.file_data:
                info = line.split(',')
                users_rates.append((info[0], info[2]))

            id_rat_dict = defaultdict(list)
            for i in range(len(users_rates)):
                id_rat_dict[users_rates[i][0]].append(float(users_rates[i][1]))

            if metric == 'average':
                for k, v in id_rat_dict.items():
                    users[k] = round(sum(v) / len(v), 2)
            elif metric == 'median':
                for k, v in id_rat_dict.items():
                    users[k] = round(self.median(v), 2)
            else:
                raise ValueError('No such metric')

            sorted_users = self.ratings.dict_sort(users, True)
            return sorted_users

        # The 3rd returns top-n users with the biggest variance of their ratings.
        def users_variance_count(self, n):
            users_rates = []
            users = {}

            for line in self.ratings.file_data:
                info = line.split(',')
                users_rates.append((int(info[0]), info[2]))

            id_rat_dict = defaultdict(list)

            for i in range(len(users_rates)):
                id_rat_dict[users_rates[i][0]].append(float(users_rates[i][1]))

            for k, v in id_rat_dict.items():
                users[k] = round(self.variance(v), 2)

            top_users = dict(Counter(users).most_common(n))

            return top_users


# -------------------------------#
#          Tags class           #
# -------------------------------#


class Tags:
    """
    Analyzing data from tags.csv
    """

    def __init__(self, path_to_the_file, has_order=True):
        self.path_file = path_to_the_file
        self.header = ('userId,movieId,tag,timestamp')
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

    def clean_text(self, text):
        text = text.replace(' - ', ' ')  # removing '-'
        text = text.replace('/', ' ')  # removing '/'
        return text

    def most_words(self, n):
        """
        The method returns top-n tags with most words inside. It is a dict
        where the keys are tags and the values are the number of words inside the tag.
        Drop the duplicates. Sort it by numbers descendingly.
        """
        tag_list = []
        lines = [row.split(',') for row in self.file_data[1:]]
        for line in lines:
            key = line[2]
            value = len(self.clean_text(key).split(' '))
            tag_list.append([key, value])
        tag_list.sort(key=lambda x: x[1], reverse=True)
        big_tags = dict(tag_list[:n])
        return big_tags

    def longest(self, n):
        """
        The method returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Drop the duplicates. Sort it by numbers descendingly.
        """
        tag_list = []
        lines = [row.split(',') for row in self.file_data[1:]]
        for line in lines:
            key = line[2]
            value = len(key)
            tag_list.append([key, value])
        tag_list.sort(key=lambda x: x[1], reverse=True)
        tag_dict = dict(tag_list[:n])
        big_tags = list(tag_dict.keys())
        return big_tags

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        a = list(self.most_words(n).keys())
        b = self.longest(n)
        big_tags = list(set(a) & set(b))
        big_tags.sort(key=lambda x: len(x), reverse=True)
        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags.
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        lines = [row.split(',') for row in self.file_data[1:]]
        tags = [line[2] for line in lines]
        cnt = Counter(tags)
        popular_tags = dict(cnt.most_common(n))
        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        lines = [row.split(',') for row in self.file_data[1:]]
        # tag_list = [line[2] for line in lines if line[2].find(word) >= 0]
        tag_list = [line[2] for line in lines]

        tags_with_word = set()

        for eq in tag_list:
            for sep_word in eq.split(" "):
                if sep_word.lower() == word.lower():
                    tags_with_word.add(eq)

        tags_with_word = list(sorted(tags_with_word))

        return tags_with_word


# -------------------------------#
#          Links class          #
# -------------------------------#


class Links:
    # Analyzing data from links.csv

    def __init__(self, path_to_the_file, movie_title, has_order=True, links_on=False):
        self.path_file = path_to_the_file
        self.movie_title = movie_title
        self.header = ('movieId,imdbId,tmdbId')
        self.links_on = links_on
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

    def get_movies_id(self):
        return [id_from_file.split(',') for id_from_file in self.file_data]

    def connect_to_server(self, imdbId):
        url = f'https://www.imdb.com/title/tt{imdbId}/'

        page = requests.get(url)
        if page.status_code != 200:
            raise ValueError("URL doesn't exist")
        soup = BeautifulSoup(page.text, "html.parser")
        if self.links_on:
            print(url)

        return soup

    def parse_director(self, html_soup):
        director = html_soup.find('a', class_="ipc-metadata-list-item__list-content-item "
                                              "ipc-metadata-list-item__list-content-item--link").text

        return director

    def parse_budget(self, html_soup):
        try:
            budget = html_soup.find('div', attrs={"data-testid": "title-boxoffice-section"}).div.text
            budget = budget.split("(")[0].strip(" ")
        except:
            return "0"

        return budget

    def parse_gross(self, html_soup):
        gross_soup = html_soup.find_all('li', class_="ipc-metadata-list__item sc-6d4f3f8c-2 fJEELB")
        gross = []

        for val in gross_soup:
            a = val.select_one('span.ipc-metadata-list-item__label')
            if a is not None and 'Gross worldwide' in a.text:
                gross = val.select_one('span.ipc-metadata-list-item__list-content-item').text

        if len(gross) == 0:
            return "0"
        return gross

    def parse_runtime(self, html_soup):
        runtime_soup = html_soup.find_all('li', class_="ipc-metadata-list__item")
        runtime = []

        for val in runtime_soup:
            a = val.select_one('span.ipc-metadata-list-item__label')
            if a is not None and 'Runtime' in a.text:
                runtime = val.select_one('div.ipc-metadata-list-item__content-container').text

        return runtime

    # The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the
    # argument (movieId). For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime]. The values
    # should be parsed from the IMDB webpages of the movies. Sort it by movieId descendingly.
    def get_imdb(self, list_of_movies, list_of_fields):
        id_list = [id_from_file for id_from_file in list_of_movies]

        imdb_info = []

        for movie_id in id_list[:3]:
            imdb_pars = [movie_id[0]]
            imdb_id = movie_id[1]
            soup = self.connect_to_server(imdb_id)
            for value in list_of_fields:
                if value == 'Director':
                    imdb_pars.append(self.parse_director(soup))
                elif value == 'Budget':
                    imdb_pars.append(self.parse_budget(soup))
                elif value == 'Cumulative Worldwide Gross':
                    imdb_pars.append(self.parse_gross(soup))
                elif value == 'Runtime':
                    imdb_pars.append(self.parse_runtime(soup))
            imdb_info.append(imdb_pars)

        return imdb_info

    # The method returns a dict with top-n directors where the keys are directors and
    # the values are numbers of movies created by them. Sort it by numbers descendingly.

    def random_list(self, n):
        imdb_list = [movie_id for movie_id in self.get_movies_id()]

        return choices(imdb_list, k=n)

    def top_directors(self, n, rand_size=10):
        director_list = []
        random_list = self.random_list(rand_size)

        for value in random_list:
            soup = self.connect_to_server(value[1])
            director_list.append(self.parse_director(soup))

        directors = dict(sorted(Counter(director_list).most_common(n), key=lambda x: (x[1], x[0]), reverse=True))

        return directors

    # The method returns a dict with top-n movies where the keys are movie titles and
    # the values are their budgets. Sort it by budgets descendingly.
    def most_expensive(self, n, rand_size=10):
        budgets_dict = {}
        random_list = self.random_list(rand_size)

        for value in random_list:
            if self.movie_title.get(value[0]):
                soup = self.connect_to_server(value[1])
                money = re.sub("[^0-9]", "", self.parse_budget(soup).replace(',', ''))
                budgets_dict[self.movie_title[value[0]]] = int(money)

        budgets = dict(sorted(Counter(budgets_dict).most_common(n), key=lambda x: (x[1], x[0]), reverse=True))

        return budgets

    # The method returns a dict with top-n movies where the keys are movie titles and
    # the values are the difference between cumulative worldwide gross and budget.
    # Sort it by the difference descendingly.
    def most_profitable(self, n, rand_size=10):
        profit_dict = {}
        random_list = self.random_list(rand_size)

        for value in random_list:
            if self.movie_title.get(value[0]):
                soup = self.connect_to_server(value[1])
                money = re.sub("[^0-9]", "", self.parse_budget(soup).replace(',', ''))
                profit = re.sub("[^0-9]", "", self.parse_gross(soup).replace(',', ''))
                prof_money = int(profit) - int(money)
                # print("prof:", profit)
                # print("budget:", money)
                # print("profit =", prof_money)
                profit_dict[self.movie_title[value[0]]] = prof_money

        profits = dict(sorted(Counter(profit_dict).most_common(n), key=lambda x: (x[1], x[0]), reverse=True))

        return profits

    # The method returns a dict with top-n movies where the keys are movie titles and
    # the values are their runtime. If there are more than one version â€“ choose any.
    # Sort it by runtime descendingly.
    def longest(self, n, rand_size=10):
        runtime_dict = {}
        random_list = self.random_list(rand_size)

        for value in random_list:
            if self.movie_title.get(value[0]):
                soup = self.connect_to_server(value[1])
                runtime = self.parse_runtime(soup)
                t = runtime.split(" ")
                minut_time = int(t[0]) * 60 + int(t[2])
                runtime_dict[self.movie_title[value[0]]] = minut_time

        runtimes = dict(sorted(Counter(runtime_dict).most_common(n), key=lambda x: (x[1], x[0]), reverse=True))

        return runtimes

    # The method returns a dict with top-n movies where the keys are movie titles and the values are the budgets divided
    # by their runtime. The budgets can be in different currencies â€“ do not pay attention to it. The values should
    # be rounded to 2 decimals. Sort it by the division descendingly.
    def top_cost_per_minute(self, n, rand_size=10):
        cost_dict = {}
        random_list = self.random_list(rand_size)

        for value in random_list:
            if self.movie_title.get(value[0]):
                soup = self.connect_to_server(value[1])
                runtime = self.parse_runtime(soup)
                try:
                    t = runtime.split(" ")
                    minute_time = 1
                    if len(t) == 4:
                        minute_time = int(t[0]) * 60 + int(t[2])
                    elif len(t) == 2:
                        minute_time = int(t[2])
                    money = re.sub("[^0-9]", "", self.parse_budget(soup).replace(',', ''))
                    cost = round(int(money) / minute_time, 2)
                except:
                    cost = 0
                cost_dict[self.movie_title[value[0]]] = cost

        costs = dict(sorted(Counter(cost_dict).most_common(n), key=lambda x: (x[1], x[0]), reverse=True))

        return costs


class Test:
    def setup_class(self):
        self.tags = Tags("ml-latest-small/tags.csv")
        self.movies = Movies('ml-latest-small/movies.csv')
        self.ratings = Ratings('ml-latest-small/ratings.csv')
        self.ratings_subclass_movie = self.ratings.Movies(self.ratings, self.movies.get_movies_title())
        self.ratings_subclass_user = self.ratings.Users(self.ratings)
        self.links = Links('ml-latest-small/links.csv', 'ml-latest-small/movies.csv')
        self.list_of_fields = ['movieId', 'Director', 'Budget', 'Cumulative Worldwide Gross', 'Runtime']

    # ______________________________________
    # Test for Movies class
    # ______________________________________

    def test__dist_by_release_type(self):
        result = self.movies.dist_by_release()
        assert isinstance(result, dict)

    def test__dist_by_release_sorted(self):
        result = self.movies.dist_by_release()
        releases = list(result.values())
        sort_state = True
        for i in range(1, len(releases)):
            if releases[i - 1] < releases[i]:
                sort_state = False
                break
        assert sort_state

    def test__dist_by_genres_type(self):
        result = self.movies.dist_by_genres()
        assert isinstance(result, dict)

    def test__dist_by_genres_sorted(self):
        result = self.movies.dist_by_genres()
        releases = list(result.values())
        sort_state = True
        for i in range(1, len(releases)):
            if releases[i - 1] < releases[i]:
                sort_state = False
                break
        assert sort_state

    def test__most_genres_type(self):
        result = self.movies.most_genres(10)
        assert isinstance(result, dict)

    def test__most_genres_sorted(self):
        result = self.movies.most_genres(25)
        releases = list(result.values())
        sort_state = True
        for i in range(1, len(releases)):
            if releases[i - 1] < releases[i]:
                sort_state = False
                break
        assert sort_state

    def test__movies__dist_by_years__types(self):
        result = self.ratings_subclass_movie.dist_by_year()
        assert isinstance(result, dict)

        is_correct_types = True
        for year, count in result.items():
            if not isinstance(year, int) or not isinstance(count, int):
                print(year, count)
                is_correct_types = False
                break
        assert is_correct_types

    def test__movies__dist_by_years__is_sorted(self):
        result = self.ratings_subclass_movie.dist_by_year()

        keys = list(result.keys())
        is_sorted = True
        for i in range(1, len(keys)):
            if keys[i - 1] > keys[i]:
                is_sorted = False
                break
        assert is_sorted

    def test__movies__dist_by_rating__types(self):
        result = self.ratings_subclass_movie.dist_by_rating()
        assert isinstance(result, dict)

        is_correct_types = True
        for rating, count in result.items():
            if not isinstance(rating, float) or not isinstance(count, int):
                is_correct_types = False
                break
        assert is_correct_types

    def test__movies__dist_by_rating__is_sorted(self):
        result = self.ratings_subclass_movie.dist_by_rating()

        keys = list(result.keys())
        is_sorted = True
        for i in range(1, len(keys)):
            if keys[i - 1] > keys[i]:
                is_sorted = False
                break
        assert is_sorted

    def test__movies__top_by_num_of_ratings__types(self):
        result = self.ratings_subclass_movie.top_by_num_of_ratings(10)
        print(result)
        assert isinstance(result, dict)

        is_correct_types = True
        for rating, count in result.items():
            if not isinstance(rating, str) or not isinstance(count, int):
                is_correct_types = False
                break
        assert is_correct_types

        assert len(result) == 10

    def test__movies__top_by_num_of_ratings__is_sorted(self):
        result = self.ratings_subclass_movie.top_by_num_of_ratings(10)
        values = list(result.values())
        is_sorted = True
        for i in range(1, len(values)):
            if values[i - 1] < values[i]:
                is_sorted = False
                break
        assert is_sorted

        assert len(result) == 10

    def test__movies__top_by_ratings__types(self):
        result = self.ratings_subclass_movie.top_by_ratings(10)
        assert isinstance(result, dict)

        is_correct_types = True
        for rating, count in result.items():
            if not isinstance(rating, str) or not isinstance(count, float):
                is_correct_types = False
                break
        assert is_correct_types

        assert len(result) == 10

    def test__movies__top_by_ratings__is_sorted(self):
        result = self.ratings_subclass_movie.top_by_ratings(10)

        values = list(result.values())
        is_sorted = True
        for i in range(1, len(values)):
            if values[i - 1] < values[i]:
                is_sorted = False
                break
        assert is_sorted

        assert len(result) == 10

    def test__movies__top_controversial__types(self):
        result = self.ratings_subclass_movie.top_controversial(10)

        assert isinstance(result, dict)

        is_correct_types = True
        for rating, count in result.items():
            if not isinstance(rating, str) or not isinstance(count, float):
                is_correct_types = False
                break
        assert is_correct_types

        assert len(result) == 10

    def test__movies__top_controversial__is_sorted(self):
        result = self.ratings_subclass_movie.top_controversial(10)

        values = list(result.values())
        is_sorted = True
        for i in range(1, len(values)):
            if values[i - 1] < values[i]:
                is_sorted = False
                break
        assert is_sorted

        assert len(result) == 10

    def test__users__dist_by_ratings_number__types(self):
        result = self.ratings_subclass_user.users_rating_count()
        assert isinstance(result, dict)

        is_correct_types = True
        for rating, count in result.items():
            if not isinstance(rating, int) or not isinstance(count, int):
                is_correct_types = False
                break
        assert is_correct_types

    def test__users__dist_by_ratings_number__is_sorted(self):
        result = self.ratings_subclass_user.users_rating_count()

        values = list(result.values())
        is_sorted = True
        for i in range(1, len(values)):
            if values[i - 1] > values[i]:
                is_sorted = False
                break
        assert is_sorted

    def test__users__top_by_variance__types(self):
        result = self.ratings_subclass_user.users_variance_count(10)
        assert isinstance(result, dict)

        is_correct_types = True
        for rating, count in result.items():
            if not isinstance(rating, int) or not isinstance(count, float):
                is_correct_types = False
                break
        assert is_correct_types

        assert len(result) == 10

    def test__users__top_by_variance__is_sorted(self):
        result = self.ratings_subclass_user.users_variance_count(10)

        values = list(result.values())
        is_sorted = True
        for i in range(1, len(values)):
            if values[i - 1] < values[i]:
                is_sorted = False
                break
        assert is_sorted

        assert len(result) == 10

    def test__most_words__types(self):
        result = self.tags.most_words(10)
        assert isinstance(result, dict)

    def test__most_words__is_sorted(self):
        result = self.tags.most_words(10)

        sorted_list = True
        words = list(result.values())
        for i in range(1, len(words)):
            if words[i - 1] < words[i]:
                sorted_list = False
                break
        assert sorted_list

    def test__longest__types(self):
        result = self.tags.longest(10)
        assert isinstance(result, list)

    def test__longest__is_sorted(self):
        result = self.tags.longest(10)
        sorted_list = True
        for i in range(1, len(result)):
            if len(result[i - 1]) < len(result[i]):
                sorted_list = False
                break
        assert sorted_list

    def test_most_words_and_longest_types(self):
        result = self.tags.most_words_and_longest(10)
        assert isinstance(result, list)

    def test_most_words_and_longest_duplicates(self):
        my_list = self.tags.most_words_and_longest(10)
        test_set = set(my_list)
        assert len(my_list) == len(test_set)

    def test_most_popular_type(self):
        result = self.tags.most_popular(10)
        assert isinstance(result, dict)

    def test_most_popular_duplicates(self):
        my_list = list(self.tags.most_popular(10).keys())
        test_set = set(my_list)
        assert len(my_list) == len(test_set)

    def test_most_popular_sorted(self):
        result = self.tags.most_popular(10)

        tag = list(result.values())
        sorted_list = True
        for i in range(1, len(tag)):
            if tag[i - 1] < tag[i]:
                sorted_list = False
                break

        assert sorted_list

        assert len(result) == 10

    def test_tags_with_out(self):
        word = 'comedy'
        result = self.tags.tags_with(word)
        check_word = True
        for i in range(len(result)):
            if word not in result[i].lower():
                check_word = False
                break
        assert check_word

    def test_tags_with_type(self):
        result = self.tags.tags_with('comedy')
        assert isinstance(result, list)

    def test_tags_with_dupl(self):
        my_list = list(self.tags.tags_with('comedy'))
        test_set = set(my_list)
        assert len(my_list) == len(test_set)

    def test_tags_with_sorted(self):
        result = self.tags.tags_with('comedy')
        sort_list = True
        for i in range(1, len(result)):
            if result[i - 1][0] > result[i][0]:
                sort_list = False
        assert sort_list
