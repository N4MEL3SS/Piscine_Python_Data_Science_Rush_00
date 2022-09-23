#irina
import re
from collections import Counter

class Tags:
    """
    Analyzing data from tags.csv
    """

    # def __init__(self, path_to_the_file):
    #     try:
    #         with open(path_to_the_file, 'r') as file:
    #             self.file_data = file.readlines()
    #     except FileNotFoundError as err:
    #         print(err)

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
        tag_list = [line[2] for line in lines if line[2].find(word) >= 0]
        # tag_list = [line[2] for line in lines]
        # tag_str = ('\n').join(tag_list)
        # for tag in tag_list:
        #     if re.findall(r'([W-w]ar)', tag):
        #         print(tag)
        tags_with_word = list(sorted(set(tag_list)))
        # или спилитить и искать по отдельным словам?
        return tags_with_word

if __name__ == '__main__':
    t = Tags('../dataset/tags.csv')
    print(t.most_words(10))
    print(t.longest(10))
    print(t.most_words_and_longest(10))
    print(t.most_popular(10))
    print(t.tags_with('war'))
