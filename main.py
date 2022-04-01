#!/usr/bin/env python3

# This file is used to get user input, and call controller with input parameters

import controller
import math


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
        "0": {"min_disks": 2, "function_name": "r0"},
        "1": {"min_disks": 2, "function_name": "r1"},
        "2": {"min_disks": 3, "function_name": "r2"},
        "3": {"min_disks": 3, "function_name": "r3"},
        "4": {"min_disks": 3, "function_name": "r4"},
        "5": {"min_disks": 3, "function_name": "r5"},
        "6": {"min_disks": 4, "function_name": "r6"},
        "01": {"min_disks": 4, "function_name": "r01"},
        "03": {"min_disks": 6, "function_name": "r03"},
        "10": {"min_disks": 4, "function_name": "r10"},
        "50": {"min_disks": 9, "function_name": "r50"},
        "60": {"min_disks": 8, "function_name": "r60"},
        "100": {"min_disks": 8, "function_name": "r100"}
    }

    raid_level = -1
    while raid_level not in raid_info:
        raid_level = input(f"\nWhat RAID level should be used?\n")

    drives_used = -1
    while drives_used < raid_info[raid_level]["min_disks"]:
        drives_used = int(input(f"\nHow many drives do you want to use? (min: {raid_info[raid_level]['min_disks']})\n"))

    controller.create_drives(drives_used)
    controller.watcher(raid_level, raid_info, drives_used)

    exit(0)