# TODO: 
# - UPDATE: While key is not pressed in watcher()
# - FIX: Unintended behaviour where second check always triggers if first check was triggered
# - FIX: Unable to remove dirs in cleanup()

if __name__ == '__main__':
    print("Run the main.py file instead of this one.")
    exit(1)

from shutil import rmtree
from atexit import register
from time import sleep
import os
import xxhash
import raid


global root_dir
global backend_dir
root_dir = os.path.abspath(os.path.dirname(__file__))
backend_dir = os.path.join(root_dir, "backend")


def create_drives(n):
    for i in range(n):
        target = f"DRIVE-{i + 1}"
        try:
            drive_path = os.path.join(backend_dir, target)
            os.makedirs(drive_path)
        except OSError as e:
            print(e)
            exit(1)
    return True


def cleanup():
    rmtree(backend_dir)
    return True


# Run cleanup() when ctrl+c is pressed or exit(0) is run.
# Same as: atexit.register(cleanup)
register(cleanup)

# 64KB buffer is used for reading large files, so we don't consume all the ram.
BUFFER_SIZE = 65536


def update_backend(raid_level, raid_info, disks_used, file_names_list):
    # Regardless of wether a file or a file name was changed,
    # operations has to be the same.
    # So, if a file was changed, it will be copied to the backend,
    # and striped, duplicated or whatever the process for the given
    # raid level is.
    # Read contents of every file in frontend in chunks of BUFFER_SIZE bytes.

    raid_function = getattr(raid, raid_info[raid_level]["function_name"])
    raid_function(file_names_list, disks_used)

    return True


def get_list_hash(l):
    return xxhash.xxh128(bytes(", ".join(l), "utf-8")).hexdigest()


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
    # Ternary operator
    return True if x == y else False


def watcher(rl, ri, du, fs_hash=None, file_hashes_list=[]):

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

        # First index of entries is a list of files, second is a list of dirs.
        entries_divided = recurse_path("./frontend")
        entries_merged = entries_divided[0] + entries_divided[1]
        prev_fs_hash = fs_hash

        fs_hash = get_list_hash(entries_merged)

        if fs_hash != prev_fs_hash:
            update_backend(rl, ri, du, entries_divided[0])
        else:
            # Create a "backup" of the current version of the list.
            # Doing list1 = list2, and then changing the value of list2
            # afterwards would change it in list1 as well, this is a
            # workaround.
            prev_file_hashes_list = file_hashes_list[:]
            file_hashes_list = []
            for entry in entries_divided[0]:
                file_hashes_list.append(get_file_hash(entry))

            if not compare_lists(file_hashes_list, prev_file_hashes_list):
                update_backend(rl, ri, du, entries_divided[0])
        sleep(5)