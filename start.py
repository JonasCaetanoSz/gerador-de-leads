from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog, messagebox
import os
from extract import extract
from instagrapi import Client
from plyer.utils import platform
from plyer import notification
from threading import Thread

# definindo variaveis importantes
grams = []
#grams.append("oi")
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = os.getcwd() + "/assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def add_gram(label_acc):

    login = entry_2.get()
    passw = entry_3.get()

    # login via sessionID (cookies)
    if  login != "" and login.isspace() is False and  passw == "" or passw.isspace(): 

        try:

            notification.notify(
                title='adicionando nova conta',
                message='fazendo login no instagram, isso pode levar alguns segundos...',
                app_name='extrair contatos do instagram',
                app_icon='assets/icon.' + ('ico' if platform == 'win' else 'png'),
                timeout=1
            )
            gram = Client()
            gram.login_by_sessionid(login)
            grams.append({"gram":gram, "username": gram.account_info().username})
            canvas.itemconfig(label_Acc, text=f'contas: {len(grams)}')
            notification.notify(
                title="sucesso!",
                message='uma nova conta do instagram foi adicionada!',
                app_name='extrair contatos do instagram',
                app_icon='assets/icon.' + ('ico' if platform == 'win' else 'png'),
                timeout=1
            )
            
        
        except Exception as e:

            messagebox.showerror(title="erro ao fazer login", message=f"message: {e}")

    elif login == "" or login.isspace() or passw == "" or passw.isspace():

        messagebox.showerror(title="impossivel fazer login", message="verifique os dados informados")
    
    else:

        try:

            notification.notify(
                title='adicionando nova conta',
                message='fazendo login no instagram, isso pode levar alguns segundos...',
                app_name='extrair contatos do instagram',
                app_icon='assets/icon.' + ('ico' if platform == 'win' else 'png'),
                timeout=1
            )
            gram = Client()
            gram.login(login, passw)
            grams.append({"gram":gram, "username": gram.account_info().username})
            canvas.itemconfig(label_Acc, text=f'contas: {len(grams)}')
            notification.notify(
                title="sucesso!",
                message='uma nova conta do instagram foi adicionada!',
                app_name='extrair contatos do instagram',
                app_icon='assets/icon.' + ('ico' if platform == 'win' else 'png'),
                timeout=1
            )
            
        
        except Exception as e:

            messagebox.showerror(title="erro ao fazer login", message=f"message: {e}")

def iniciar(window, entry_1, entry_4, grams):

    output = entry_1.get()
    user = entry_4.get()

    if user.isspace() or user == "":

        messagebox.showerror(title="nenhum usuario declarado", message="nenhum usuario foi declarado. por favor defina um usuario, ex: @neymar" )

    elif output.isspace() or output == "":

        messagebox.showerror(title="defina a pasta de saida", message="por favor defina a pasta de saida do arquivo xlsx.")


    elif len(grams) == 0:

        messagebox.showerror(title="adicionar conta do instagram", message="por favor adicone ao menos uma conta do instagram, caso tenha alguma duvida leia o README.MD")


    else:

        extract(window=window, user=user,grams=grams, outputfolder=output)



def selecionar_output(entry):

    output = filedialog.askdirectory()
    entry.insert(3, output)

window = Tk()

window.geometry("416x408")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 408,
    width = 416,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    44.0,
    30.0,
    anchor="nw",
    text="extrair seguidores do instagram\n",
    fill="#506563",
    font=("Inter", 14 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    28.0,
    25.0,
    image=image_image_1
)

canvas.create_text(
    13.0,
    123.0,
    anchor="nw",
    text="usuario: ",
    fill="#000000",
    font=("Inter", 14 * -1)
)

canvas.create_text(
    13.0,
    171.0,
    anchor="nw",
    text="salvar em:",
    fill="#000000",
    font=("Inter", 14 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    197.5,
    181.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=112.5,
    y=170.0,
    width=170.0,
    height=21.0
)

canvas.create_text(
    13.0,
    211.0,
    anchor="nw",
    text="login:",
    fill="#000000",
    font=("Inter", 14 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    207.0,
    225.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=115.0,
    y=214.0,
    width=184.0,
    height=20.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: selecionar_output(entry_1),
    relief="flat"
)
button_1.place(
    x=278.0,
    y=168.0,
    width=42.0,
    height=28.0
)

label_Acc = canvas.create_text(
    319.0,
    370.0,
    anchor="nw",
    text="contas : 0",
    fill="#000000",
    font=("Inter", 14 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: Thread(target=add_gram, args=(label_Acc,)).start(),
    relief="flat"
)
button_2.place(
    x=320.0,
    y=252.0,
    width=59.0,
    height=24.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    207.0,
    265.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_3.place(
    x=115.0,
    y=254.0,
    width=184.0,
    height=20.0
)

canvas.create_text(
    13.0,
    251.0,
    anchor="nw",
    text="senha:",
    fill="#000000",
    font=("Inter", 14 * -1)
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:  iniciar(window=window,entry_1=entry_1, grams=grams , entry_4=entry_4),
    relief="flat"
)
button_3.place(
    x=151.0,
    y=318.0,
    width=92.0,
    height=33.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    205.5,
    139.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=112.0,
    y=128.0,
    width=187.0,
    height=20.0
)

window.title("extrair seguidores do instagram")
window.iconbitmap(relative_to_assets("icon.ico"))
window.resizable(False, False)
window.mainloop()
