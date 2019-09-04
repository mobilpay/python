### Dependencies

---

##### In order to run the sdk you need to install the following dependencies

- ```python ^3.5.x```
- ```pip install pycrypto```
- ```pip install pyopenssl```


#### Implementation
    See ```server/main.py``` and ```server/main_local``` for implementation


###### Optional

- ```brew install libffi```

- Then reinstall ```cryptography``` or ```boxsdk``` with pip:

- ```pip install cryptography --force-reinstall```

~~~~python

#CLIENT SIDE
payment_url = 'http://sandboxsecure.mobilpay.ro'

# path to your public certificate that contains the public key
x509_filePath = "path_to_cert/public_cert.cer"

obj_pm_req_card = Card()

obj_pm_req_card.set_signature("signature_from_xml")

obj_pm_req_card.set_payment_type("card")

obj_pm_req_card.set_order_id("order_id")

obj_pm_req_card.set_confirm_url("confirm_url")

obj_pm_req_card.set_return_url("return_url")

obj_pm_req_card.set_invoice(Invoice())

obj_pm_req_card.get_invoice().set_currency("RON")

obj_pm_req_card.get_invoice().set_amount("0.10")

obj_pm_req_card.get_invoice().set_token_id("fmndiusnvdfiu")

obj_pm_req_card.get_invoice().set_details("Plata online cu cardul")

billing_address = Address("billing")

billing_address.set_type("person")
billing_address.set_first_name("Netopia")
billing_address.set_last_name("Man")
billing_address.set_address("Acasa Bucuresti")
billing_address.set_email("contact@netopia.com")
billing_address.set_mobile_phone("8989989")

obj_pm_req_card.get_invoice().set_billing_address(billing_address)

shipping_address = Address("shipping")

shipping_address.set_type("person")
shipping_address.set_first_name("Netopia")
shipping_address.set_last_name("House")
shipping_address.set_address("Acasa Bucuresti")
shipping_address.set_email("contact@netopia.com")
shipping_address.set_mobile_phone("8989989")

obj_pm_req_card.get_invoice().set_shipping_address(shipping_address)

obj_pm_req_card.encrypt(x509_filePath)

# encoded data and env_key
data = obj_pm_req_card.get_enc_data()
env_key = obj_pm_req_card.get_env_key()


# SERVER SIDE

~~~~