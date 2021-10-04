import csv
import hashlib
from store_manager import Manager
from customer import Customer, Purchase
from person import Person
import logging
import re
import json
from datetime import time

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
                start_work_period = str(time(int(input("starting hour: ")), (int(input("starting min: ")))))
                end_work_period = str(time(int(input("starting hour: ")), (int(input("starting min: ")))))
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
                # manager logs in
                user = input("enter your username: ")
                pass_word = input("enter your password: ")
                if Person.log_in(user, pass_word) == "manager":
                    store_manager = Manager.enter_manager(user, pass_word)
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
                    raise Exception("you are not a manager")
            except Exception as e:
                print(e)

        elif m == 2:  # customer logs in
            try:
                user = input("enter your username: ")
                pass_word = input("enter your password: ")
                if Person.log_in(user, pass_word) == "customer":
                    store_customer = Customer(user, pass_word)
                    buy = Purchase(user)
                    print("=====================")

                    def adminLoginWindow():
                        return "1.See your previous invoices\n2.See the list of active shops\n" \
                               "\n3.Search for a shop and start shopping\n4.Choose a shop and start shopping\n5.See " \
                               "the menu\n6.Logout"

                    a = adminLoginWindow()
                    print(a)
                    print("=====================")
                    choice = 7
                    while choice != 6:
                        choice = int(input("select your option"))
                        if choice == 1:
                            print(store_customer.see_invoices())
                        if choice == 2:
                            print(buy.active_shops())
                        if choice == 3:
                            user_shop = input("enter the name of the shop you wanna search: ").lower().strip()
                            print(buy.search_shop(user_shop))
                        if choice == 4:
                            user_selection = input("enter the name of the shop you chose: ").lower().strip()
                            print(buy.choose_shop(user_selection))
                            if buy.choose_shop(user_selection) == user_selection:
                                print(buy.list_of_products(user_selection))
                                choose = int(input("1.choose products and shop\n2.search products\n3.exit: "))
                                if choose == 1:
                                    print(buy.choose_products())
                                    buy_customer = Purchase(user, user_selection)
                                    print(buy_customer.choose_products())
                                    print(buy_customer.invoices(Purchase.purchase_list))
                                elif choose == 2:
                                    product = input("enter the name of product you wanna search: ")
                                    buy_customer = Purchase(user, user_selection)
                                    print(buy_customer.search_products(product, user_selection))
                                    print(buy_customer.invoices(Purchase.purchase_list))
                                else:
                                    break
                            else:
                                break
                        if choice == 5:
                            a = adminLoginWindow()
                            print(a)
                        if choice == 6:
                            break
                else:
                    raise Exception("you are not a customer")
            except Exception as e:
                print(e)
                logging.error("invalid input")
except Exception as e:
    print(e)
    logging.error("invalid input")
