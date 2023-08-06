# coding:utf-8
import os
import pickle
import getpass
import keyring


class UserInfoManager(object):
    CORP_ID = 'CORP_ID'
    USER_ID = 'USER_ID'
    USER_PASS = 'USER_PASS'
    MF_SERVICE = 'MF_SERVICE'
    USER_INFO_PATH = os.environ['HOME'] + '/.local/share/dakoker'

    def get(self):
        user_info = self.get_cached()
        if not user_info:
            print("Please enter your login info.")
            user_info = {}
            user_info[self.CORP_ID] = input("company ID: ")
            user_info[self.USER_ID] = input("user ID or email address: ")
            user_info[self.USER_PASS] = getpass.getpass("password: ")

        return user_info

    def get_cached(self):
        if os.path.isfile(self.USER_INFO_PATH + '/user_info.pkl'):
            with open(self.USER_INFO_PATH + '/user_info.pkl', "rb") as f:
                info = pickle.load(f)
                passwd = keyring.get_password(
                    self.MF_SERVICE, info[self.USER_ID])
                if passwd:
                    info[self.USER_PASS] = passwd
                    return info

        return None

    def remove(self):
        if os.path.isfile(self.USER_INFO_PATH + '/user_info.pkl'):
            os.remove(self.USER_INFO_PATH + "/user_info.pkl")

    def save(self, user_info):
        if not os.path.isdir(self.USER_INFO_PATH):
            os.makedirs(self.USER_INFO_PATH)

        keyring.set_password(
            self.MF_SERVICE,
            user_info[self.USER_ID],
            user_info[self.USER_PASS])

        del user_info[self.USER_PASS]
        pickle.dump(user_info,
                    open(self.USER_INFO_PATH + "/user_info.pkl", "wb"))
