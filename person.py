import csv
import hashlib
import logging


class Person:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def log_in(username, password):
        try:
            hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            with open("UserInfo.csv", "r") as manager_info:
                read = csv.DictReader(manager_info)
                list_user = list(read)
                for dic in list_user:
                    if dic['password'] == hash_password and dic['username'] == username:
                        if dic["roll"] == "manager":
                            username = dic["username"]
                            name_shop = dic["shop name"]
                            start_work = dic["start work period"]
                            end_work = dic["end work period"]
                            logging.info('you entered successfully!')
                            return "manager"
                        elif dic["roll"] == "customer":
                            logging.info('you are not registered as manager')
                            return "customer"
        except Exception as e:
            logging.error("you are not registered")
            print(e)
