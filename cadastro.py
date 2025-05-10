import customtkinter as ctk
import cv2
import sqlite3
from PIL import Image, ImageTk
import io
import tkinter.messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Variável global para imagem capturada
imagem_capturada = None

# Banco de dados
def salvar_paciente():
    global imagem_capturada
    nome = entry_nome.get().strip()
    cpf = entry_cpf.get().strip()
    nascimento = entry_nascimento.get().strip()
    genero = combo_genero.get().strip()

    if not (nome and cpf and nascimento and genero):
        tkinter.messagebox.showwarning("Erro", "Preencha todos os campos.")
        return

    if imagem_capturada is None:
        tkinter.messagebox.showwarning("Erro", "Capture uma imagem antes de salvar.")
        return

    try:
        conn = sqlite3.connect("pacientes.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nome, cpf, nascimento, genero, foto)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, cpf, nascimento, genero, imagem_capturada))
        conn.commit()
        conn.close()
        tkinter.messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
        limpar_campos()
    except sqlite3.IntegrityError as e:
        tkinter.messagebox.showerror("Erro", f"CPF já cadastrado ou erro ao salvar.\n{e}")
    except Exception as e:
        tkinter.messagebox.showerror("Erro", f"Erro inesperado ao salvar paciente:\n{e}")

# Captura de imagem da webcam
def capturar_foto():
    global imagem_capturada
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        tkinter.messagebox.showerror("Erro", "Não foi possível acessar a câmera.")
        return

    def capturar():
        ret, frame = cap.read()
        if ret:
            cap.release()
            cv2.destroyAllWindows()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imagem = Image.fromarray(frame_rgb).resize((160, 160))
            buffer = io.BytesIO()
            imagem.save(buffer, format='PNG')
            global imagem_capturada
            imagem_capturada = buffer.getvalue()

            imagem_tk = ImageTk.PhotoImage(imagem)
            label_imagem.configure(image=imagem_tk, text="")
            label_imagem.image = imagem_tk

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Pressione C para Capturar", frame)
        key = cv2.waitKey(1)
        if key == ord('c'):
            capturar()
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Limpa os campos do formulário
def limpar_campos():
    entry_nome.delete(0, ctk.END)
    entry_cpf.delete(0, ctk.END)
    entry_nascimento.delete(0, ctk.END)
    combo_genero.set("")
    label_imagem.configure(image=None, text="Foto")

# Interface
app = ctk.CTk()
app.title("Cadastro de Paciente")
app.geometry("400x600")

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Cadastro de Paciente", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome")
entry_nome.pack(pady=5)

entry_cpf = ctk.CTkEntry(frame, placeholder_text="CPF")
entry_cpf.pack(pady=5)

entry_nascimento = ctk.CTkEntry(frame, placeholder_text="Data de nascimento (AAAA-MM-DD)")
entry_nascimento.pack(pady=5)

combo_genero = ctk.CTkComboBox(frame, values=["Masculino", "Feminino", "Outro"])
combo_genero.pack(pady=5)

label_imagem = ctk.CTkLabel(frame, text="Foto", width=160, height=160, corner_radius=8)
label_imagem.pack(pady=10)

btn_foto = ctk.CTkButton(frame, text="Capturar Imagem", command=capturar_foto)
btn_foto.pack(pady=5)

btn_salvar = ctk.CTkButton(frame, text="Salvar Paciente", command=salvar_paciente)
btn_salvar.pack(pady=10)

app.mainloop()


