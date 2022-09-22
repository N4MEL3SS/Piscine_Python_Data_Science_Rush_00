from links import Links
from movies import Movies
from ratings import Ratings
from tags import Tags
import config


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


def main():
    file_path = "../dataset/ratings.csv"
    rating_class = Ratings(file_path)
    print(rating_class.Movies.dist_by_year())


if __name__ == '__main__':
    main()
