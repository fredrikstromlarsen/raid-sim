#!/usr/bin/env python3

import controller
import math
from time import sleep


class RaidInfo:
    def __init__(self, rl, du, ds, sdp, nb):
        self.raid_level = rl
        self.drives_used = du
        self.drive_size = ds
        self.single_drive_performance = sdp
        self.number_of_backups = nb

    def raid_0(self):
        usable_space = self.drives_used * self.drive_size
        ok_number_of_corrupted_drives = 0
        read_performance = self.drives_used * self.single_drive_performance
        write_performance = self.drives_used * self.single_drive_performance

        return {
            "usable_space": usable_space,
            "ok_number_of_corrupted_drives": ok_number_of_corrupted_drives,
            "read_performance": read_performance,
            "write_performance": write_performance
        }

    def raid_1(self):
        usable_space = 1 / self.number_of_backups * self.drives_used
        ok_number_of_corrupted_drives = self.number_of_backups
        read_performance = self.number_of_backups * self.single_drive_performance
        write_performance = self.single_drive_performance

        return {
            "usable_space": usable_space,
            "ok_number_of_corrupted_drives": ok_number_of_corrupted_drives,
            "read_performance": read_performance,
            "write_performance": write_performance
        }

    def raid_2(self):
        usable_space = (1 - (1 / self.drives_used) * math.log2(self.drives_used + 1)) * (
                    self.drives_used * self.drive_size)
        ok_number_of_corrupted_drives = 1
        read_performance = "Wikipedia says \"depends\""
        write_performance = "Wikipedia says \"depends\""

        return {
            "usable_space": usable_space,
            "ok_number_of_corrupted_drives": ok_number_of_corrupted_drives,
            "read_performance": read_performance,
            "write_performance": write_performance
        }


if __name__ == '__main__':
    raid_info = {
        "0": 2,
        "1": 2,
        "2": 3,
        "3": 3,
        "4": 3,
        "5": 3,
        "6": 4,
        "01": 4,
        "03": 6,
        "10": 4,
        "50": 9,
        "60": 8,
        "100": 8
    }

    raid_level = -1
    while raid_level not in raid_info:
        raid_level = input(f"\nWhat RAID level should be used?\n")

    drives_used = -1
    while drives_used < raid_info[raid_level]:
        drives_used = int(input(f"\nHow many drives do you want to use? (min: {raid_info[raid_level]})\n"))

    controller.create_drives(drives_used)
    controller.start_watcher()

    sleep(2)

    controller.cleanup()

    exit(0)