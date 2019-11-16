#!/usr/bin/python
from tkinter import *
from tkinter import filedialog
import DES

window = Tk()
window.title('basic-crypto')
window.geometry('1024x640')
OPTIONS = ["DES", "DESX", "DES3", "ceasar", "playfiar"]

#variable
var_cipher = StringVar(window)
var_cipher.set(OPTIONS[0])
key1 = StringVar(window, 'abcdefghijkl')
key2 = StringVar(window, 22222222)
key3 = StringVar(window, 33333333)
data = IntVar()


#callbacks
def e_btn_callback():
    if data.get() == 1:
        path_in = filedialog.askopenfilename(title='Select File to Encrypt')
        path_out = filedialog.asksaveasfilename(title='Select Output File')
        DES.DES_encrypt_file(path_in, key1.get(), path_out)


def d_btn_callback():
    if data.get() == 1:
        path_in = filedialog.askopenfilename(title='Select File to Decrypt')
        path_out = filedialog.asksaveasfilename(title='Select Output File')
        DES.DES_decrypt_file(path_in, key1.get(), path_out)


#widgets
title = Label(
    window,
    text='Welcome to Basic-Crypto',
    font=('Arial', 30),
).grid(row=0, column=1, columnspan=2, pady=(30, 30))
select_ciper = Label(window, text='Select cipher:',
                     font=('Arial', 18)).grid(row=1, padx=(50, 20), sticky=E)

k1 = Entry(window, textvariable=key1, font=('Arial', 14)).grid(row=3, column=1)
k2 = Entry(window, textvariable=key2, font=('Arial', 14)).grid_forget()
k3 = Entry(window, textvariable=key3, font=('Arial', 14)).grid_forget()

cipher_option_menu = OptionMenu(window, var_cipher, OPTIONS[0], OPTIONS[1],
                                OPTIONS[2], OPTIONS[3],
                                OPTIONS[4]).grid(row=1,
                                                 column=1,
                                                 columnspan=2,
                                                 sticky=W)

key_label = Label(window, text='key:', font=('Arial', 18)).grid(row=3,
                                                                padx=(50, 20),
                                                                sticky=E)

Data_label = Label(window, text='Data:',
                   font=('Arial', 18)).grid(row=4, padx=(50, 20), sticky=E)

r1 = Radiobutton(window,
                 text='Text',
                 value=0,
                 font=('Arial', 18),
                 variable=data).grid(row=4, column=1)

r2 = Radiobutton(window,
                 text='File',
                 value=1,
                 font=('Arial', 18),
                 variable=data).grid(row=4, column=2)

btn_e = Button(window, text='Encrypt', command=e_btn_callback).grid(row=5,
                                                                    column=1,
                                                                    sticky=E)

btn_d = Button(window, text='Decrypt', command=d_btn_callback).grid(row=5,
                                                                    column=2,
                                                                    sticky=W)

window.mainloop()
