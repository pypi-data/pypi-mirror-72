#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A wrapper for zip the file.
TODO: testing Zipper.
"""
import os
import copy
import shutil
from zipfile import ZipFile
from path import not_type_append_type, not_dir_mkdir, del_dir_or_file
from check import is_exist, check_file_type

__all__ = ['Zipper']


class Zipper(object):
    def __init__(self, zip_name: str, file_loc: str = '.') -> None:
        assert isinstance(zip_name, str)
        self.file_loc = file_loc
        self.zip_name = not_type_append_type(zip_name)
        
    @classmethod
    def without_savedir(
            cls, zip_name: str, save_loc: str = '', file_loc: str = '.'):
        """Before construct, create a save_loc folder.
        """
        assert isinstance(save_loc, str)
        assert isinstance(file_loc, str)
        assert isinstance(zip_name, str)
        assert is_exist(file_loc)
        not_dir_mkdir(save_loc)
        path2zip = os.path.join(save_loc, zip_name)
        return cls(path2zip, file_loc)
    
    def zip_list(self, file_list: list) -> None:
        """Zip selected files in the file_list.
        """
        assert isinstance(file_list, list)
        with ZipFile(self.zip_name, 'w') as z:
            for file in file_list:
                path2file = os.path.join(self.file_loc, file)    
                z.write(path2file, file)

    def zip_all(self, save_py: bool = False, save_folder: bool = False) -> None:
        """Zip the all files into saveloc.
        """
        file_list = os.listdir(self.file_loc)
        file_list_tmp = copy.deepcopy(file_list)
        for i in file_list:
            if not save_py:
                if check_file_type(i, 'py'):
                    file_list_tmp.remove(i)
            if not save_folder: 
                if os.path.isdir(i):
                    file_list_tmp.remove(i)
        with ZipFile(self.zip_name, 'w') as z:
            for file in file_list_tmp:
                path2file = os.path.join(self.file_loc, file)    
                z.write(path2file, file)

    def unzip(self, dest_loc: str) -> None:
        """ Unzip the  to destloc.
        """
        assert isinstance(dest_loc, str)
        del_dir_or_file(dest_loc)
        with ZipFile(self.zip_name, 'r') as z:
            for file in z.namelist():
                z.extract(file, dest_loc)
