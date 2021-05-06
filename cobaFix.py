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
        URL = "http://acadia-gemastik.my.id/rest_ci/index.php/penumpang"
        PARAMS = {'uid':uid} 
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
        jumlah = len(data)

        if jumlah > 0 and data[0]['status'] == '1' :
            put = {'id' : data[0]['id_penumpang'], 'status' : 0}
            put = requests.put(url = URL, data = put)
            print put.status_code
            time.sleep(4)
        else :
            d = {'id_bus': 1,  'uid_penumpang': uid}
            requests.post("http://acadia-gemastik.my.id/rest_ci/index.php/penumpang", data=d)
            print "Data berhasil diinput"
            time.sleep(4)
    except:
        print("no connection")
