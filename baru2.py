from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard import util
import time
import requests
WAIT_FOR_SECONDS = 60
card_type = AnyCardType()
request = CardRequest(timeout=WAIT_FOR_SECONDS, cardType=card_type)

while True:
    service = None
    try:
        service = request.waitforcard()
    except CardRequestTimeoutException:
        print("ERROR: No card detected")

    try:
        conn = service.connection
        conn.connect()

        get_uid = util.toBytes("FF CA 00 00 00")
        data, sw1, sw2 = conn.transmit(get_uid)
        uid = util.toHexString(data)
        status = util.toHexString([sw1, sw2])

        print uid
        d = {'nama': 'penumpang',  'nomor': uid}
        requests.post("http://127.0.0.1/rest_ci/index.php/kontak", data=d)
        time.sleep(2)
    except:
        print("no connection")
