from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
from smartcard.util import toHexString
import time

import sys
getuid=[0xFF, 0xCA, 0x00, 0x00, 0x00]
act = AnyCardType()
while 1:
    cr = CardRequest( timeout=10, cardType=act )
    cs = cr.waitforcard()
    cs.connection.connect()

    data, sw1, sw2 = cs.connection.transmit(getuid)
    if (sw1, sw2) == (0x90, 0x0):
        print("Status: The operation completed successfully.")
    elif (sw1, sw2) == (0x63, 0x0):
        print("Status: The operation failed.")

    print("uid={}".format(data))
    cs.connection.disconnect()
    time.sleep(5)
