# coding:utf-8
import fire
from halo import Halo

from src.user_info_manager import UserInfoManager
from src.attendance_manager import AttendanceManager


class Dakoker(object):

    def __init__(self):
        self.manager = AttendanceManager()

    def start(self):
        if self.manager.login():
            self.manager.clock_in()
            self.manager.exit()

    def stop(self):
        if self.manager.login():
            self.manager.clock_out()
            self.manager.exit()

    def remove_data(self):
        spinner = Halo(text='Remove your local data...', spinner='dots')
        removed = UserInfoManager().remove()
        if removed:
            spinner.succeed("Data Successfully deleted.")
        else:
            spinner.warn("Data not found.")


def main():
    fire.Fire(Dakoker)
