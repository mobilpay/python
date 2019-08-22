import hashlib
import random
import time
from mobilPay.address import Address
from mobilPay.invoice import Invoice
from mobilPay.payment.request.card import Card
from mobilPay.util.encrypt_data import Crypto
from mobilPay.util.xml_helper import save_to_xml

payment_url = 'https://www.mobilpay.ro'

# path to your public certificate that contains the public key
x509_filePath = "public_certificate"

obj_pm_req_card = Card()

try:

    obj_pm_req_card.set_signature("signature from server")

    # must set it
    obj_pm_req_card.set_order_id(hashlib.md5(str(int(random.random() * int(time.time()))).encode('utf-8')).hexdigest())

    obj_pm_req_card.set_confirm_url("confirm_url")

    obj_pm_req_card.set_return_url("return_url")

    obj_pm_req_card.set_invoice(Invoice())

    obj_pm_req_card.get_invoice().set_currency("RON")

    obj_pm_req_card.get_invoice().set_amount("0.10")

    obj_pm_req_card.get_invoice().set_token_id("fmndiusnvdfiu")

    obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")

    billing_address = Address("billing")

    #get_from_website
    billing_address.set_type("person")
    billing_address.set_first_name("Loca")
    billing_address.set_last_name("Maca")
    billing_address.set_address("Acasa Bucuresti")
    billing_address.set_email("andrei@netopia.com")
    billing_address.set_mobile_phone("8989989")

    obj_pm_req_card.get_invoice().set_billing_address(billing_address)

    shipping_address = Address("shipping")

    #get_from_website
    shipping_address.set_type("person")
    shipping_address.set_first_name("Vic")
    shipping_address.set_last_name("Loco")
    shipping_address.set_address("Acasa Bucuresti")
    shipping_address.set_email("victorlocoman@gmail.com")
    shipping_address.set_mobile_phone("8989989")

    obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

    obj_pm_req_card.encrypt(x509_filePath)
    data = obj_pm_req_card.get_enc_data()
    key = obj_pm_req_card.get_env_key()

    private_key = Crypto.get_rsa_key("/Users/0dmg/Desktop/Git/python_encryption/private_pem.pem")
    xml_dec = Crypto.decrypt(obj_pm_req_card.get_enc_data(), private_key, obj_pm_req_card.get_env_key())
    print(xml_dec.decode("utf-8"))

    # save your object to xml
    save_to_xml(obj_pm_req_card, "/Users/0dmg/Desktop/Git/NETOPIA/python/mp/loaded.xml")


except Exception as e:
    raise Exception(e)
