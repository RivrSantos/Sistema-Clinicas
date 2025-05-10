import customtkinter as ctk
import sqlite3
from PIL import Image, ImageTk
import io

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def buscar_paciente():
    nome = entry_nome.get()

    if not nome:
        ctk.CTkMessagebox(title="Atenção", message="Digite o nome do paciente.", icon="warning")
        return

    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome, cpf, nascimento, genero, foto FROM pacientes WHERE nome LIKE ?", (f"%{nome}%",))
    paciente = cursor.fetchone()
    conn.close()

    if not paciente:
        ctk.CTkMessagebox(title="Erro", message="Paciente não encontrado.", icon="cancel")
        limpar_dados()
        return

    nome, cpf, nascimento, genero, foto = paciente
    label_info.configure(text=f"Nome: {nome}\nCPF: {cpf}\nNascimento: {nascimento}\nGênero: {genero}")

    if foto:
        imagem = Image.open(io.BytesIO(foto)).resize((160, 160))
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem.configure(image=imagem_tk, text="")
        label_imagem.image = imagem_tk
    else:
        label_imagem.configure(image=None, text="Sem foto")

def limpar_dados():
    label_info.configure(text="")
    label_imagem.configure(image=None, text="Foto")

# Interface
app = ctk.CTk()
app.title("Prontuário do Paciente")
app.geometry("400x500")

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Consultar Prontuário", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

entry_nome = ctk.CTkEntry(frame, placeholder_text="Digite o nome do paciente")
entry_nome.pack(pady=5)

btn_buscar = ctk.CTkButton(frame, text="Buscar", command=buscar_paciente)
btn_buscar.pack(pady=5)

label_info = ctk.CTkLabel(frame, text="", justify="left")
label_info.pack(pady=10)

label_imagem = ctk.CTkLabel(frame, text="Foto", width=160, height=160, corner_radius=8)
label_imagem.pack(pady=10)

app.mainloop()
