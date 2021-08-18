# -*- coding: utf-8 -*-


PROC_FILE_NAME = 'events.txt'
REC_FILE_NAME = 'collected_statistic.txt'


class CollectStat:

    def __init__(self, file_name):
        self.processed_file = file_name
        self.stat_nok = {}
        self.sign_time = 0

    def execute(self):
        self.setup_sign_time()
        self.collect()

    def collect(self):
        with open(REC_FILE_NAME, mode='w+') as new_file:
            with open(self.processed_file, mode='r') as file:
                current_time = None
                for line in file:
                    if line[1:self.sign_time] != current_time:
                        if current_time and self.stat_nok[current_time]:
                            new_file.write(f'[{current_time}] {self.stat_nok[current_time]}\n')
                        current_time = line[1:self.sign_time]
                        self.stat_nok[current_time] = 0
                    if line.endswith('NOK\n'):
                        self.stat_nok[current_time] += 1
                if current_time and self.stat_nok[current_time]:
                    new_file.write(f'[{current_time}] {self.stat_nok[current_time]}\n')

    def setup_sign_time(self):
        self.sign_time = 17


class CollectStatPerHour(CollectStat):

    def setup_sign_time(self):
        self.sign_time = 14


class CollectStatPerDay(CollectStat):

    def setup_sign_time(self):
        self.sign_time = 11


class CollectStatPerMonth(CollectStat):

    def setup_sign_time(self):
        self.sign_time = 8


class CollectStatPerYear(CollectStat):

    def setup_sign_time(self):
        self.sign_time = 5


statistic = CollectStat(file_name=PROC_FILE_NAME)
# statistic = CollectStatPerHour(file_name=PROC_FILE_NAME)
# statistic = CollectStatPerDay(file_name=PROC_FILE_NAME)
# statistic = CollectStatPerMonth(file_name=PROC_FILE_NAME)
# statistic = CollectStatPerYear(file_name=PROC_FILE_NAME)
statistic.execute()
