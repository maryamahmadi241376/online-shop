import csv
import hashlib
from store_manager import Manager
from customer import Customer
import logging
import re
import json

name = "Manager"
logger = logging.getLogger("Manager related")
logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',
                    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s' \n",
                    datefmt='%d-%b-%y %H:%M:%S')

regex = r"^09\d{9}"

try:
    print("1.Register\n2.Enter")  # user chooses to register or enter
    n = int(input("please choose: "))
    if n == 1:
        try:
            print("1.Manager\n2.customer")  # user chooses to be the manager or the customer
            m = int(input("please choose: "))
            if m == 1:  # manager registers
                username = input("enter your phone number as username: ")
                password = input("enter password: ")
                confirm_password = input("confirm password: ")
                shop_name = input("enter shop name: ")
                start_work_period = int(input("enter starting hour of work period: "))
                end_work_period = int(input("enter ending hour of work period: "))
                matches = re.finditer(regex, username, re.MULTILINE)
                try:
                    for matchNum, match in enumerate(matches, start=1):
                        if confirm_password == password and username == match.group():
                            Password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                            with open('UserInfo.csv', 'r') as info:
                                reader = csv.DictReader(info)
                                for row in reader:
                                    if username in row.values():
                                        raise Exception("username is already taken!")
                            with open('UserInfo.csv', 'a') as user_info:  # a file that contains
                                # manager information
                                columns = ["username", "password", "roll", "shop name", "start work period",
                                           "end work period"]
                                managers = [{'username': username, 'password': Password, 'roll': 'manager',
                                             'shop name': shop_name,
                                             'start work period': start_work_period,
                                             'end work period': end_work_period}]
                                writer = csv.DictWriter(user_info, fieldnames=columns)
                                if user_info.tell() == 0:
                                    writer.writeheader()
                                writer.writerows(managers)
                            with open('ShopList.json', 'r+') as fp:  # a file that contains manaegers shop details
                                try:
                                    data = json.load(fp)
                                except:
                                    data = []
                                if not isinstance(data, list):
                                    data = []

                                data.append(
                                    {
                                        'username': username,
                                        'product list': Manager.shopping,
                                        'shop name': shop_name,
                                        'start work period': start_work_period,
                                        'end work period': end_work_period,
                                        'block list': []
                                    }
                                )
                                with open('ShopList.json', 'w+') as fp:
                                    json.dump(data, fp, indent=2)
                                    logging.info(f"new shop is added successfully : {shop_name}")
                        else:
                            print("password or username not confirmed!")
                            logging.error("password not confirmed!")
                except Exception as e:
                    print(f"{e},password not confirmed!")
            elif m == 2:  # customers registers
                username = input("enter your phone number as username: ")
                password = input("enter password: ")
                confirm_password = input("confirm password: ")
                matches = re.finditer(regex, username, re.MULTILINE)
                try:
                    for matchNum, match in enumerate(matches, start=1):
                        if password == confirm_password and username == match.group():
                            Password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                            with open('UserInfo.csv', 'r') as info:
                                reader = csv.DictReader(info)
                                for row in reader:
                                    if username in row.values():
                                        raise Exception("username is already taken!")
                            with open('UserInfo.csv', 'a') as user_info:  # a file that contains customers information
                                columns = ["username", "password", "roll", "shop name", "start work period",
                                           "end work period"]
                                customers = [
                                    {'username': username, 'password': Password, 'roll': 'customer',
                                     'shop name': 'None',
                                     'start work period': 'None', 'end work period': 'None'}]
                                writer = csv.DictWriter(user_info, fieldnames=columns)
                                if user_info.tell() == 0:
                                    writer.writeheader()
                                writer.writerows(customers)

                except Exception as e:
                    logging.error("password or username not confirmed!")
                    print(f"{e}, password or username not confirmed!")

        except Exception as e:
            print(f"{e} has occurred,wrong option")
            logging.error("wrong option")

    elif n == 2:
        print("1.Manager\n2.customer")  # user chooses to enter as a manager or customer
        m = int(input("please choose: "))
        if m == 1:
            try:
                # def enter_manager():  # manager logs in
                user = input("enter your username: ")
                pass_word = input("enter your password: ")
                hash_password = hashlib.sha256(pass_word.encode('utf-8')).hexdigest()
                with open("UserInfo.csv", "r") as manager_info:
                    read = csv.DictReader(manager_info)
                    list_user = list(read)
                    for dic in list_user:
                        if dic['password'] == hash_password and dic['username'] == user:
                            if dic["roll"] == "manager":
                                user = dic["username"]
                                name_shop = dic["shop name"]
                                start_work = dic["start work period"]
                                end_work = dic["end work period"]
                                # print(user, name_shop, start_work, end_work)
                                store_manager = Manager.enter_manager(user, name_shop, start_work, end_work)
                                logging.info('you entered successfully!')
                                print(store_manager.warning())

                                print("=====================")


                                def adminLoginWindow():
                                    return "1.Add Product\n2.Products goods available\n3.List of products\n4.Customer " \
                                           "Invoices\n5.Customer List\n6.Block Customer\n7.Logout "


                                a = adminLoginWindow()
                                print(a)
                                print("=====================")
                                choice = 9
                                while choice != 8:
                                    choice = int(input("select a number: "))
                                    if choice == 1:
                                        print(store_manager.add_product())
                                    elif choice == 2:
                                        print(store_manager.available_products())
                                        print(store_manager.warning())
                                    elif choice == 3:
                                        print(store_manager.warning())
                                    elif choice == 4:  # this option is not available at this moment
                                        print(store_manager.customer_invoice())
                                    elif choice == 5:
                                        print(store_manager.customer_info())
                                    elif choice == 6:
                                        chosen_username = input("dear manager, please choose customers username: ")
                                        print(store_manager.block_customer(chosen_username))
                                    elif choice == 7:
                                        print("You logged out to the main Menu now.")
                                        print(a)
                                    else:
                                        logging.warning("No such option available")
                                        a = adminLoginWindow()
                                        print(a)
                                        raise Exception("No such option available,please choose a valid option")

                            else:
                                logging.error("log in unsuccessful!")
                                raise Exception("log in unsuccessful!")
            except Exception as e:
                print(e)

        elif m == 2:  # customer logs in
            try:
                user = input("enter your username: ")
                pass_word = input("enter your password: ")
                hash_password = hashlib.sha256(pass_word.encode('utf-8')).hexdigest()
                with open("UserInfo.csv", "r") as customer_info:
                    read = csv.DictReader(customer_info)
                    list_user = list(read)
                    for dic in list_user:
                        if list_user:
                            if dic['password'] == hash_password and dic['username'] == user:
                                if dic["roll"] == "customer":
                                    user = dic["username"]
                                    store_customer = Customer(user, pass_word)
                                    logging.info('you entered successfully!')
                                    print("=====================")


                                    def adminLoginWindow():
                                        return "1.See your previous invoices\n2.See the list of shops\n3.See the list " \
                                               "of shops\n4.Search for a shop\n5.Choose a shop\n6.See the list of " \
                                               "products\n7.Choose products\n8.See pre_invoice\n9.Confirm or change " \
                                               "purchase list\n10.Logout "


                                    a = adminLoginWindow()
                                    print(a)
                                    print("=====================")
                                    choice = 11
                                    while choice != 11:
                                        choice = int(input("select your option"))
                                        if choice == 1:
                                            pass
                                        if choice == 2:
                                            pass
                                        if choice == 3:
                                            pass
                                        if choice == 4:
                                            pass
                                        if choice == 5:
                                            pass
                                        if choice == 6:
                                            pass
                                        if choice == 7:
                                            pass
                                        if choice == 8:
                                            pass
                                        if choice == 9:
                                            pass
                                        if choice == 10:
                                            pass
                            else:
                                logging.error("log in unsuccessful!")
                                raise Exception("log in unsuccessful!")
            except Exception as e:
                print(e)
                logging.error("invalid input")
except Exception as e:
    print(e)
    logging.error("invalid input")
