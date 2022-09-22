import links
import movies
import ratings
import tags


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
    pass


if __name__ == '__main__':
    main()
