# TODO: UPDATE: While key is not pressed in watcher()
# TODO: FIX: Unintended behaviour where second check always triggers if first check was triggered

if __name__ == '__main__':
    print("Run the main.py file instead of this one.")
    exit(1)

from time import sleep
import os
from pprint import pprint
import xxhash


def create_drives(n):
    parent_dir = "./backend"

    for i in range(n):
        target = f"DRIVE-{i + 1}"

        try:
            path = os.path.join(parent_dir, target)
            os.makedirs(path)

        except OSError as e:
            print(e)
            exit(1)

    return True


def cleanup():
    parent_dir = "./backend"
    try:
        os.rmdir(parent_dir)
    except OSError as e:
        print(e)
        exit(1)
    return True


def update_backend(x, y):
    # TEMPORARY
    print(f"filesystem_hash: {x}\n"
        f"one_hash_to_rule_them_all: {y}\n")
    return True


def hash_the_list(l):
    # As long as the check doesn't change,it's sufficient.
    return xxhash.xxh128(bytes(", ".join(l), "utf-8")).hexdigest()


# 64KB buffer will be used for reading large files so we don't consume all the ram.
BUFFER_SIZE = 65536


def get_file_hash(x):
    with open(x, 'rb') as f:
        file_hash = xxhash.xxh128()
        while True:
            data = f.read(BUFFER_SIZE)
            if not data:
                break

            # Add 64KB chunks to hash function
            file_hash.update(data)
    return file_hash.hexdigest()


def recurse_path(path):
    file_entries = []
    dir_entries = []

    for root, dirs, files in os.walk(path, topdown=True, followlinks=False):
        for name in files:
            file_entries.append(os.path.join(root, name))
        for name in dirs:
            dir_entries.append(os.path.join(root, name))

    return [file_entries, dir_entries]


def compare_lists(x, y):
    if len(x) != len(y):
        return False
    elif x == y:
        return True
    else:
        return False


def watcher(fs_hash=None, file_hashes_list=[]):
    while True:
        # Check first if the file structure has been changed
        # by returning a list of all the files/dirs and
        # hashing + comparing the new hash, against the old one.

        # Then, if it is the same, check the file contents by
        # hashing every file, saving the checksum to a list,
        # and lastly comparing the hash value of the new list
        # the with previous list.

        # This is so that I don't have to think about the files.
        # Otherwise, it would be like reinventing the "diff" command.

        entries = recurse_path("./frontend")
        prev_fs_hash = fs_hash
        fs_hash = hash_the_list(entries[0] + entries[1])

        if fs_hash != prev_fs_hash:
            update_backend("Filesystem changed", "Files too, of course")
        else:
            prev_file_hashes_list = file_hashes_list[:]
            file_hashes_list = []
            for entry in entries[0]:
                file_hashes_list.append(get_file_hash(entry))

            if not compare_lists(file_hashes_list, prev_file_hashes_list):
                update_backend("Filesystem not changed", "Files changed")
        sleep(5)
    cleanup()
    return True