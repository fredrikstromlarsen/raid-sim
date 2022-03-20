if __name__ == '__main__':
    print("Run the main.py file instead of this one.")
    exit(1)

from time import sleep
import os


def create_drives(n):
    parent_dir = "./backend"

    for i in range(n):
        target = f"DRIVE-{i+1}"

        try:
            path = os.path.join(parent_dir, target)
            os.makedirs(path)

        except OSError as e:
            print(e)
            exit(1)

    return True


def start_watcher():
    while True:
        sleep(2)
        break
    return True


def cleanup():
    parent_dir = "./backend"
    try:
        for element in os.listdir(parent_dir):
            path = os.path.join(parent_dir, element)
            os.rmdir(path)
    except OSError as e:
        print(e)
        exit(1)

    return True