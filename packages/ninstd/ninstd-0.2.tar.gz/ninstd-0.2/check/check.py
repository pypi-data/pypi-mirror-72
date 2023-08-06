#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Collections of functions for asserting or checking.
Note that if the module is related to check, the priority is to put at here.
"""
import os
import sys
import shutil

__all__ = [
    'is_imported', 
    'is_dir', 
    'is_exist', 
    'check_file_type',
    ]


def is_imported(module: str) -> bool:
    """Check the module is load or not.
    From: https://stackoverflow.com/questions/30483246/how-to-check-if-a-python-module-has-been-imported
    """
    if module in sys.modules:
        return True
    else:
        return False

def is_dir(directory: str) -> bool:
    """Return True if that directory is dir. 
    """
    return os.path.isdir(os.path.join(os.getcwd(), directory))


def is_exist(directory: str) -> bool:
    """Return True if that directory is dir. 
    """
    return os.path.exists(os.path.join(os.getcwd(), directory))


def check_type_args(*args: str, type: str) -> bool:
    """Assert that all args has same type as type.
    """
    for arg in args:
        assert isinstance(arg, type)
    

def check_file_type(directory: str, suffix: str) -> None:
    """Split a file type from directory and check that is same as file_type or not.
    """
    assert isinstance(directory, str)
    return suffix == directory.split('.')[-1]

