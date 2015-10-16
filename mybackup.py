"""
Program to backup and restore directories without storing duplicates twice
Specifications as per 159.251 Software Engineering Design and Construction Assignment 2, Semester 2 2015
"""

import sys
import os
import os.path
import pickle

import logger
from mkfilesig import create_file_signature

__author__ = 'Sam Hunt'


def help_():
    print("myBackup supported commands:\n")
    print("init")
    print("\tInitialise an archive directory at '~/Desktop/myArchive'")
    print("\tIdempotent if archive already exists at location\n")
    return


def init():
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments: init() takes either 0 arguments.")

    try:
        # to store whether initialisation was required
        created = False

        # assert the myArchive folder exists
        archive_path = os.path.join(os.path.expanduser("~"), "Desktop", "myArchive")
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)
            created = True

        # assert the objects folder within myArchive exists
        objects_dir = os.path.join(archive_path,"objects")
        if not os.path.exists(objects_dir):
            os.makedirs(objects_dir)
            created = True

        # assert the index dictionary within myArchive exists
        index_file = os.path.join(archive_path,"index.pkl")
        if not os.path.exists(index_file):
            with open(index_file, 'wb') as handle:
                pickle.dump({}, handle)
            created = True

        # report on the status of the initialisation
        print("myArchive", "successfully initialised" if created else "already exists", "at '" + archive_path + "'")

    except OSError:
        print("Unable to initialise myArchive at", archive_path, "!")
        sys.exit(1)
    return


def store():
    pass


def list_():
    pass


def test():
    pass


def get():
    pass


def restore():
    pass


if __name__ == '__main__':

    # the command entered by the user
    command = hash(sys.argv[1].strip().lower())

    # all commands supported by the program
    commands = {hash('init'): init,
                hash('store'): store,
                hash('list'): list_,
                hash('test'): test,
                hash('get'): get,
                hash('restore'): restore,
                hash('help'): help_}

    # ensure the user has entered a supported command
    if command not in commands.keys():
        raise ValueError("command must be one of 'help', 'init', 'store', 'list', 'test', 'get', 'restore'")

    # switch on command
    commands[command]()

    # return execution to os
    sys.exit(0)
