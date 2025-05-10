import customtkinter as ctk
import sqlite3
import datetime
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

def registrar_pagamento():
    nome = entry_nome.get()
    valor = entry_valor.get()
    forma = combo_forma.get()

    if not nome or not valor or not forma:
        ctk.CTkMessagebox(title="Atenção", message="Preencha todos os campos.", icon="warning")
        return

    try:
        valor_float = float(valor)
    except ValueError:
        ctk.CTkMessagebox(title="Erro", message="Valor inválido.", icon="cancel")
        return

    conn = sqlite3.connect("pacientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pacientes WHERE nome LIKE ?", (f"%{nome}%",))
    resultado = cursor.fetchone()

    if not resultado:
        ctk.CTkMessagebox(title="Erro", message="Paciente não encontrado.", icon="cancel")
        conn.close()
        return

    paciente_id = resultado[0]
    data_hoje = datetime.date.today().isoformat()

    cursor.execute("""
        INSERT INTO pagamentos (paciente_id, valor, forma, data)
        VALUES (?, ?, ?, ?)
    """, (paciente_id, valor_float, forma, data_hoje))

    conn.commit()
    conn.close()

    ctk.CTkMessagebox(title="Sucesso", message="Pagamento registrado com sucesso!", icon="check")
    entry_valor.delete(0, ctk.END)
    combo_forma.set("")

# Interface
app = ctk.CTk()
app.title("Registro de Pagamentos")
app.geometry("400x400")

frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Registrar Pagamento", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome do Paciente")
entry_nome.pack(pady=5)

entry_valor = ctk.CTkEntry(frame, placeholder_text="Valor (R$)")
entry_valor.pack(pady=5)

combo_forma = ctk.CTkComboBox(frame, values=["PIX", "Crédito", "Dinheiro"])
combo_forma.pack(pady=5)

btn_salvar = ctk.CTkButton(frame, text="Registrar", command=registrar_pagamento)
btn_salvar.pack(pady=10)

app.mainloop()
