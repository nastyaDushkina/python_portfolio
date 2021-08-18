# -*- coding: utf-8 -*-

import os
import time
import shutil

FILE_SOURCE = 'icons.zip'
DIR_FOR_REC = 'icons_by_year'

import zipfile


class FileDistributor:
    def __init__(self, path):
        self.path = path
        self.files_list = []
        self.sort_files = {}

    def execute(self):
        self.prepare_paths()
        self.collect_file_inf()
        self.sort()
        self.distribute_files()

    def prepare_paths(self):
        self.path = os.path.normpath(self.path)
        # print(self.path)
        self.parent_dir = os.path.dirname(self.path)
        # print(self.parent_dir)

    def collect_file_inf(self):
        for dirpath, dirname, filenames in os.walk(self.path):
            for file in filenames:
                full_file_path = os.path.join(dirpath, file)
                time_secs = os.path.getmtime(full_file_path)
                file_time = time.gmtime(time_secs)

                self.files_list.append([full_file_path, file_time[0], file_time[1]])

    def sort(self):
        for file in self.files_list:
            self.sort_files.setdefault(file[1], {})
            self.sort_files[file[1]].setdefault(file[2], [])
            self.sort_files[file[1]][file[2]].append(file[0])

    def distribute_files(self):
        for year, year_obj in self.sort_files.items():
            for month, list in year_obj.items():
                destination = os.path.join(DIR_FOR_REC, str(year), str(month))
                os.makedirs(destination)
                self.copy_files(destination, list)

    def copy_files(self, destination, list):
        for file in list:
            shutil.copy2(file, destination)


class FileZipDistributor(FileDistributor):

    def collect_file_inf(self):
        self.zfile = zipfile.ZipFile(self.path, 'r')
        for file in self.zfile.infolist():
            if not file.is_dir():
                self.files_list.append([file.filename, file.date_time[0], file.date_time[1]])

    def copy_files(self, destination, list):
        for file in list:
            dest = os.path.join(destination, file.split('/')[-1])
            with self.zfile.open(file, 'r') as source, open(dest, 'wb') as target:
                shutil.copyfileobj(source, target)


if FILE_SOURCE.endswith('.zip'):
    distibute_files = FileZipDistributor(path=FILE_SOURCE)
else:
    distibute_files = FileDistributor(path=FILE_SOURCE)

distibute_files.execute()
