from tkinter import *
from tkinter import Tk,ttk, messagebox
from tkcalendar import Calendar,DateEntry
from collections import Counter
import random
from datetime import datetime
import sqlite3


#dicionários de fontes e cores
st_f = {'f1':('M Hei PRC', 10, 'bold'),'f2':('Helvetica', 8,'bold','italic'),'f3':('Helvetica', 10, 'bold'),'f4':("Helvetica", 12, "bold"),'f5':('Helvetica', 7, 'italic'),'f6':('New', 9),'f7':('Arial', 10, 'bold')}

#DICIONÁRIO DE CORES USADAS DENTRO DO PROGRAMA.
# C REPRESENTA CORES
		#CORES	LARANJA			BRANCO		 AZUL ESCURO	AZUL CEU	  VERDE			VERMELHO
c = {'br':'#FFFFFF','rx':'#893880', 'az':'#0f4d87','bk':'black','cz':'#EEEEEE','czc':'#f7f7f7'}
root = Tk()
#criando a class que executará a tela da aplicação 


class Conection():
    def __init__(self):
        self.conn = sqlite3.connect('venv\\Lib\\site-packages\\.it\\.it1\\sqlite\\s_db\\sher_db\\.MegaData.db')
        self.cursor = self.conn.cursor()
        # Inicializar variáveis para armazenar os dados do concurso

conexao = Conection()


class Functions():
    def __init__(self):
        pass
    
    def ultimo_concurso(self):
        conexao.cursor.execute("SELECT * FROM MAX_CONCURSO")
        self.resu = conexao.cursor.fetchall()
        return self.resu
    
    def acao_bt_Registrar(self):
        valor_concurso = self.concurso.get()
        valor_data_ptbr = self.data_conc.get()
        valor_data = datetime.strptime(valor_data_ptbr, "%d/%m/%Y").strftime("%y-%m-%d")
        valor_numero = self.entry_num.get()
        valor_premio = self.premio.get() if self.premio is not None else None

        try:
            if valor_premio is not None:
                conexao.cursor.execute("INSERT INTO HIST_MEGA_SENA (CONCURSO, DATA_CONCURSO, APOSTA, VENCEDOR, PREMIO) \
                                    VALUES (?, ?, ?, ?, ?)", (valor_concurso, valor_data, valor_numero, "Ganhadora", valor_premio))
            else:
                conexao.cursor.execute("INSERT INTO HIST_MEGA_SENA (CONCURSO, DATA_CONCURSO, APOSTA) \
                                    VALUES (?, ?, ?)", (valor_concurso, valor_data, valor_numero))
            conexao.conn.commit()
            messagebox.showinfo("Sucesso!", f"Dados do concurso '{valor_concurso}' cadastrados com sucesso!")
        except Exception as e:
            print(e)
            messagebox.showerror("Erro!", f"Erro ao tentar inserir os dados.\n{e}")

    def bt_update(self):
        valor_concurso = self.concurso.get()
        valor_data_ptbr = self.data_conc.get()
        valor_data = datetime.strptime(valor_data_ptbr, "%d/%m/%Y").strftime("%y-%m-%d")
        valor_numero = self.entry_num.get()
        valor_premio = self.premio.get() if self.premio is not None else None

        try:
            if valor_premio is not None:
                conexao.cursor.execute(f"UPDATE HIST_MEGA_SENA SET  \
                                     {valor_concurso}, {valor_data}, {valor_numero}, 'Ganhadora', {valor_premio}\
                                        WHERE CONCURSO = {valor_concurso}")
            else:
                conexao.cursor.execute(f"UPDATE HIST_MEGA_SENA SET  \
                                     {valor_concurso}, {valor_data}, {valor_numero}\
                                        WHERE CONCURSO = {valor_concurso}")
            conexao.conn.commit()
            messagebox.showinfo("Sucesso!", f"Dados do concurso '{valor_concurso}' foram alterados com sucesso!")
        except Exception as e:
            print(e)
            messagebox.showerror("Erro!", f"Erro ao tentar alterar os dados.\n{e}")

    # Lógica das escolhas do ComboBox
    def combobox_selected(self, event):
        self.selected_option = self.options.get()
        if self.selected_option == "Sim":
            self.show_entry()
        elif self.selected_option == "Não":
            self.hide_entry()

    # Lógica das escolhas do ComboBox
    def combobox_selected(self, event):
        self.selected_option = self.options.get()
        if self.selected_option == "Sim":
            self.show_entry()
        elif self.selected_option == "Não":
            self.hide_entry()

    # Essa função mostra o campo de entrada que recebe o valor premiado no concurso apenas quando o ComboBox chama a opção "Sim"
    def show_entry(self, event=None):
        if self.options.get() == "Sim":
            self.show_label(True)
            self.premio = Entry(self.fm_baixo)
            self.premio.place_configure(x=20, y=118, width=175, height=25)
        else:
            self.show_label(False)
            pass

    # Função que esconde o campo de entrada que recebe o valor premiado no concurso e o rótulo apenas quando o ComboBox chama a opção "Não"
    def hide_entry(self):
        if self.options.get() == "Não" and self.premio is not None:
            self.show_label(False)
            self.premio.place_forget()
            self.premio = None

    # Função para mostrar ou esconder o rótulo
    def show_label(self, show):
        if show:
            self.lb_config = Label(master=self.fm_baixo, text='Valor Sorteado', font=st_f['f6'])
            self.lb_config.place_configure(x=20, y=95)
        else:
            if self.lb_config is not None:
                self.lb_config.place_forget()
                self.lb_config = None

    def formatar_data_para_exibicao(self,data):
        partes = data.split('-')  # Divide a data em partes usando hífens
        ano = partes[0]  # Os dois últimos dígitos do ano
        mes = partes[1]
        dia = partes[2]
        data_formatada = f"{dia}/{mes}/{ano}"
        return data_formatada

class Aplication(Functions):
    def __init__(self):
        self.root = root
        self.premio = None  # Variável para rastrear o Entry de valor premiado
        self.winConfig()
        self.frames()
        self.windgets_app()
        self.table()
        root.mainloop()
        pass
    def labels(self,master,text,x,y):
        self.lb_config = Label(master=master,text=text,font=st_f['f6'])
        self.lb_config.place_configure(x=x, y=y)
    
    def entrys(self,master,width,height,x,y,**kargs):
        entry = Entry(master=master)
        entry.place_configure(x=x,y=y,width=width,height=height)
        return entry
    
    #Função para todas as configurações da tela
    def winConfig(self):
        self.root.geometry("600x320")
        self.root.config(bg=c['br'])
        self.root.resizable(False,False)# impede que a tela seja maximizada ou minimizada
        #Define que a tela sempre seja criada no meio da tela do computador--------------------------------------------------------------
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        win_width = 600
        win_height = 320
        # Calcula as coordenadas para centralizar a janela
        x = int(screen_width / 2 - win_width / 2)
        y = int(screen_height / 2 - win_height / 1)
        # Define as coordenadas da janela
        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        #--------------------------------------------------------------------------------------------------------------------------------
    #função que cria os frames da tela
    def frames(self):
        self.fm_up = Frame(self.root,bg=c['cz'],width=580, height=42,borderwidth=1, highlightbackground=c['az'], highlightthickness=1)
        self.fm_up.place_configure(x=10,y=2)

        self.fm_superior = Frame(self.root,width=580, height=75,borderwidth=1, highlightbackground=c['az'], highlightthickness=1)
        self.fm_superior.place_configure(x=10,y=55)
        
        self.fm_baixo = Frame(self.root,width=580,height=170,borderwidth=1, highlightbackground=c['az'], highlightthickness=1)
        self.fm_baixo.place_configure(x=10,y=140)
    #Função que cria e exibe todos os Widgets da tela
    def table(self):
        cell_height = 30
        self.style_tb = ttk.Style()
        self.style_tb.theme_use('clam')
            # self.style_tb.configure("Treeview", rowheight=cell_height)
        self.style_tb.configure('Treeview',rowheight=cell_height,
                             fieldbackground=c['br'],
                             background=c['br'],
                             foreground=c['az'],
                             arrowcolor=c['br'],
                     				)  # Define a altura mínima da linha
        self.style_tb.configure("Treeview.Heading", font=st_f['f3'], foreground=c['az'])# Define a fonte do cabeçalho
        resultado = self.ultimo_concurso()
        #Itera pelos valores retornados pela query da função ultimo concurso e armazena os valores retornados em variáveis
        self.Coldata = ('CONCURSO','DATA','APOSTA','VENCEDOR','PREMIO')
        self.tree = ttk.Treeview(master=self.fm_superior,height=1,columns=(self.Coldata),show='headings',selectmode='browse')
        self.tree.place_configure(x=5,y=7,width=570)
        # self.tree.column("#0", width=0, anchor='center')
        self.tree.column("CONCURSO", width=5, anchor='center')
        self.tree.column("DATA", width=10,anchor='center')
        self.tree.column("APOSTA", width=10,anchor='center')
        self.tree.column("VENCEDOR", width=10,anchor='center')
        self.tree.column("PREMIO", width=10,anchor='center')
        # self.tree.tag_configure("gray", background='lightgray')
        self.tree.tag_configure("normal", background='gray')

        self.tree.heading("#0", text="ID", anchor=W)
        for col in self.Coldata:
                self.tree.heading(col, text=col, anchor=CENTER)

        # Preencher o Treeview com os dados, formatando a data
        for row in resultado:
            formatted_date = self.formatar_data_para_exibicao(row[1])
            formatted_row = row[:1] + (formatted_date,) + row[2:]
            self.tree.insert('', 'end', values=formatted_row)
    
    def windgets_app(self):
        #cria o stilo do DataEntry
        self.style = ttk.Style()
        self.style.configure('my.DataEntry.TButton',
                fieldbackground=c['br'],
                background=c['br'],
                foreground=c['az'],
                arrowcolor=c['br']
                )
        self.style.configure("my.DataEntry.TButton", font=st_f['f3'], foreground=c['az'],background=c['az'])# Define a fonte do cabeçalho
        # #widgets frame de cima
        # self.labels(master=self.fm_superior,text=self.n_conc,x=20,y=15)

        self.labels(master=self.fm_baixo,text='Nº Concurso',x=20, y=15)
        self.concurso = self.entrys(master=self.fm_baixo,x=20, y=35, width=100,height=25)
        
        # self.entry_concurso = Entry(self.fm_baixo)
        # self.entry_concurso.place_configure(x=20, y=35, width=100,height=25)

        self.labels(master=self.fm_baixo,text='Data',x=150, y=15)
        self.data_conc = DateEntry(self.fm_baixo,style='my.DataEntry.TButton',width=12,locale='pt_br',font=st_f['f6'])
        self.data_conc.place_configure(x=150, y=35, height=27)

        self.bt_registrar = Button(self.fm_baixo,text="Registrar",fg=c['az'],font=st_f['f3'],command=self.acao_bt_Registrar)
        self.bt_registrar.place_configure(x=370, y=118, width=90, height=25)

        self.bt_alterar = Button(self.fm_baixo,text="Alterar",fg="#FF6C22",font=st_f['f3'],command='self.bt_update')
        self.bt_alterar.place_configure(x=480, y=118, width=80, height=25)
    
        self.labels(master=self.fm_baixo,text='Numero sorteado',x=280, y=16)
        self.entry_num = Entry(self.fm_baixo)
        self.entry_num.place_configure(x=280, y=35, width=175,height=25)

        self.labels(master=self.fm_baixo,text='Venceu',x=485, y=16)
        self.options= ttk.Combobox(self.fm_baixo,values=['Sim','Não'])
        self.options.place_configure(x=485, y=35, width=55,height=25)
        self.options.bind("<<ComboboxSelected>>", self.combobox_selected)

if __name__ == "__main__":
    Aplication()


def insert_in_database():
    conn = sqlite3.connect('MegaData.db')
    cursor = conn.cursor()
    # Inicializar variáveis para armazenar os dados do concurso
    concurso = ""
    data_concurso = ""
    apostas = ""
    vencedor = ""

    # Abrir o arquivo de texto
    with open("dados_concursos.txt", "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()  # Remover espaços em branco

            if linha.startswith("Concurso:"):
                # Extrair o número do concurso
                concurso = linha.split("Concurso:")[1].split('-')[0].strip()
                vencedor = "Ganhadora" if "Ganhadora" in linha else ""
            elif linha.startswith("Data:"):
                # Extrair a data do concurso no formato "dd/mm/yyyy"
                data_concurso = linha.split("Data:")[1].strip()
                # Converter para o formato "aaaa-mm-dd" esperado pelo SQL Server
                data_concurso = data_concurso.split("/")
                data_concurso = f"{data_concurso[2]}-{data_concurso[1]}-{data_concurso[0]}"
            elif linha.startswith("Aposta:"):
                # Extrair a sequência de números da aposta
                apostas = linha.split("Aposta:")[1].strip()

                # Inserir os dados no banco de dados quando todas as informações estiverem disponíveis
                if concurso and data_concurso and apostas:
                    try:
                        # Inserir os dados na tabela do banco de dados
                        cursor.execute("INSERT INTO HIST_MEGA_SENA (Concurso, Data_concurso, Aposta, Vencedor) VALUES (?, ?, ?, ?)",
                                    (concurso, data_concurso, apostas, vencedor))
                        conn.commit()
                        # Limpar as variáveis
                        concurso = ""
                        data_concurso = ""
                        apostas = ""
                        vencedor = ""
                    except Exception as e:
                        print("Erro", str(e))

    # Fechar a conexão com o banco de dados
    cursor.close()

def gerador_de_num():


    # Lista para armazenar os números das apostas ganhadoras
    numeros_apostas_ganhadoras = []

    # Abre o arquivo para leitura
    with open('dados_concursos.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        # Remove espaços em branco no início e no final da linha
        linha = linha.strip()
        
        if linha.startswith("Aposta:") and "Ganhadora" in linha:
            # Divide a linha da aposta em números separados
            numeros = [int(num) for num in linha.split(": ")[1].split("-")]
            numeros_apostas_ganhadoras.extend(numeros)

    # Conta a frequência de cada número nas apostas ganhadoras
    contagem_numeros = Counter(numeros_apostas_ganhadoras)

    # Encontre os 6 números mais frequentes
    seis_mais_frequentes = [numero for numero, _ in contagem_numeros.most_common(6)]

    # Gere um jogo baseado nos 6 números mais frequentes
    jogo = random.choices(seis_mais_frequentes, k=6)

    print("Os 6 números mais frequentes nas apostas ganhadoras são:", seis_mais_frequentes)
    print("Seu jogo gerado com base nesses números é:", jogo)

