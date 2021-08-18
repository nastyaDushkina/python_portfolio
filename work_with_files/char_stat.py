# -*- coding: utf-8 -*-


import zipfile
import os.path

FILE_NAME = os.path.normpath('python_snippets/voyna-i-mir.txt.zip')


class CollectionStatistic:

    def __init__(self, file_name):
        self.file_name = file_name
        self.total_count = 0
        self.stat = {}

    def execute(self):
        self.prepare_file()
        self.collect_stat()
        self.prepare_necessary_stat()
        self.sort_stat()
        self.print_statistic()

    def prepare_file(self):
        if self.file_name.endswith('.zip'):
            self.unzip()

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
        self.file_name = filename

    def collect_stat(self):
        self.currrent_char = ' '
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._collect_for_line(line=line[:-1])

    def _collect_for_line(self, line):
        for char in line:
            self.stat[char] = self.stat.setdefault(char, 0) + 1

    def prepare_necessary_stat(self):
        self.required_statistic = []
        for char, count in self.stat.items():
            if char.isalpha():
                self.required_statistic.append([char, count])
                self.total_count += count

    def sort_stat(self):
        sort_params = self.get_sort_key()
        self.required_statistic.sort(key=sort_params[0], reverse=sort_params[1])

    def get_sort_key(self):  # Поправил имя немного
        return (lambda i: i[1], True)

    def print_statistic(self):
        print('+' + '-' * 23 + '+')
        print('|   буква   |' + '  частота  |')
        print('+' + '-' * 23 + '+')
        for char, count in self.required_statistic:
            print(f'|   {char:^5}   |  {count:^7}  |')
        print('+' + '-' * 23 + '+')
        print(f'|   итого:  |{self.total_count:^11}|')
        print('+' + '-' * 23 + '+')


class SortFrequencyAscending(CollectionStatistic):

    def get_sort_key(self):
        return (lambda i: i[1], False)


class SortAlphabetAscending(CollectionStatistic):

    def get_sort_key(self):
        return (lambda i: i[0], False)


class SortAlphabetDescending(CollectionStatistic):

    def get_sort_key(self):
        return (lambda i: i[0], True)


# statistic = CollectionStatistic(file_name=FILE_NAME)
# statistic = SortFrequencyAscending(file_name=FILE_NAME)
statistic = SortAlphabetAscending(file_name=FILE_NAME)
# statistic = SortAlphabetDescending(file_name=FILE_NAME)
statistic.execute()
