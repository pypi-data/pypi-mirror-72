#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collection of modules related to path, dir and files.
"""
import os
import shutil
from ..check import is_dir, is_exist, check_file_type

__all__ = ['del_dir_or_file', 'not_dir_mkdir']


def del_dir_or_file(dir_or_file: str) -> None:
    """
    """
    assert isinstance(dir_or_file, str)
    if is_dir(dir_or_file):
        shutil.rmtree(dir_or_file)
    if is_exist(dir_or_file):
        os.remove(dir_or_file)


def not_dir_mkdir(directory: str) -> None:
    """
    """
    assert isinstance(directory, str)
    if not is_dir(directory):
        os.mkdir(os.path.join(os.getcwd(), directory))


def not_type_append_type(directory: str, suffix: str) -> str:
    """
    """
    assert isinstance(directory, str)
    assert isinstance(suffix, str)
    if not check_file_type(directory, suffix):
        splited = directory.split('.')
        assert len(splited) == 1 or len(splited) == 2, 'Not work when directory contains `.` more than one.'
        prefix = splited[0]
        path = os.path.join(prefix, suffix)
    else:
        path = directory
    return path
    


    
    
 