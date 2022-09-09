import os

import requests
import json
from http.cookies import SimpleCookie

URL = "https://hrd.shanghaitech.edu.cn"
TIMEOUT = 10.00


class AutoHrd:
    def __init__(self):
        self.json_data = None
        self.session_id = None

    def login(self):
        login_url = URL + "/ldapLogin"
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Cookie": "JSESSIONID = 7CAEACCA8C0958911F6180C3CDF8B123",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        body = {"j_password": os.environ['HRD_PASSWORD'], "studentNum": os.environ['HRD_USER']}
        r = requests.post(login_url, json=body, headers=headers, timeout=TIMEOUT)

        if r.text != "\"success\"":
            return
        self.session_id = r.headers.get("Set-Cookie").split(';', maxsplit=1)[0].split("=", maxsplit=1)[1]

    def get_info(self):
        info_url = URL + "/findInfoByid"
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Cookie": "JSESSIONID = " + self.session_id,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        r = requests.post(info_url, headers=headers, timeout=TIMEOUT)
        self.json_data = r.json()

    def confirm(self):
        confirm_url = URL + "/insertDailyReport"
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "Cookie": "JSESSIONID = " + self.session_id,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        body = {"dailyreportUsername": self.json_data['infomationUser'],
                "dailyreportDepartment": self.json_data['infomationXueyuan'],
                "dailyreportUseremail": self.json_data['infomationEmail'],
                "dailyreportIdentity": self.json_data['infomationIndentity'],
                "dailyreportGrade": self.json_data['infomationNianji'],
                "dailyreportOperation": "无变化",
                "infomationtableId": self.json_data['infomationId'],

                }
        r = requests.post(confirm_url, headers=headers, json=body, timeout=TIMEOUT)
        return r.text

    def do(self):
        self.login()
        if self.session_id is None:
            print("Login failed")
            return
        self.get_info()
        result = self.confirm()
        if result == "1":
            print("Success")
        else:
            print("Something is wrong, result is " + result)


if __name__ == '__main__':
    autoHrd = AutoHrd()
    autoHrd.do()
