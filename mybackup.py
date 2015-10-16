"""
Program to backup and restore directories without storing duplicates twice
Specifications as per 159.251 Software Engineering Design and Construction Assignment 2, Semester 2 2015
"""

import sys
import os
import os.path
import pickle
import shutil

import logger
from mkfilesig import create_file_signature

__author__ = 'Sam Hunt'


def help_():
    print("myBackup supported commands:\n")
    print("init")
    print("\tInitialise an archive directory at '~/Desktop/myArchive'")
    print("\tIdempotent if archive already exists at location\n")
    # TODO: Add help descriptions for other commands
    return


def init():
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments: init() takes exactly 0 arguments.")

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
    if len(sys.argv) > 3:
        raise ValueError("Too many arguments: store() takes exactly 1 argument.")

    # check that the supplied directory name is actually a valid directory
    if not os.path.exists(sys.argv[2]) or not os.path.isdir(sys.argv[2]):
        raise ValueError("'" + sys.argv[2] + "' is not a valid directory!")

    # double check that the archive is initialised
    archive_path = os.path.join(os.path.expanduser("~"), "Desktop", "myArchive")
    objects_dir = os.path.join(archive_path,"objects")
    index_file = os.path.join(archive_path,"index.pkl")
    if not os.path.exists(archive_path) or not os.path.exists(objects_dir) or not os.path.exists(index_file):
        raise RuntimeError("myArchive not initialised @'" + archive_path + "' !")

    # load the existing index file from disk
    with open(index_file, 'rb') as handle:
        index = pickle.load(handle)

    # recursively backup each file in the named directory into archive's objects folder
    already_in_archive_count = 0
    for dir_path, _, file_names in os.walk(sys.argv[2]):
        for file_name in file_names:
            current_file = os.path.join(dir_path, file_name)

            # check that the file is not already in the archive
            if file_name in index.keys():
                already_in_archive_count += 1
                continue

            sig = create_file_signature(current_file)
            if sig is None:
                print("unable to access file: '" + current_file + "' !")
                continue
            _, _, hash_sig = sig

            # copy and rename the file into the archive
            try:
                shutil.copyfile(current_file, os.path.join(objects_dir, hash_sig))
            except IOError:
                print("Failed to add file to archive: '" + file_name + "'")
                continue

            # store the filename and hash in the index
            index[file_name] = hash_sig
            print("Successfully added file to archive: '" + file_name + "'")

    with open(index_file, 'wb') as handle:
        pickle.dump(index, handle)

    if already_in_archive_count:
        print(already_in_archive_count, "duplicate-named files found in archive and not added!")
    else:
        print("No duplicate-named files found, all files added to archive")
    return


def list_():
    # TODO: Implement list command
    pass


def test():
    # TODO: Implement test command
    pass


def get():
    # TODO: Implement get command
    pass


def restore():
    # TODO: Implement restore command
    pass

# TODO: Check logging at correct times as per assignment specification
# TODO: Update default archive directory from '~/desktop' to '~' on release version

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
