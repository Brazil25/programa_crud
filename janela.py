from tkinter import *
from tkinter import messagebox
import pyodbc
from datetime import datetime

dados_conexao = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost;"
    "Database=EstoqueMentoria;"
    "UID=seu_usuario_aqui;"
    "PWD=sua_senha_aqui;"
    "TrustServerCertificate=yes;"
)
conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

#procurar insumo
def btn_clicked0():
    nome_insumo = entry1.get().strip()

    comando = "SELECT * FROM Insumos WHERE nome_insumo = ?"
    cursor.execute(comando, (nome_insumo,))
    
    resultados = cursor.fetchall()

    entry0.delete("1.0", END)

    if len(resultados) > 0:
        for linha in resultados:
            texto = f"Item: {linha.nome_insumo}\nQuantidade: {linha.qtde}\nLote: {linha.lote}\nValidade: {linha.data_validade}\n"
            entry0.insert(END, texto)
    else:
        messagebox.showinfo(title="AVISO - Busca de Insumo", message=f"O insumo {nome_insumo} não está registrado no banco de dados!")
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)

#deletar insumo
def btn_clicked1():
    nome_insumo = entry1.get().strip()
    
    comando_buscar = "SELECT * FROM Insumos WHERE nome_insumo = ?"
    cursor.execute(comando_buscar, (nome_insumo,))
    
    resultados = cursor.fetchall()

    entry0.delete("1.0", END)

    if len(resultados) > 0:
        comando_deletar = "DELETE from Insumos WHERE nome_insumo = ?"
        cursor.execute(comando_deletar, (nome_insumo,))
        cursor.commit()
        messagebox.showinfo(title="AVISO - Exclusão de Insumo", message=f"O insumo {nome_insumo} foi excluído com sucesso!")
    else:
        messagebox.showinfo(title="AVISO - Exclusão de Insumo", message=f"O insumo {nome_insumo} não está registrado no banco de dados!")
    entry0.delete("1.0", END)
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)

#consumir insumo
def btn_clicked2():
    nome_insumo = entry1.get().strip()
    qtde_usada = int(entry4.get().strip())

    comando_buscar = "SELECT * FROM Insumos WHERE nome_insumo = ?"
    cursor.execute(comando_buscar, (nome_insumo,))
    
    resultados = cursor.fetchall()

    entry0.delete("1.0", END)

    if len(resultados) > 0:
        comando_buscar2 = "SELECT qtde FROM Insumos WHERE nome_insumo = ?"
        cursor.execute(comando_buscar2, (nome_insumo,))
        
        resultados2 = cursor.fetchone()
        qtde_atual = int(resultados2.qtde)
        if qtde_usada < qtde_atual:
            comando_consumir = """UPDATE Insumos
                    SET qtde = qtde - ?
                    WHERE nome_insumo = ?;"""

            cursor.execute(comando_consumir, (qtde_usada, nome_insumo))
            cursor.commit()
            messagebox.showinfo(title="AVISO - Consumo de Insumo", message=f"{qtde_usada} unidades do insumo {nome_insumo} consumidas com sucesso!")
        elif qtde_usada == qtde_atual:
            comando_deletar = "DELETE from Insumos WHERE nome_insumo = ?"
            cursor.execute(comando_deletar, (nome_insumo,))
            cursor.commit()
            messagebox.showinfo(title="AVISO - Consumo de Insumo", message=f"O insumo {nome_insumo} foi completamente consumido, então foi excluído do banco de dados!")
        else:
            messagebox.showinfo(title="AVISO - Consumo de Insumo", message=f"Estoque insuficiente!\nEstoque atual: {qtde_atual}\nTentativa de consumo: {qtde_usada}")
    else:
        messagebox.showinfo(title="AVISO - Consumo de Insumo", message=f"O insumo {nome_insumo} não está registrado no banco de dados!")
    entry0.delete("1.0", END)
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)


#adicionar insumo
def btn_clicked3():
    try:
        nome_insumo = entry1.get().strip()
        data_validade_str = entry2.get().strip()
        lote = entry3.get().strip()
        qtde = entry4.get().strip()
            
        data_validade = datetime.strptime(data_validade_str, "%d/%m/%Y").date()
        qtde = int(qtde)

        comando_buscar = "SELECT * FROM Insumos WHERE nome_insumo = ?"
        cursor.execute(comando_buscar, (nome_insumo,))
        
        resultados = cursor.fetchall()

        entry0.delete("1.0", END)

        if len(resultados) > 0:
            comando_adicionar = """UPDATE Insumos
                                SET qtde = qtde + ?
                                WHERE nome_insumo = ?;"""
            
            cursor.execute(comando_adicionar, (qtde, nome_insumo))
            cursor.commit()
            messagebox.showinfo(title="AVISO - Adição de Insumo", message=f"{qtde} unidades do insumo {nome_insumo} adicionadas com sucesso!")
        else:
            comando_adicionar = """INSERT INTO Insumos (nome_insumo, data_validade, lote, qtde)
                        VALUES (?, ?, ?, ?);"""

            cursor.execute(comando_adicionar, (nome_insumo, data_validade, lote, qtde))
            cursor.commit()
            messagebox.showinfo(title="AVISO - Adição de Insumo", message=f"Insumo {nome_insumo} adicionado com sucesso!")
    except:
        messagebox.showinfo(title="AVISO - Adição de Insumo", message="Por favor, preencha todos os campos para adicionar um insumo!")
    entry0.delete("1.0", END)
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)


window = Tk()

window.geometry("711x646")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 646,
    width = 711,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"imagens/background.png")
background = canvas.create_image(
    355.5, 323.0,
    image=background_img)

img0 = PhotoImage(file = f"imagens/img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked0,
    relief = "flat")

b0.place(
    x = 479, y = 195,
    width = 178,
    height = 38)

img1 = PhotoImage(file = f"imagens/img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked1,
    relief = "flat")

b1.place(
    x = 247, y = 197,
    width = 178,
    height = 36)

img2 = PhotoImage(file = f"imagens/img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked2,
    relief = "flat")

b2.place(
    x = 479, y = 123,
    width = 178,
    height = 35)

img3 = PhotoImage(file = f"imagens/img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked3,
    relief = "flat")

b3.place(
    x = 247, y = 125,
    width = 178,
    height = 34)

entry0_img = PhotoImage(file = f"imagens/img_textBox0.png")
entry0_bg = canvas.create_image(
    455.0, 560.0,
    image = entry0_img)

entry0 = Text(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 250, y = 502,
    width = 410,
    height = 114)

entry1_img = PhotoImage(file = f"imagens/img_textBox1.png")
entry1_bg = canvas.create_image(
    517.0, 294.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 377, y = 278,
    width = 280,
    height = 31)

entry2_img = PhotoImage(file = f"imagens/img_textBox2.png")
entry2_bg = canvas.create_image(
    517.0, 340.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry2.place(
    x = 377, y = 324,
    width = 280,
    height = 31)

entry3_img = PhotoImage(file = f"imagens/img_textBox3.png")
entry3_bg = canvas.create_image(
    517.0, 388.5,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry3.place(
    x = 377, y = 372,
    width = 280,
    height = 31)

entry4_img = PhotoImage(file = f"imagens/img_textBox4.png")
entry4_bg = canvas.create_image(
    517.0, 436.5,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry4.place(
    x = 377, y = 420,
    width = 280,
    height = 31)

window.resizable(False, False)
window.mainloop()
