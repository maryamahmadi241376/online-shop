import csv
import logging
import json

name = "Manager"
logger = logging.getLogger("Manager related")
logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',
                    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s' \n",
                    datefmt='%d-%b-%y %H:%M:%S')


class Manager:
    def __init__(self, user, name_shop, start_work, end_work):
        self.username = user
        self.shop_name = name_shop
        self.start_work = start_work
        self.end_work = end_work

    @classmethod
    def enter_manager(cls, user, name_shop, start_work, end_work):
        return cls(user, name_shop, start_work, end_work)

    shopping = []

    # shopping = [{"barcode": 1001, "brand": "HP-AE12", "available": 100, "price": 25000, "product name": "HP
    # laptop"}, {"barcode": 1002, "brand": "DELL", "available": 100, "price": 35000, "product name": "Dell laptop"},
    # {"barcode": 1003, "brand": "ASUS", "available": 100, "price": 28000, "product name": "Asus laptop"},
    # {"barcode": 1004, "brand": "APPLE", "available": 100, "price": 60000, "product name": "Apple laptop"},
    # {"barcode": 1005, "brand": "ACER", "available": 100, "price": 24000, "product name": "Acer laptop"},
    # {"barcode": 1006, "brand": "SAMSUNG", "available": 100, "price": 35000, "product name": "Samsung laptop"},
    # {"barcode": 1007, "brand": "OPPO", "available": 100, "price": 15000, "product name": "Oppo laptop"},
    # {"barcode": 1008, "brand": "XAOMI", "available": 100, "price": 45000, "product name": "Xaomi laptop"},
    # {"barcode": 1009, "brand": "HUAWEI", "available": 100, "price": 20000, "product name": "Huawei laptop"},
    # {"barcode": 1010, "brand": "VIVO", "available": 100, "price": 12000, "product name": "Vivo laptop"}]

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
        with open('CustomerInvoice.json', 'r+') as fp:
            try:
                data = json.load(fp)
            except:
                data = []
            if not isinstance(data, list):
                data = []

            data.append(
                {
                    'username': "username",
                    'purchase list': [],
                    'shop name': "shop_name",
                    'total price': []
                }
            )
            with open('CustomerInvoice.json', 'w+') as fp:
                json.dump(data, fp, indent=2)
        with open('CustomerInvoice.json', 'r') as invoice:
            lst = json.load(invoice)
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
            for row in list(reader):
                if row['username'] == chosen_username and row['roll'] != 'customer':
                    with open('ShopList.json', 'r') as f:
                        lst = json.load(f)
                        for dic in lst:
                            if chosen_username in dic["block list"]:
                                raise Exception("this user is already blocked!")
                            if dic['username'] != self.username:
                                dic["block list"].append(chosen_username)
                                with open('ShopList.json', 'w') as training:
                                    json.dump(dic, training, indent=1)
        return f"{chosen_username}, is added to the block list"

