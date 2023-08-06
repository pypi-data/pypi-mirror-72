# coding:utf-8
import datetime
from src.browser import Browser
from src.utils.colors import Colors


class AttendanceManager(object):

    def __init__(self):
        self.browser = Browser()
        self.driver = self.browser.driver

    def login(self):
        return self.browser.login()

    def clock_in(self):
        if self.driver.current_url != self.browser.MYPAGE_URL:
            print("Please login.")

        self.driver.find_element_by_class_name(
            "attendance-card-time-stamp-clock-in"
        ).click()
        print("CLOCK " + Colors.get_colored(Colors.BOLD, "IN") + " TIME: "
              + self.current_time())
        Colors.print(Colors.GREEN, "DAKOKU successful. Good luck!")

    def clock_out(self):
        if self.driver.current_url != self.browser.MYPAGE_URL:
            print("Please login.")

        self.driver.find_element_by_class_name(
            "attendance-card-time-stamp-clock-out"
        ).click()
        print("CLOCK " + Colors.get_colored(Colors.BOLD, "OUT") + " TIME: "
              + self.current_time())
        Colors.print(Colors.GREEN, "DAKOKU successful. Good job today!")

    def current_time(self):
        return str(datetime.datetime.now()).split('.')[0]

    def exit(self):
        self.driver.close()
