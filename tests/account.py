from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import os
from threading import Thread
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.getcwd() + "/assets"
grams = []


def continuar():

    if len(grams) == 0:

        messagebox.showerror("não está esquecendo de nada?", "nenhuma conta foi adicionada, para continuar você precisa adicionar ao menos uma.")
    
    else:

        return grams

def cancelar(window):

    return False
    window.destroy()
def add_gram(entry_1, entry_2):

    user = entry_1.get()
    passw = entry_2.get()

    if user.isspace() or user == "" or passw.isspace() or passw == "":

        messagebox.showerror("login ou senha invalidos", "os dados informados não são validos, verifique-os e tente novamente.")
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def account(Toplevel):
    
    window = Toplevel
    window.geometry("409x259")
    window.configure(bg = "#FFFFFF")


    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 259,
        width = 409,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: continuar(),
        relief="flat"
    )
    button_1.place(
        x=65.0,
        y=201.0,
        width=106.0,
        height=30.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: cancelar(window),
        relief="flat"
    )
    button_2.place(
        x=245.0,
        y=198.0,
        width=102.0,
        height=30.0
    )

    canvas.create_text(
        30.0,
        105.0,
        anchor="nw",
        text="usuario:",
        fill="#000000",
        font=("Inter", 14 * -1)
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_1 = canvas.create_image(
        206.0,
        116.0,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=114.0,
        y=104.0,
        width=184.0,
        height=22.0
    )

    canvas.create_text(
        125.0,
        23.0,
        anchor="nw",
        text="adicione uma nova conta",
        fill="#000000",
        font=("Inter", 14 * -1)
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: add_gram(entry_1, entry_2),
        relief="flat"
    )
    button_3.place(
        x=321.0,
        y=143.0,
        width=52.0,
        height=24.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_2 = canvas.create_image(
        206.0,
        156.0,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=114.0,
        y=144.0,
        width=184.0,
        height=22.0
    )

    canvas.create_text(
        29.0,
        150.0,
        anchor="nw",
        text="senha:",
        fill="#000000",
        font=("Inter", 14 * -1)
    )
    window.resizable(False, False)
    window.mainloop()
