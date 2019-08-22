from urllib.parse import unquote, quote
from flask import Flask
from flask import request
from mobilPay.payment.request.base_request import BaseRequest
from mobilPay.request import Request
from xml.dom.minidom import Document

app = Flask(__name__)


@app.route('/', methods=["POST"])
def demo():
    error_code = 0
    error_type = BaseRequest.CONFIRM_ERROR_TYPE_NONE
    error_message = ""
    if request.method == "POST":
        # calea catre cheia privata
        private_key_path = "/Users/0dmg/Desktop/Git/NETOPIA/sandbox.JM4B-T2Q5-67WU-EEUH-8C4Lprivate.key"

        # get the envelope key and data from the request
        result = request.form.to_dict()
        env_key = result["env_key"]
        env_data = result["data"]

        # env_key si data trebuie parsate pentru ca vin din url, se face cu function unquote din urllib
        obj_pm_request = Request().factory_from_encrypted(unquote(env_key), unquote(env_data), private_key_path)

        notify = obj_pm_request.get_notify()

        # rrn
        rrn = notify.rrn

        if env_key is not None and len(env_key) > 0 and env_data is not None and len(env_data) > 0:
            try:
                if int(notify.errorCode) == 0:
                    """
                    # orice action este insotit de un cod de eroare si de un mesaj de eroare. Acestea pot fi citite
                    # folosind error_code = obj_pm_req.get_notify().errorCode
                    # respectiv error_message = obj_pm_req.get_notify()errorMessage
                    # pentru a identifica ID-ul comenzii pentru care primim rezultatul platii folosim
                    # order_id = obj_pm_req.get_order_id()
                    """
                    if notify.action == "confirmed":
                        """ 
                        # cand action este confirmed avem certitudinea ca banii au plecat din contul posesorului de
                        # card si facem update al starii comenzii si livrarea produsului
                        # update DB, SET status = "confirmed/captured"
                        """
                        error_message = notify.errorMessage
                    elif notify.action == "confirmed_pending":
                        """ 
                        # cand action este confirmed_pending inseamna ca tranzactia este in curs de verificare
                        # antifrauda. Nu facem livrare/expediere. In urma trecerii de aceasta verificare se va primi o
                        # noua notificare pentru o actiune de confirmare sau anulare.
                        # update DB, SET status = "pending"
                        """
                        error_message = notify.errorMessage
                    elif notify.action == "paid_pending":
                        """
                        # cand action este paid_pending inseamna ca tranzactia este in curs de verificare. 
                        # Nu facem livrare/expediere. In urma trecerii de aceasta verificare se va primi o noua 
                        # notificare pentru o actiune de confirmare sau anulare.
                        # update DB, SET status = "pending"
                        """
                        error_message = notify.errorMessage
                    elif notify.action == "paid":
                        # cand action este paid inseamna ca tranzactia este in curs de procesare.
                        # Nu facem livrare/expediere. In urma trecerii de aceasta procesare se va primi o noua
                        # notificare pentru o actiune de confirmare sau anulare.
                        # update DB, SET status = "open/preauthorized"
                        error_message = notify.errorMessage
                    elif notify.action == "canceled":
                        # cand action este canceled inseamna ca tranzactia este anulata. Nu facem livrare/expediere.
                        # update DB, SET status = "canceled"
                        error_message = notify.errorMessage
                    elif notify.action == "credit":
                        """
                        # cand action este credit inseamna ca banii sunt returnati posesorului de card. 
                        # Daca s-a facut deja livrare, aceasta trebuie oprita sau facut un reverse. 
                        # update DB, SET status = "refunded"
                        """
                        error_message = notify.errorMessage
                    else:
                        error_type = Request.CONFIRM_ERROR_TYPE_PERMANENT
                        error_code = Request.ERROR_CONFIRM_INVALID_ACTION
                        error_message = 'mobilpay_refference_action paramaters is invalid'
                else:
                    """#update DB, SET status = "rejected"""
                    error_message = notify.errorMessage
                    # error_type = Request.CONFIRM_ERROR_TYPE_TEMPORARY # not sure here
                    # error_code = notify.errorCode
            except Exception as e:
                error_type = Request.CONFIRM_ERROR_TYPE_TEMPORARY
                error_code = e.code
                error_message = 'mobilpay_refference_action paramaters is invalid'
        else:
            error_type = Request.CONFIRM_ERROR_TYPE_PERMANENT
            error_code = Request.ERROR_CONFIRM_INVALID_POST_PARAMETERS
            error_message = 'mobilpay.ro posted invalid parameters'
    else:
        error_type = Request.CONFIRM_ERROR_TYPE_PERMANENT
        error_code = Request.ERROR_CONFIRM_INVALID_POST_METHOD
        error_message = 'invalid request method for payment confirmation'

    crc = Document()
    crc_text = crc.createElement("crc")
    crc_value = crc.createTextNode(error_message)

    if error_code != 0:
        crc_text.setAttribute("error_type", str(error_type))
        crc_text.setAttribute("error_code", str(error_code))

    crc_text.appendChild(crc_value)
    crc.appendChild(crc_text)

    return crc.toprettyxml(indent="\t", newl="\n", encoding="utf-8")


if __name__ == '__main__':
    app.run()
