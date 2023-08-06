# coding:utf-8
from halo import Halo

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from src.utils.colors import Colors
from src.user_info_manager import UserInfoManager


class Browser(object):
    TIMEOUT = 3
    ROOT_URL = "https://attendance.moneyforward.com"
    LOGIN_URL = ROOT_URL + "/employee_session/new"
    MYPAGE_URL = ROOT_URL + "/my_page"
    LOGIN_SUCCEED = "Login Success."
    LOGIN_FAILED = "Login Failed."

    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(chrome_options=options)
        self.info_manager = UserInfoManager()

    def login(self):
        spinner = Halo(text='Loading login page...', spinner='dots')
        spinner.start()
        self.driver.get(self.LOGIN_URL)
        spinner.succeed("Login page loaded.")

        user_info = self.info_manager.get()
        spinner = Halo(text='Login...', spinner='dots')
        spinner.start()
        return self.login_with_user_info(user_info, spinner)

    def login_with_user_info(self, user_info, spinner):
        self.driver.find_element_by_id(
            "employee_session_form_office_account_name"
        ).send_keys(user_info[self.info_manager.CORP_ID])
        self.driver.find_element_by_id(
            "employee_session_form_account_name_or_email"
        ).send_keys(user_info[self.info_manager.USER_ID])
        self.driver.find_element_by_id(
            "employee_session_form_password"
        ).send_keys(user_info[self.info_manager.USER_PASS])

        self.driver.find_element_by_class_name(
            "attendance-before-login-card-button"
        ).click()

        return self.check_login(user_info, spinner)

    def check_login(self, user_info, spinner):
        try:
            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "attendance-card-title")
                )
            )
            self.info_manager.save(user_info)
            spinner.succeed(self.LOGIN_SUCCEED)
            return True

        except TimeoutException:
            if self.driver.find_elements(By.CLASS_NAME, "is-error") != 0:
                Colors.print(
                    Colors.RED,
                    "\nCompany ID, User ID or Password is wrong."
                )
                self.info_manager.remove()
                spinner.fail(self.LOGIN_FAILED)
                return self.login()
            else:
                Colors.print(Colors.RED, "\nLogin Timeout.")
                spinner.fail(self.LOGIN_FAILED)
                return False
