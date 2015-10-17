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

ARCHIVE_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "myArchive")
OBJECTS_DIR = os.path.join(ARCHIVE_PATH,"objects")
INDEX_FILE = os.path.join(ARCHIVE_PATH,"index.pkl")


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
        if not os.path.exists(ARCHIVE_PATH):
            os.makedirs(ARCHIVE_PATH)
            created = True

        # assert the objects folder within myArchive exists
        if not os.path.exists(OBJECTS_DIR):
            os.makedirs(OBJECTS_DIR)
            created = True

        # assert the index dictionary within myArchive exists
        if not os.path.exists(INDEX_FILE):
            _save_index({})
            created = True

        # report on the status of the initialisation
        print("myArchive", "successfully initialised" if created else "already exists", "at '" + ARCHIVE_PATH + "'")

    except OSError:
        print("Unable to initialise myArchive at", ARCHIVE_PATH, "!")
        sys.exit(1)
    return


def store():
    if len(sys.argv) > 3:
        raise ValueError("Too many arguments: store() takes exactly 1 argument.")

    # check that the supplied directory name is actually a valid directory
    if not os.path.exists(sys.argv[2]) or not os.path.isdir(sys.argv[2]):
        raise ValueError("'" + sys.argv[2] + "' is not a valid directory!")

    # double check archive is initialised
    _check_initialised()

    # load the existing index file from disk
    index = _load_index()

    # recursively backup each file in the named directory into archive's objects folder
    already_in_archive_count = 0
    for dir_path, _, file_names in os.walk(sys.argv[2]):

        # first get the current relative subdirectory
        relative_subdir = ""
        for each_subdir in dir_path.split(os.sep)[len(sys.argv[2].split(os.sep))-1:]:
            relative_subdir = os.path.join(relative_subdir, each_subdir)

        # now store each file in the current subdirectory
        for file_name in file_names:
            current_file = os.path.join(dir_path, file_name)
            index_filename = os.path.join(relative_subdir, file_name)

            # generate the hash object name
            sig = create_file_signature(current_file)
            if sig is None:
                print("unable to access file: '" + current_file + "' !")
                continue
            _, _, hash_sig = sig

            # check that a different file with the same name is not already in the archive
            # if it's the same file with same name, then re-adding it can fix inconsistencies found with test()
            if index_filename in index.keys() and index[index_filename] != hash_sig:
                already_in_archive_count += 1
                continue

            # copy and rename the file into the archive
            try:
                shutil.copyfile(current_file, os.path.join(OBJECTS_DIR, hash_sig))
            except IOError:
                print("Failed to add file to archive: '" + index_filename + "'")
                continue

            # store the filename and hash in the index
            index[index_filename] = hash_sig
            print("Successfully added file to archive: '" + index_filename + "'")

    # update the archive index on disk
    _save_index(index)

    if already_in_archive_count:
        print("duplicate-named different-content files found in archive and not added:", already_in_archive_count, "!")
    else:
        print("No duplicate-named different-content files found, all files added to archive")
    return


def list_():
    if len(sys.argv) > 3:
        raise ValueError("Too many arguments: list() takes either 0 or 1 arguments.")

    # double check archive is initialised
    _check_initialised()

    # load the existing index from disk
    index = _load_index()

    # check the archive is not empty
    if not len(index.keys()):
        print("Archive is empty")
        return

    # find files matching <pattern>
    count = 0
    pattern = sys.argv[2] if len(sys.argv) == 3 else ""
    for file_name in index.keys():
        if pattern in file_name:
            print(str(count+1).ljust(4), file_name)
            count += 1
    if not count:
        print("No files found matching '" + pattern + "'")
    return


def test():
    if len(sys.argv) > 2:
        raise ValueError("Too many arguments: test() takes exactly 0 arguments.")

    # double check the archive is initialised
    _check_initialised()

    # load the index file from disk
    index = _load_index()

    # check the consistency of the index and objects
    bad_files, bad_hashes, consistent_count = [], [], 0
    for file_name, hash_name in index.items():

        # check that a hash object matches the filename
        hash_path = os.path.join(OBJECTS_DIR, hash_name)
        if not os.path.exists(hash_path):
            bad_files.append(file_name)
            continue

        # check that the hash object is consistent
        sig = create_file_signature(hash_path)
        if sig is None:
            bad_hashes.append(hash_name)
            continue
        _, _, hash_sig = sig
        if hash_sig != hash_name:
            bad_hashes.append(hash_name)
            continue

        # update the consistent items count
        consistent_count += 1

    # print the report of consistency test findings
    count = 1
    print("issue(s) found:", len(bad_files) + len(bad_hashes))
    for bad_file in bad_files:
        print(str(count).ljust(4), "expected file not found in archive:", bad_file)
        count += 1
    for bad_hash in bad_hashes:
        print(str(count).ljust(4),"archived file inconsistent or inaccessible:", bad_hash)
        count += 1
    print("total number of consistent files:", consistent_count, "out of expected", len(index))
    return


def get():
    # TODO: Implement get command
    pass


def restore():
    # TODO: Implement restore command
    pass


def _check_initialised():
    if not os.path.exists(ARCHIVE_PATH) or not os.path.exists(OBJECTS_DIR) or not os.path.exists(INDEX_FILE):
        raise RuntimeError("myArchive not initialised @'" + ARCHIVE_PATH + "' !")


def _save_index(index_dict):
    try:
        with open(INDEX_FILE, 'wb') as handle:
            pickle.dump(index_dict, handle)
    except IOError:
        print("Error saving index file!")
        sys.exit(1)
    return


def _load_index():
    try:
        with open(INDEX_FILE, 'rb') as handle:
            index_dict = pickle.load(handle)
    except IOError:
        print("Error loading index file!")
        sys.exit(1)
    return index_dict


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
