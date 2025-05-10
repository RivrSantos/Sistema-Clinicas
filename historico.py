import customtkinter as ctk
import sqlite3
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def buscar_historico():
    nome = entry_nome.get()
    if not nome:
        ctk.CTkMessagebox(title="Atenção", message="Digite o nome do paciente.", icon="warning")
        return

    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pacientes WHERE nome LIKE ?", (f"%{nome}%",))
    paciente = cursor.fetchone()

    if not paciente:
        ctk.CTkMessagebox(title="Erro", message="Paciente não encontrado.", icon="cancel")
        return

    paciente_id = paciente[0]
    cursor.execute("SELECT data, valor, forma FROM pagamentos WHERE paciente_id = ?", (paciente_id,))
    pagamentos = cursor.fetchall()
    conn.close()

    texto_resultado = ""
    if pagamentos:
        for data, valor, forma in pagamentos:
            texto_resultado += f"{data} - R$ {valor:.2f} - {forma}\n"
    else:
        texto_resultado = "Nenhum pagamento registrado."

    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    textbox.insert("0.0", texto_resultado)
    textbox.configure(state="disabled")

# Interface
app = ctk.CTk()
app.title("Histórico de Pagamentos")
app.geometry("450x450")

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Consultar Histórico", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome do Paciente")
entry_nome.pack(pady=5)

btn_buscar = ctk.CTkButton(frame, text="Buscar", command=buscar_historico)
btn_buscar.pack(pady=5)

textbox = ctk.CTkTextbox(frame, width=400, height=300, state="disabled")
textbox.pack(pady=10)

app.mainloop()
