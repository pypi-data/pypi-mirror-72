#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""
import os
import json
import logging
from .path import del_dir_or_file

__all__ = [
    'set_json_log', 
    'get_log_path',
    ]

DEF_LOG_PATH = os.path.join(os.path.dirname(__file__), 'logging.json')
DEF_INFO_PATH = 'info.log'
DEF_DEBUG_PATH = 'debug.log'


def get_log_path(env_vari: str='LOG_PATH') -> str:
    """
    """
    assert isinstance(env_vari, str)
    log_path = os.getenv(env_vari)
    if log_path is None:
        log_path = DEF_LOG_PATH
    return log_path


def set_json_log(
        json_path: str = DEF_LOG_PATH, 
        def_lvl: int = logging.INFO, 
        rm_old: bool = True) -> None:
    """Modified from: https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    Using json logging as the main logger.
    Should used in every files with: logger = logging.getLogger(__name__)
    """
    assert isinstance(rm_old, bool)
    assert isinstance(def_lvl, int)
    assert isinstance(json_path, str)
    if rm_old:
        del_dir_or_file(DEF_INFO_PATH)
        del_dir_or_file(DEF_DEBUG_PATH)
        
    if os.path.exists(json_path):
        with open(json_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        raise FileNotFoundError(
                f'Cannot find json logging file from: {json_path}')

DEF_LOG_PATH = get_log_path()