import json
import logging

name = "Customer"
logger = logging.getLogger("Customer related")
logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',
                    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s' \n",
                    datefmt='%d-%b-%y %H:%M:%S')


# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('your name is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

class Customer:
    # customer_invoice = [{"shop name ": "shop_name", "username": "09122334367", "purchase list": [], "total price":
    # []}]

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def see_invoices():  # customers invoices stored in a json file
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
