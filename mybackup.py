"""
Program to backup and restore directories without storing duplicates twice
Specifications as per 159.251 Software Engineering Design and Construction Assignment 2, Semester 2 2015
"""

import sys

from mkfilesig import create_file_signature

__author__ = 'Sam Hunt'

if __name__ == '__main__':

    if sys.argv[1] not in ['init', 'store', 'list', 'test', 'get', 'restore']:
        raise ValueError("command must be one of 'init', 'store', 'list', 'test', 'get', 'restore'")
        sys.exit(1)
