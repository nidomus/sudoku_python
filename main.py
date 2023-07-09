import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from classes.tabuleiro import Tabuleiro
from pkg_resources import resource_filename
import copy
from classes.quadrante import BlockedException
import time
from queue import Queue
from threading import Thread
from widgets.popup_numero import Popup_numeros

# FUNDO_1 = "#DED9C3"
FUNDO_1 = "white"

# COR_1 = "#8A8771"
COR_1 = "#344861"

FONTE_1 = 30
FONTE_2 = 20


class T_resolve(Thread):
    def __init__(self, tabuleiro, queue):
        Thread.__init__(self)
        self.tabuleiro = tabuleiro
        self.queue = queue
        # self.tabuleiro_copia = copy.deepcopy(tabuleiro)

    def run(self):
        global flag
        global t
        flag = False
        quadrantes_copia = copy.deepcopy(self.tabuleiro.quadrantes)
        try:
            while flag == False:
                flag = True
                self.tabuleiro.quadrantes = copy.deepcopy(quadrantes_copia)
                for i in range(len(self.tabuleiro.quadrantes)):
                    try:
                        self.tabuleiro.quadrantes[i].resolver_quadrante()
                    except BlockedException:
                        i -= 2
                        print(i)

        finally:
            self.queue.put(self.tabuleiro)
            self.queue.task_done()
            print(self.name)


class App():
    def __init__(self, master: tk.Tk) -> None:

        self.master = master

        self.master.bind('<Key>', self.alterar_valor)
        self.selecao = None
        self.quad_selecao = None
        self.coord_selecao = None
        self.quadrantes_botoes = []
        self.erros = 0
        self.espacos_preenchidos = 0

        self.tabuleiro = Tabuleiro()
        self.tabuleiro.gerar_jogo()
        # self.tabuleiro.zerar_quadrantes()

        self.tabuleiro_backup = copy.deepcopy(self.tabuleiro)

        self.renderizar_tabuleiro()

        print(len(self.quadrantes_botoes))

    def renderizar_tabuleiro(self):
        self.container = tk.Frame(self.master, background=COR_1)
        self.container.pack(fill=BOTH, expand=YES)
        # ttk.Separator(master=self.master,orient=HORIZONTAL).pack(side = TOP,fill=X, pady=(5,0), padx=10)
        self.frame_1 = tk.Frame(self.container, background=COR_1)
        self.frame_1.pack(side=TOP, pady=(6, 2), padx=2, expand=YES)
        # ttk.Separator(master=self.master,orient=HORIZONTAL).pack(side = TOP,fill=X, pady=10, padx=10)
        self.frame_2 = tk.Frame(self.container, background=COR_1)
        self.frame_2.pack(side=TOP, pady=2, padx=2, expand=YES)
        # ttk.Separator(master=self.master,orient=HORIZONTAL).pack(side = TOP,fill=X, pady=10, padx=10)
        self.frame_3 = tk.Frame(self.container, background=COR_1)
        self.frame_3.pack(side=TOP, pady=(2, 6), padx=2, expand=YES)
        # ttk.Sep, background='black'arator(master=self.master,orient=HORIZONTAL).pack(side = TOP,fill=X, pady=2, padx=10)

        self.frame_botoes = tk.Frame(self.container, background=COR_1)
        self.frame_botoes.pack(side='top', pady=(20, 0), expand=YES, fill=X)

        self.botao_reiniciar = tk.Button(self.frame_botoes, text='Reiniciar', font=(
            'Arial', FONTE_2), fg=COR_1, command=self.reiniciar_jogo)
        self.botao_reiniciar.pack(side=LEFT, padx=5, pady=5)

        self.botao_novo_jogo = tk.Button(self.frame_botoes, text='Novo Jogo', font=(
            'Arial', FONTE_2), fg=COR_1, command=self.novo_jogo)
        self.botao_novo_jogo.pack(side=RIGHT, padx=5, pady=5)

        self.botao_resolver = tk.Button(self.frame_botoes, text='Resolver', font=(
            'Arial', FONTE_2), fg=COR_1, command=self.resolver_jogo)
        self.botao_resolver.pack(side=RIGHT, padx=5, pady=5)

        for q in range(3):
            matriz = self.tabuleiro.quadrantes[q].matriz
            frame_quad = tk.Frame(self.frame_1, class_=q)
            frame_quad.pack(side=LEFT, padx=(2))
            matriz_botoes = []
            for i in range(3):
                frame_btns = tk.Frame(frame_quad,)
                frame_btns.pack(side=TOP,)
                botoes = []
                for j in range(3):
                    valor = matriz[i][j]
                    if valor == 0:
                        btn = tk.Button(
                            frame_btns, text='  ', background='white', width=3, font=('Arial', FONTE_1))
                        botoes.append(btn)
                        btn.bind('<Button-1>', lambda event, btn=btn, coord=(i, j),
                                 quad=frame_quad: self.selecionado(btn, coord, quad))
                        btn.bind('<Button-3>', lambda event, btn=btn, coord=(i, j), quad=frame_quad: Popup_numeros(
                            root=self.master, app=self, btn=btn, coord=coord, quad=quad))
                        btn.bind('<Button-2>', lambda event, btn=btn, coord=(i, j),
                                 quad=frame_quad: self.limpar_valor(event, btn, coord, quad))
                    else:
                        btn = tk.Button(frame_btns, text=matriz[i][j], state='disabled', bg=FUNDO_1,
                                        width=3, disabledforeground=COR_1, font=('Arial', FONTE_1))
                        botoes.append(btn)
                    btn.pack(side=LEFT)
                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)

        for q in range(3, 6):
            matriz = self.tabuleiro.quadrantes[q].matriz
            frame_quad = tk.Frame(self.frame_2, class_=q)
            frame_quad.pack(side=LEFT, padx=(2))
            matriz_botoes = []

            for i in range(3):
                frame_btns = tk.Frame(frame_quad)
                frame_btns.pack(side=TOP,)
                botoes = []
                for j in range(3):
                    valor = matriz[i][j]
                    if valor == 0:
                        btn = tk.Button(
                            frame_btns, text='  ', background='white', width=3, font=('Arial', FONTE_1))
                        botoes.append(btn)
                        btn.bind('<Button-1>', lambda event, btn=btn, coord=(i, j),
                                 quad=frame_quad: self.selecionado(btn, coord, quad))
                        btn.bind('<Button-3>', lambda event, btn=btn, coord=(i, j), quad=frame_quad: Popup_numeros(
                            root=self.master, app=self, btn=btn, coord=coord, quad=quad))
                        btn.bind('<Button-2>', lambda event, btn=btn, coord=(i, j),
                                 quad=frame_quad: self.limpar_valor(event, btn, coord, quad))

                    else:
                        btn = tk.Button(frame_btns, text=matriz[i][j], state='disabled', width=3,
                                        bg=FUNDO_1, disabledforeground=COR_1, font=('Arial', FONTE_1))
                        botoes.append(btn)
                    btn.pack(side=LEFT)

                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)

        for q in range(6, 9):
            matriz = self.tabuleiro.quadrantes[q].matriz
            frame_quad = tk.Frame(self.frame_3, class_=q)
            frame_quad.pack(side=LEFT, padx=(2))
            matriz_botoes = []

            for i in range(3):
                frame_btns = tk.Frame(frame_quad)
                frame_btns.pack(side=TOP,)
                botoes = []
                for j in range(3):
                    valor = matriz[i][j]
                    if valor == 0:
                        btn = tk.Button(
                            frame_btns, text='  ', background='white', width=3, font=('Arial', FONTE_1))
                        botoes.append(btn)
                        btn.bind('<Button-1>', lambda event, btn=btn, coord=(i, j),
                                 quad=frame_quad: self.selecionado(btn, coord, quad))
                        btn.bind('<Button-3>', lambda event, btn=btn, coord=(i, j), quad=frame_quad: Popup_numeros(
                            root=self.master, app=self, btn=btn, coord=coord, quad=quad))
                        btn.bind('<Button-2>', lambda event, btn=btn, coord=(i, j),
                                 quad=frame_quad: self.limpar_valor(event, btn, coord, quad))

                    else:
                        btn = tk.Button(frame_btns, text=matriz[i][j], state='disabled', bg=FUNDO_1,
                                        width=3, disabledforeground=COR_1, font=('Arial', FONTE_1))
                        botoes.append(btn)

                    btn.pack(side=LEFT, fill=BOTH)

                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)

    def selecionado(self, btn, coord, quad):
        if self.selecao is not None:
            if self.selecao['text'] != '  ':
                self.restaurar_botoes_invalidos(int(self.selecao['text']), int(
                    self.quad_selecao['class']), int(self.coord_selecao[0]), int(self.coord_selecao[1]))
            self.selecao.configure(bg='white')

        self.selecao = btn
        self.quad_selecao = quad
        self.coord_selecao = coord

        if self.selecao['text'] != '  ':
            self.alterar_botoes_invalidos(int(self.selecao['text']))

        if self.selecao['foreground'] != 'red':
            self.selecao.configure(bg='#B0DBEE')
        else:
            self.selecao.configure(bg='#FA9F85')

    def alterar_valor(self, event):
        quad = int(self.quad_selecao['class'])
        linha, coluna = self.coord_selecao
        if event.char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:

            self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = int(
                event.char)
            if self.selecao['text'] != '  ':
                print(self.selecao['text'])
                self.restaurar_botoes_invalidos(
                    int(self.selecao['text']), quad, linha, coluna)

            self.alterar_botoes_invalidos(int(event.char))

            self.selecao.configure(text=event.char,)
            self.espacos_preenchidos += 1
            print(self.espacos_preenchidos)

        if event.keycode == 8:
            valor = int(self.selecao['text'])
            self.selecao.configure(text='  ', bg='#B0DBEE', fg='black')
            self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = 0
            self.restaurar_botoes_invalidos(valor, quad, linha, coluna)

    def alterar_valor_popup(self, event, valor):
        quad = int(self.quad_selecao['class'])
        linha, coluna = self.coord_selecao

        self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = valor
        if self.selecao['text'] != '  ':
            print(self.selecao['text'])
            self.restaurar_botoes_invalidos(
                int(self.selecao['text']), quad, linha, coluna)

        self.alterar_botoes_invalidos(valor)
        self.selecao.configure(text=valor,)

        self.espacos_preenchidos += 1
        print(self.espacos_preenchidos)

    def limpar_valor(self, event, btn, coord, quad):

        linha, coluna = coord
        valor = int(btn['text'])
        btn.configure(text='  ', fg='black')
        self.tabuleiro.quadrantes[int(quad['class'])].matriz[linha][coluna] = 0
        self.restaurar_botoes_invalidos(
            valor, int(quad['class']), linha, coluna)
        self.selecionado(btn, coord, quad)

    def alterar_botoes_invalidos(self, valor):
        quad = int(self.quad_selecao['class'])
        linha, coluna = self.coord_selecao
        posicoes_invalidas = self.tabuleiro.encontrar_valores_invalidos(
            quad, valor, linha, coluna)
        if len(posicoes_invalidas) > 0:
            self.erros += 1
            self.selecao.configure(fg='red', bg='#FA9F85',)
            for q, i, j in posicoes_invalidas:
                self.quadrantes_botoes[q][i][j].configure(
                    fg='red', disabledforeground='red', bg='#FA9F85')
        else:
            self.selecao.configure(fg='black', bg='#B0DBEE')

    def restaurar_botoes_invalidos(self, valor, quad, linha, coluna):

        coords = []

        # Retira as marcações de erro do botão atual
        for q, i, j in self.tabuleiro.encontrar_valores_invalidos(quad, valor, linha, coluna):
            botao = self.quadrantes_botoes[q][i][j]
            cor_de_fundo = 'white'
            if botao['state'] == 'disabled':
                cor_de_fundo = FUNDO_1
            else:
                coords.append((q, i, j))
            botao.configure(
                fg='black', disabledforeground=COR_1, bg=cor_de_fundo)

        # Verifica se alguma casa continua inválida mesmo após apagar o botão principal
        for coord in coords:
            quadrante, i, j = coord
            posicoes = self.tabuleiro.encontrar_valores_invalidos(
                quadrante, valor, i, j)

            # Se sim, mantém o texto em vermelho
            if len(posicoes) > 0:
                self.quadrantes_botoes[quadrante][i][j].configure(fg='red',)

    def resolver_jogo(self):

        self.tabuleiro = copy.deepcopy(self.tabuleiro_backup)
        self.tabuleiro.print_tabuleiro()
        # self.tabuleiro.resolver_jogo()
        tempo_inicial = time.time()
        # self.queue = Queue()
        # for _ in range(1):

        #     tabuleiro = copy.deepcopy(self.tabuleiro)
        #     trabalhador = T_resolve(tabuleiro, self.queue)
        #     trabalhador.name = f't{_}'
        #     trabalhador.daemon = True
        #     trabalhador.start()

        self.tabuleiro.resolver_jogo()
        # self.queue.join()
        # self.tabuleiro = self.queue.get()

        tempo_final = time.time()

        print(tempo_final-tempo_inicial)

        self.container.destroy()
        self.renderizar_tabuleiro()

        # for i in range(9):
        #     for linha in range(3):
        #         for coluna in range(3):
        #             valor = self.tabuleiro.quadrantes[i].matriz[linha][coluna]
        #             self.quadrantes_botoes[i][linha][coluna].configure(text=valor, state = 'disabled', bg='white')
        #             self.quadrantes_botoes[i][linha][coluna].unbind('<Button-1>')

    def reiniciar_jogo(self):

        # Reseta os atributos de controle
        self.selecao = None
        self.quad_selecao = None
        self.coord_selecao = None
        self.quadrantes_botoes = []
        self.erros = 0
        self.espacos_preenchidos = 0

        # Recupera a cópia do tabuleiro
        self.tabuleiro = copy.deepcopy(self.tabuleiro_backup)

        # Destrói o container principal
        self.container.destroy()

        # Renderiza o tabuleiro novamente
        self.renderizar_tabuleiro()

    def novo_jogo(self):

        # Reseta os atributos de controle
        self.selecao = None
        self.quad_selecao = None
        self.coord_selecao = None
        self.quadrantes_botoes = []
        self.erros = 0
        self.espacos_preenchidos = 0

        # Cria um novo tabuleiro
        self.tabuleiro = Tabuleiro()
        self.tabuleiro.gerar_jogo()

        # Destrói o container principal
        self.container.destroy()

        # Renderiza o tabuleiro novamente
        self.renderizar_tabuleiro()


root = tk.Tk()

app = App(root)
root.resizable(0, 0)

# root.geometry('720x720')
root.eval('tk::PlaceWindow . center')

icone = resource_filename(__name__, 'icon.ico')
root.iconbitmap(icone)
root.title('Sudoku!')
root.mainloop()
