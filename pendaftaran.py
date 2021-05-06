from tkinter import *
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import CardRequestTimeoutException
from smartcard.CardType import AnyCardType
from smartcard import util
import time
import requests
WAIT_FOR_SECONDS = 60
card_type = AnyCardType()
request = CardRequest(timeout=WAIT_FOR_SECONDS, cardType=card_type)


while 1:
    screen = Tk()
    screen.geometry("500x600")
    screen.title("Form Pendaftaran User")


    def save_info():
        firstname_info = firstname.get()
        lastname_info = lastname.get()
        alamat_info = alamat.get()
        print(firstname_info, lastname_info, nomor_ktp)
        d = {'nama_pengguna': firstname_info,  'uid_pengguna': nomor_ktp, 'nomor_pengguna': lastname_info, 'alamat_pengguna': alamat_info}
        requests.post("http://acadia-gemastik.my.id/rest_ci/index.php/pengguna", data=d)
        print(" User ", alamat_info, " has been registered successfully")

        firstname_entry.delete(0, END)
        lastname_entry.delete(0, END)
        #   uid_text.delete(0, END)
        screen.destroy()

    heading = Label(text = "Form Pendaftaran User", bg = "#007BFF", fg = "white", width = "500", height = "3", font=("bold",20))
    heading.pack()
    firstname_text = Label(text = "Nama Lengkap",font=("bold",15))
    lastname_text = Label(text = "Nomor Telepon", font=("bold",15))
    uid_text = Label(text = "UID", font=("bold",15))
    alamat_text = Label(text= "Alamat", font=("bold",15))
    uid_text.place(x = 15, y = 270)
    firstname_text.place(x = 15, y = 130)
    lastname_text.place(x = 15, y = 200)
    alamat_text.place(x = 15, y = 340)
    card = True
    while card:
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
            card = False
            print uid 

            age_entry = Label(text = uid, width = "30",font=("bold",15))
            age_entry.place(x = 15, y = 310)
            nomor_ktp = uid
            time.sleep(4)
        except:
            print("no connection")
            card = True

    firstname = StringVar()
    lastname = StringVar()
    nomor_ktp = uid
    alamat = StringVar()

    firstname_entry = Entry(textvariable = firstname, width = "30",font=("bold",15))
    lastname_entry = Entry(textvariable = lastname, width = "30",font=("bold",15))
    alamat_entry = Entry(textvariable = alamat, width = "30",font=("bold",15))

    firstname_entry.place(x = 15, y = 170)
    lastname_entry.place(x = 15, y = 240)
    alamat_entry.place(x = 15, y = 380)

    register = Button(screen,text = "Register", width = "30", height = "2", command = save_info, bg = "#007BFF", fg = "white")
    register.place(x = 15, y = 450)

    screen.mainloop()