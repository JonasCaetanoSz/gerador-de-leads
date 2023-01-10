from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage, Toplevel, messagebox
from insta import Instagram
from threading import Thread
import os
from instagrapi import Client

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.getcwd() + "/assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def close(insta:Instagram):

    try: 

        insta.book.save(rf"{insta.xlsxpath}/{insta.user}.xlsx")
        quit()
    
    except Exception as e:
        
        quit()
        
# adiconar conta 

def add_gram(insta):

    try:

        usuario = input("\n[+] digite seu nome de usuario: ")
        senha = input("\n[+] digite sua senha : ")
        print("\n[*] fazendo login no instagram")
        gram = Client()
        gram.login(usuario, senha)
        insta.grams.append({"gram":gram, "username": gram.account_info().username})
        print("login realizado com sucesso!")
        insta.writeLog("login realizado com sucesso!")

    except Exception as e:

        print("erro ao fazer login")
        print(e)
# janela de extração

def extract(window, user, grams, outputfolder):

    window.geometry("477x318")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 318,
        width = 477,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(
        0.0,
        1.0,
        477.0,
        319.0,
        fill="#D9D9D9",
        outline="")

    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        25.0,
        25.0,
        image=image_image_1
    )

    canvas.create_text(
        50.0,
        36.0,
        anchor="nw",
        text="extrair seguidores do instagram",
        fill="#254C51",
        font=("Inter", 13 * -1)
    )

    canvas.create_rectangle(
        182.0,
        93.0,
        325.0,
        121.0,
        fill="#D9D9D9",
        outline="")

    canvas.create_text(
        186.0,
        99.0,
        anchor="nw",
        text="usuario: " + user,
        fill="#000000",
        font=("Inter", 14 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_1 = canvas.create_image(
        238.5,
        256.0,
        image=entry_image_1
    )
    entry_1 = Text(
        bd=0,
        bg="#282626",
        fg="#FFF",
        highlightthickness=0,
        font=("Inter", 10 * -1)
    )
    entry_1.place(
        x=0.0,
        y=193.0,
        width=477.0,
        height=124.0
    )

    text_total = canvas.create_text(
        5.0,
        168.0,
        anchor="nw",
        text="0 analisados de 0 seguidores:",
        fill="#000000",
        font=("Inter", 14 * -1)
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: Thread(target=add_gram, args=(insta,)).start(),
        relief="flat"
    )
    button_1.place(
        x=317.0,
        y=4.0,
        width=160.0,
        height=21.0
    )

    insta = Instagram(user=user, output=outputfolder, grams=grams, log_entry=entry_1, text_total=text_total,window=window, canvas=canvas)
    theardInsta = Thread(target=insta.obterseguidores, daemon=True)
    theardInsta.start()
    window.resizable(False, False)
    window.title("extraindo seguidores")
    window.iconbitmap(relative_to_assets("icon.ico"))
    window.protocol("WM_DELETE_WINDOW", lambda: close (insta))
    window.mainloop()

