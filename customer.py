import csv
import json
import logging
from person import Person
from datetime import datetime, date, time

name = "Customer"
logger = logging.getLogger("Customer related")
logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',
                    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s' \n",
                    datefmt='%d-%b-%y %H:%M:%S')


class Customer(Person):
    now = datetime.now()
    request_time = str(time(now.hour, now.minute))

    def __init__(self, username, password):
        super().__init__(username, password)
        self.password = password
        self.username = username

    def see_invoices(self):  # customers can see their invoices
        try:
            with open("CustomerInvoice.csv", 'r') as s:
                reader = csv.DictReader(s)
                lst = list(reader)
                for dic in lst:
                    if dic["username"] == self.username:
                        logging.warning("The list of customers previous invoices")
                        return f"This is your invoices list:\n{dic}"
                    else:
                        logging.error("Sorry! you have no invoices yet!")
                        return f"Sorry! you have no invoices yet!"
        except Exception as e:
            print(e)


class Purchase:  # shopping class
    purchase_list = []
    total = 0

    def __init__(self, username, shop_name=None):

        self.shop_name = shop_name
        self.username = username

    def invoices(self, purchase_list=None):  # customers invoices are being stored in a csv file
        with open('CustomerInvoice.csv', 'a') as user_invoice:
            columns = ["username", "product_name", "number_of_products", "date", "purchase_list",
                       "shop_name", "total_price"]
            invoice = [
                {
                    'username': self.username,
                    'date': date.today(),
                    'purchase_list': purchase_list,
                    'shop_name': self.shop_name,
                    'total_price': Purchase.total
                }
            ]
            writer = csv.DictWriter(user_invoice, fieldnames=columns)
            if user_invoice.tell() == 0:
                writer.writeheader()
            writer.writerows(invoice)
            logging.info("New invoice has been created!")
            return "saved!"

    @staticmethod
    def active_shops():  # customer can see active shops based on their open and close time
        with open('ShopList.json', 'r') as s:
            lst = json.load(s)
            for dic in lst:
                if dic["start work period"] < Customer.request_time < dic["end work period"]:
                    print(dic)
                    return f"These are available shops at this moment"
                else:
                    logging.warning("No shops available at this moment")
                    raise Exception("No shops available at this moment")

    def search_shop(self, user_shop):  # customer can search a shop buy their name and opening and closing time
        try:
            with open('ShopList.json', 'r') as s:
                lst = json.load(s)
                for dic in lst:
                    if dic["shop name"] == user_shop and dic["start work period"] < Customer.request_time < dic[
                        "end work period"]:
                        if self.username not in dic["block list"]:
                            return f"you can purchase from {user_shop} shop"
                        else:
                            logging.warning("you are blocked, or the shop is closed at the moment")
                            return "you are blocked, or the shop is closed at the moment"
        except Exception as q:
            print(q)

    def choose_shop(self, user_selection):  # customer can choose a shop by their name
        try:
            with open('ShopList.json', 'r') as s:
                lst = json.load(s)
                for dic in lst:
                    s = [d["block list"] for d in dic if self.username not in d["block list"]][0]
                    if dic["shop_name"] == user_selection and s:
                        if dic["start work period"] < Customer.request_time < dic["end work period"]:
                            return user_selection
                        else:
                            logging.error("either you are blocked nor chosen a shop which does not exist")
                            return f"either you are blocked nor chosen a shop which does not exist"
        except Exception as e:
            print(e)

    @staticmethod
    def list_of_products(user_selection):  # customer can see the list of products in their chosen shop
        try:
            with open('ShopList.json', 'r') as s:
                lst = json.load(s)
                for dic in lst:
                    if dic["shop_name"] == user_selection:  # or user_selection in dic["shop_name"]:
                        if len(dic['product list']) > 0:
                            if dic['product list']["available"] > 0:
                                return f"name : {dic['product list']['name']},price : {dic['product list']['price']}, " \
                                       f"brand : {dic['product list']['brand']} "
                            else:
                                logging.error("No products!")
                                return f"No products!"
        except Exception as ex:
            print(ex)

    @staticmethod
    def search_products(product, shop):  # customers can search for the product they want
        try:
            with open('ShopList.json', 'r') as f:
                lst = json.load(f)
                for dic in lst:
                    for i in dic["product list"]:
                        if product in i["product name"] and shop in dic["shop name"]:
                            print(f"{i}")
                            brand = input("what brand do you want? :")
                            if brand in i["brand"]:
                                print(f"{i}")
                                end = input("do you want to buy this good? (yes/no) :").lower()
                                if end == "yes":
                                    num = input(f' How many {product} : ')
                                    if int(i["available"]) > int(num):
                                        i["available"] = str(int(i["available"]) - int(
                                            num))
                                        Purchase.purchase_list.append({"name": product, "number": num, "brand": brand})
                                        for d in Purchase.purchase_list:
                                            if d["name"] in dic["product name"]:  # or d["name"] == dic["product name"]
                                                Purchase.total += (int(d["number"]) * dic["price"])
                                                print(
                                                    f"your purchase list:\n{Purchase.purchase_list}\ntotal price:{Purchase.total}")
                                                logging.info(f"your purchase list:\n{Purchase.purchase_list}\ntotal price:{Purchase.total}")
                                                sure = input('Are you sure? (1.yes\n2.no) ').lower()
                                                if sure == "1":
                                                    print("thanks for shopping:)")
                                                else:
                                                    exit(0)
                                else:
                                    exit(0)
                with open('ShopList.json', 'w') as training:
                    json.dump(lst, training, indent=1)
                    logging.info("new purchase!")
            return Purchase.purchase_list
        except Exception as w:
            print(w)

    @staticmethod
    def choose_products(*args):  # customers can choose the products they want
        try:
            with open('ShopList.json', 'r') as f:
                lst = json.load(f)
                for i in lst:
                    for dic in i["product list"]:
                        print(dic)
                        for productName in args:
                            if productName in dic['product name']:
                                num = int(input(f' How many {productName} : '))
                                if int(dic["available"]) > num:
                                    dic["available"] = str(int(dic["available"]) - num)  # edit ShopList.json
                                    end = input('end of purchase? (1.yes\n2.no) ').lower()  # edit ShopList.json
                                    if end == "1":
                                        Purchase.purchase_list.append({"name": productName, "number": num})
                                        for d in Purchase.purchase_list:
                                            if d["name"] in dic["product name"]:  # or d["name"] == dic["product name"]
                                                Purchase.total += (int(d["number"]) * dic["price"])
                                                print(
                                                    f"your purchase list:\n{Purchase.purchase_list}\ntotal price:{Purchase.total}")
                                                sure = input('Are you sure? (1.yes\n2.no) ').lower()
                                                if sure == "1":
                                                    print("thanks for shopping:)")
                                                else:
                                                    exit(0)
                                    else:
                                        exit(0)
                with open('ShopList.json', 'w') as training:
                    json.dump(lst, training, indent=1)
                    logging.info("new purchase!")
            return Purchase.purchase_list
        except Exception as a:
            print(a)

    # def confirm_or_edit(self):
    #     if Purchase.choose_products(self) == "1":
    #         print("thanks for shopping")
    #     else:
    #         print(Purchase.choose_products(self))
