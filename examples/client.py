
"""
    Client side / Front End

    Path of the imports should be changed according to the location of the module in your project
"""

from urllib.parse import unquote, quote
import requests
import hashlib
import random
import time
from mobilpay.address import Address
from mobilpay.invoice import Invoice
from mobilpay.request import Request
from mobilpay.payment.request.crc import Crc
from mobilpay.payment.request.card import Card
from mobilpay.payment.request.base_request import BaseRequest

# implementation example


def get_and_send_request():
    payment_url = '<mobilpay-url>'

    # path to your public certificate that contains the public key
    x509_filePath = "path_to_public_cert.cer"

    obj_pm_req_card = Card()

    try:
        obj_pm_req_card.set_signature("<signature>")

        # order id
        obj_pm_req_card.set_order_id(
            hashlib.md5(str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest())
        obj_pm_req_card.set_confirm_url("confirmurl")
        obj_pm_req_card.set_return_url("returnurl")
        obj_pm_req_card.set_invoice(Invoice())
        obj_pm_req_card.get_invoice().set_currency("RON")
        obj_pm_req_card.get_invoice().set_amount("0.10")
        obj_pm_req_card.get_invoice().set_token_id("<TokenId>")
        obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")
        billing_address = Address("billing")

        # get_from_website
        billing_address.set_type("person")
        billing_address.set_first_name("Netopia")
        billing_address.set_last_name("Payments")
        billing_address.set_address("Pipera")
        billing_address.set_email("contact@netopia.com")
        billing_address.set_mobile_phone("8989989")

        obj_pm_req_card.get_invoice().set_billing_address(billing_address)

        shipping_address = Address("shipping")
        # get_from_website
        shipping_address.set_type("person")
        shipping_address.set_first_name("Netopia")
        shipping_address.set_last_name("Payments")
        shipping_address.set_address("Pipera")
        shipping_address.set_email("contact@netopia.com")
        shipping_address.set_mobile_phone("8989989")


        obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

        """encoded data and env_key"""
        obj_pm_req_card.encrypt(x509_filePath)
        data = obj_pm_req_card.get_enc_data()
        env_key = obj_pm_req_card.get_env_key()

        return data, env_key

    except Exception as e:
        raise Exception(e)


# request example
try:
    data, key = get_and_send_request()

    r = requests.post("<mobilpay-url>",
                      data={'env_key': key, 'data': data})
    # get status code
    print(r.status_code, r.reason)
    # print response
    print(r.text)

except Exception as e:
    # catch any error that occured
    print(e.args)
