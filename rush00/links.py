#  salavat
import re
from collections import Counter

import requests
from random import choices
from bs4 import BeautifulSoup


class Links:
    """
    Analyzing data from links.csv
    """

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
