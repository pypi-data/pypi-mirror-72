# coding:utf-8
from src.browser import Browser
from src.utils.color import Color
from src.utils.calc import Calc


class AttendanceManager(object):

    def __init__(self):
        self.browser = Browser()
        self.driver = self.browser.driver

    def stamp(self, method):
        if self.login() and method in dir(self):
            getattr(self, method)()
            self.exit()

    def login(self):
        return self.browser.login()

    def clock_execute(self, selector, time_prefix):
        if self.driver.current_url != self.browser.MYPAGE_URL:
            print("Please login.")

        self.driver.find_element_by_class_name(selector).click()
        print(time_prefix + Calc.current_time())

    def start(self):
        selector = "attendance-card-time-stamp-clock-in"
        prefix = "Work " + Color.get_colored(Color.BOLD, "START") + " time: "
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "DAKOKU successful. Good luck!")

    def end(self):
        selector = "attendance-card-time-stamp-clock-out"
        prefix = "Work " + Color.get_colored(Color.BOLD, "END") + " time: "
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "DAKOKU successful. Good job today!")

    def start_break(self):
        selector = "attendance-card-time-stamp-start-break"
        prefix = "Break " + Color.get_colored(Color.BOLD, "START") + " time: "
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "DAKOKU successful. Let's take a break.")

    def end_break(self):
        selector = "attendance-card-time-stamp-end-break"
        prefix = "Break " + Color.get_colored(Color.BOLD, "END") + " time: "
        self.clock_execute(selector, prefix)

        Color.print(Color.GREEN, "DAKOKU successful. Let's get back to work.")

    def exit(self):
        self.driver.close()
