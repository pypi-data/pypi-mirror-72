#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime
try:
    from __main__ import __file__
except ImportError:
    pass

__all__ = ['Namer']


class Namer(object):
    """For create a name for hyper-parameter searching.
    namer = Namer(**{'test': 1, 'test2': 2})
    print(namer.gen_name())
    """
    def __init__(self, *args: str, **kwargs: dict) -> None:
        self.args = args
        self.kwargs = kwargs
    
    @staticmethod
    def get_foldername() -> str:
        """Return a string of folder name.
        """
        full_path = os.path.realpath(__file__)
        path, _ = os.path.split(full_path)
        _, folder_name = os.path.split(path)
        return folder_name
    
    @staticmethod
    def get_date() -> str:
        """Return a string of datetime.
        """
        return str(datetime.now().strftime('%y-%m-%d_%H-%M-%S'))

    @staticmethod
    def dot_to_dash(string) -> str:
        """From the input string, find . change into _.
        """
        assert isinstance(string, str)
        return string.replace('.', '-')

    @staticmethod
    def get_filename() -> str:
        """Return a string name of python scirpt.
        """
        return os.path.basename(__file__).replace('.py', '')
    
    def gen_name(self) -> str:
        """Generate the name.
        """
        folder = self.get_foldername()
        file = self.get_filename()
        date = self.get_date()
        name = f'{folder}_{file}_{date}'
        for kw in self.kwargs.keys():
            kw = self.dot_to_dash(kw)
            name += '_' + kw + str(self.kwargs[kw])
        for arg in self.args:
            arg = self.dot_to_dash(arg)
            name += '_' + str(arg)
        return name

    @classmethod
    def from_args(cls, args):
        """Using with parser.parse_args().
        """
        return cls(**vars(args))