from smartcard.scard import *
from smartcard.util import     toHexString
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.CardConnection import CardConnection
import time
import requests


def s():
  hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
  assert hresult==SCARD_S_SUCCESS
  hresult, readers = SCardListReaders(hcontext, [])
  assert len(readers)>0
  reader = readers[0]
  hresult, hcard, dwActiveProtocol = SCardConnect(
     hcontext,
     reader,
     SCARD_SHARE_SHARED,
     SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)
  try:
   hresult, response = SCardTransmit(hcard,dwActiveProtocol,[0xFF,0xCA,0x00,0x00,0x04])
   uid = toHexString(response, format=0)
   print uid
   d = {'nama': 'penumpang',  'nomor': uid}
   requests.post("http://127.0.0.1/rest_ci/index.php/kontak", data=d)
  except SystemError:
   print "no card found"



while 1:
   act = AnyCardType()
   cr = CardRequest(timeout=10, cardType=act )
   cs = cr.waitforcard()
   cs.connection.connect()
   s()
   time.sleep(5)