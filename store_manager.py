import csv
import logging
import json
from person import Person

name = "Manager"
logger = logging.getLogger("Manager related")
logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',
                    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s' \n",
                    datefmt='%d-%b-%y %H:%M:%S')


class Manager(Person):
    def __init__(self, username, password, name_shop=None, start_work=None, end_work=None):
        super().__init__(username, password)
        self.password = password
        self.username = username
        self.shop_name = name_shop
        self.start_work = start_work
        self.end_work = end_work

    @classmethod
    def enter_manager(cls, user, password, *args):
        return cls(user, user, password, *args)

    shopping = []

    def add_product(self):  # manager adds products
        try:
            n = int(input("Enter the no.of.items need to be added : "))
            for i in range(n):
                barcode = input("Enter new barcode: ")
                price = int(input("Enter new price: "))
                brand = input("Enter new brand: ")
                product_name = input("Enter new product name: ")
                available_goods = input("Enter number of available goods: ")
                products = [{"barcode": barcode,
                             "price": price,
                             "brand": brand,
                             "product name": product_name,
                             "available": available_goods}]
                Manager.shopping.append(products)  # new products will be added to previous products
                with open('ShopList.json', 'r') as f:  # new products will be saved to the file
                    lst = json.load(f)
                    for dic in lst:
                        if dic['username'] == self.username:
                            dic['product list'].append(products[0])
                            with open('ShopList.json', 'w') as training:
                                json.dump(lst, training, indent=1)
                    logging.info('New products added')
                return f'new products added: {products}'
        except Exception as e:
            print(e)
            logging.warning("wrong value")

    def available_products(self):
        try:
            with open('ShopList.json', 'r') as s:  # manager reads available products from the file
                lst = json.load(s)
                for dic in lst:
                    if len(dic["product list"]) > 0 and dic['username'] == self.username:
                        return f"list of products :\n{dic['product list']}"
                    else:
                        return f"No products available"
            # return f"{d['product name']} = {d['available']}"
        except Exception as e:
            print(f"{e}, has occurred")

    def warning(self):  # warn the manager about the products that he is running out of
        try:
            with open('ShopList.json', 'r') as s:
                lst = json.load(s)
                for dic in lst:
                    for inner_dic in dic["product list"]:
                        if int(inner_dic['available']) < 10 and dic['username'] == self.username:
                            logging.warning("These goods are running out")
                            return f"Warning! These goods are running out:\n{inner_dic}"
                        else:
                            logging.info("All goods are available now")
                            return f"All goods are available now"
        except Exception as e:
            print(f"{e}, no available item")

    @staticmethod
    def customer_invoice():  # manager can see his customers invoices from the related file
        with open('CustomerInvoice.csv', 'r') as invoice:
            reader = csv.DictReader(invoice)
            lst = list(reader)
            for row in lst:
                if len(lst) > 0:
                    return f"customers invoices :\n {row}"
                else:
                    raise Exception("No invoices available yet!")

    @staticmethod
    def customer_info():
        try:
            with open("UserInfo.csv", "r") as user:
                r = csv.DictReader(user)
                for rows in list(r):
                    for k, v in rows.items():
                        if k == 'roll' and v == 'customer':
                            print(rows)
                            logging.info(f"list of customers:\n{rows}")
            return f"list of customers"
        except Exception as e:
            logging.info("No customers!")
            print(e)

    def block_customer(self, chosen_username):  # manager chooses a username and adds it to the block list
        with open('UserInfo.csv', 'r') as user_info:
            reader = csv.DictReader(user_info)
            users_list = [d['username'] for d in list(reader)]
            if chosen_username in users_list:
                with open('ShopList.json', 'r') as f:
                    lst = json.load(f)
                    manager_shop = [d for d in lst if d["username"] == self.username][0]
                    if chosen_username in manager_shop["block list"]:
                        raise Exception("this user is already blocked!")
                    manager_shop["block list"].append(chosen_username)
                    with open('ShopList.json', 'w') as training:
                        json.dump(lst, training, indent=1)
        return f"{chosen_username}, is added to the block list"
