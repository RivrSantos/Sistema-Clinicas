import customtkinter as ctk
import subprocess
import tkinter.messagebox
from PIL import Image

ctk.set_appearance_mode("blue")
ctk.set_default_color_theme("blue")

app= ctk.CTk()
app.minsize(1366, 960)
app.title("Sistema Médico com IA")
# my_image = ctk.CTkImage(dark_image= Image.open("venv/imagens/paper.jpg"), size=(1366, 960))    #485,335
ctk.CTkLabel(app, width= 0, height= 0, text= '\n\n\n\n\n\n\n "Nosso proposito e salvar vidas;\n                Unindo ciencia e Tecnologia"', text_color= "#34495e", font=('Segoe UI', 35, 'bold')).place(x= 0, y= 0, relwidth= 1, relheight= 1)

def abrir(modulo):
    subprocess.Popen(["python", modulo])

def fechar(app):
    tkinter.messagebox.showwarning("Fechar", "O programa sera encerrado, feche todas janelas!")
    app= app.destroy()

titulo = ctk.CTkLabel(app, text="Menu Principal", text_color= "#34495e", width= 100, height= 30, corner_radius= 10, font=('Segoe UI', 35, 'bold'))
titulo.pack(pady=20)

ctk.CTkLabel(app, text= "Anotações", text_color= "#34495e",width= 130, height= 30, font=('Segoe UI', 25, 'bold')).place(x= 100, y= 30)
anotacoes= ctk.CTkTextbox(app, width= 300, height= 400, border_width= 3, border_color= "blue", border_spacing= 10, fg_color= "#34495e", text_color= "white", corner_radius= 10, font=('Segoe UI', 18, 'bold'))
anotacoes.place(x= 30, y= 80)

botoes = [
    ("Cadastrar Paciente", "venv/cadastro.py"),
    ("Prontuário", "venv/prontuario.py"),
    ("Pagamentos", "venv/pagamentos.py"),
    ("Histórico", "venv/historico.py"),
    ]

for texto, arquivo in botoes:
    btn = ctk.CTkButton(app, text=texto, text_color= "white", width=220, height= 30, font=('Segoe UI', 18, 'bold'), command=lambda a=arquivo: abrir(a))
    btn.pack(pady=15)

btn = ctk.CTkButton(app, text="Sair", text_color= "white", width=100, height= 30, font=('Segoe UI', 18, 'bold'), command= lambda a=app: fechar(a))
btn.pack(pady=15)

app.mainloop()
