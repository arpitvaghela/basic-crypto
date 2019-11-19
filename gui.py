from tkinter import *
from tkinter import ttk, filedialog, messagebox
import DES, ceasar, playfair

root = Tk()
root.geometry('1024x640')
welcomeMsg = "Welcome to Basic-Crypto"

# variables
cipher_values = {"DES": 1, "DES3": 2, "DESX": 3, "ceasar": 4, "playfair": 5}
cipherSelect = IntVar(root, 1)

key1 = StringVar(root, '11111111')
key2 = StringVar(root, '22222222')
key3 = StringVar(root, '33333333')

data_type_values = {"Text": 1, "File": 2}
data_type = IntVar(root, 2)

plaintext = StringVar()
e_text = StringVar()

# widgets
L_welcome = ttk.Label(root, text=welcomeMsg)
#key layer
L_key = ttk.Label(root, text="Key:")
E_k1 = ttk.Entry(root, textvariable=key1)
E_k2 = ttk.Entry(root, textvariable=key2)
E_k3 = ttk.Entry(root, textvariable=key3)


#callback by cipher select
def cipher_callback():
    if cipherSelect.get() == 2 or cipherSelect.get() == 3:
        E_k2.grid(row=2, column=3, columnspan=2)
        E_k3.grid(row=2, column=5, columnspan=2)
    else:
        E_k2.grid_remove()
        E_k3.grid_remove()
    if cipherSelect.get() == 4 or cipherSelect.get() == 5:
        datatype_radioframe.grid(row=3, column=1, columnspan=3)
    else:
        datatype_radioframe.grid_remove()
        data_type.set(2)
        datatype_callback()


#cipher select
L_cipher = ttk.Label(root, text="Select Cipher:")
radioframe = ttk.Frame(root)
for (text, value) in cipher_values.items():
    Radiobutton(radioframe,
                text=text,
                variable=cipherSelect,
                value=value,
                command=cipher_callback).grid(row=0, column=value - 1)

#text boxes
T_plaintext = Text(root, height=25, width=50)
T_e_text = Text(root, height=25, width=50)
L_plaintext = ttk.Label(root, text="Plain Text")
L_e_text = ttk.Label(root, text="Encrypted Text")


#callback by datatype select
def datatype_callback():
    if data_type.get() == 1:
        T_plaintext.grid(row=4, column=0, columnspan=4)
        T_e_text.grid(row=4, column=4, columnspan=4)
        L_plaintext.grid(row=5, column=1)
        L_e_text.grid(row=5, column=5)

    else:
        T_plaintext.grid_remove()
        T_e_text.grid_remove()
        L_plaintext.grid_remove()
        L_e_text.grid_remove()


#datatype select
L_dataType = ttk.Label(root, text="Data Type:")
datatype_radioframe = ttk.Frame(root)
for (text, value) in data_type_values.items():
    Radiobutton(datatype_radioframe,
                text=text,
                variable=data_type,
                value=value,
                command=datatype_callback).grid(row=0, column=value - 1)


def getfiles():
    #print("here")
    path_in = filedialog.askopenfilename(title='Select File to Encrypt')
    path_out = filedialog.asksaveasfilename(title='Select Output File')
    return (path_in, path_out)


def gettxtfiles():
    path_in = filedialog.askopenfilename(title='Select File to Encrypt',
                                         filetypes=(('text files', '.txt'), ))
    path_out = filedialog.asksaveasfilename(title='Select Output File',
                                            filetypes=(('text files',
                                                        '.txt'), ))
    return (path_in, path_out)


def readtxtfile(path):
    with open(path, 'r') as file:
        r = file.read()
    return r


def writetxtfile(path, content):
    with open(path, 'w') as file:
        file.write(content)


def checkshortkey():
    if cipherSelect.get() < 3:
        l1 = len(key1.get())
        if l1 < 8:
            messagebox.showerror("Short Key", "Minimum length required is 8")
        if cipherSelect.get() > 1:
            l2 = len(key2.get())
            l3 = len(key3.get())
            if l2 < 8 or l3 < 8:
                messagebox.showerror("Short Key",
                                     "Minimum length required is 8")


#callback by buttons
def e_callback():
    checkshortkey()
    try:
        if cipherSelect.get() == 1:
            (fin, fout) = getfiles()
            print(fin, fout)
            DES.DES_encrypt_file(fin, key1.get(), fout)
        if cipherSelect.get() == 2:
            (fin, fout) = getfiles()
            DES.DES3_encrypt_file(fin, key1.get(), key2.get(), key3.get(),
                                  fout)
        if cipherSelect.get() == 3:
            (fin, fout) = getfiles()
            DES.DESX_encrypt_file(fin, key1.get(), key2.get(), key3.get(),
                                  fout)
        if cipherSelect.get() == 4:
            if data_type.get() == 2:
                (fin, fout) = gettxtfiles()
                r = readtxtfile(fin)
                try:
                    k = int(key1.get())
                except ValueError:
                    messagebox.showerror(
                        "Error", "Require integer key for ceasar cipher")
                #add alert
                e = ceasar.ceasar_encrypt(r, k)
                writetxtfile(fout, e)
            else:
                plaintext = T_plaintext.get("1.0", END)
                try:
                    k = int(key1.get())
                except ValueError:
                    messagebox.showerror(
                        "Error", "Require integer key for ceasar cipher")
                #add alert
                e = ceasar.ceasar_encrypt(plaintext, k)
                T_e_text.delete("1.0", END)
                T_e_text.insert("1.0", e)
        if cipherSelect.get() == 5:
            if data_type.get() == 2:
                (fin, fout) = gettxtfiles()
                r = readtxtfile(fin)
                e = playfair.encrypt_playfiar(r, key1.get())
                writetxtfile(fout, e)
            else:
                plaintext = T_plaintext.get("1.0", END)
                #add alert
                e = playfair.encrypt_playfiar(plaintext, key1.get())
                T_e_text.delete("1.0", END)
                T_e_text.insert("1.0", e)
    except:
        messagebox.showerror("Error", "Encryption failed")
    else:
        messagebox.showinfo("Info", "Encryption Successful")


def d_callback():
    try:
        if cipherSelect.get() == 1:
            (fin, fout) = getfiles()
            DES.DES_decrypt_file(fin, key1.get(), fout)
        if cipherSelect.get() == 2:
            (fin, fout) = getfiles()
            DES.DES3_decrypt_file(fin, key1.get(), key2.get(), key3.get(),
                                  fout)
        if cipherSelect.get() == 3:
            (fin, fout) = getfiles()
            DES.DESX_decrypt_file(fin, key1.get(), key2.get(), key3.get(),
                                  fout)
        if cipherSelect.get() == 4:
            if data_type.get() == 2:
                (fin, fout) = gettxtfiles()
                r = readtxtfile(fin)
                try:
                    k = int(key1.get())
                except ValueError:
                    messagebox.showerror(
                        "Error", "Require integer key for ceasar cipher")
                e = ceasar.ceasar_decrypt(r, k)
                writetxtfile(fout, e)
            else:
                plaintext = T_e_text.get("1.0", END)
                try:
                    k = int(key1.get())
                except ValueError:
                    messagebox.showerror(
                        "Error", "Require integer key for ceasar cipher")
                p = ceasar.ceasar_decrypt(plaintext, k)
                T_plaintext.delete("1.0", END)
                T_plaintext.insert("1.0", p)
        if cipherSelect.get() == 5:
            if data_type.get() == 2:
                (fin, fout) = gettxtfiles()
                r = readtxtfile(fin)
                w = playfair.decrypt_playfair(r, key1.get())
                writetxtfile(fout, w)
            else:
                e_text = T_e_text.get("1.0", END)
                #add alert
                e = playfair.decrypt_playfair(e_text, key1.get())
                T_plaintext.delete("1.0", END)
                T_plaintext.insert("1.0", e)
    except:
        messagebox.showerror("Error", "Decryption failed")
    else:
        messagebox.showinfo("Info", "Decryption Successful")


#buttons
btn_e = ttk.Button(root, text="Encrypt", command=e_callback)
btn_d = ttk.Button(root, text="Decrypt", command=d_callback)

#grid manager
L_welcome.grid()

L_cipher.grid(row=1)
radioframe.grid(row=1, column=1, columnspan=5)
L_key.grid(row=2)
E_k1.grid(row=2, column=1)

L_dataType.grid(row=3)

btn_e.grid(row=7, column=2)
btn_d.grid(row=7, column=4)

root.mainloop()