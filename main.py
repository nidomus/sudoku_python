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

from widgets.celula import Celula

# FUNDO_1 = "#DED9C3"
FUNDO_1 = "white"

# COR_1 = "#8A8771"
COR_1 = "#344861"

FONTE_1 = 30
FONTE_2 = 20


class App():
    def __init__(self, master: tk.Tk) -> None:

        self.master = master

        self.master.bind('<Key>', self.alterar_valor)
        self.master.bind('<F1>', self.ativar_anotacoes)
        self.selecao: Celula = None
        self.quad_selecao = None
        self.coord_selecao = None
        self.quadrantes_botoes = []
        self.erros = 0
        self.espacos_preenchidos = 0
        self.modo_anotacao = False

        self.tabuleiro = Tabuleiro()
        self.tabuleiro.gerar_jogo()
        # self.tabuleiro.zerar_quadrantes()

        self.tabuleiro_backup = copy.deepcopy(self.tabuleiro)

        self.renderizar_tabuleiro()

        self.menu = tk.Menu(self.master, font=("", FONTE_2))

        self.menu_jogo = tk.Menu(self.menu, tearoff=0)

        self.menu_jogo.add_command(
            label="Novo Tabuleiro", font=("", 12), command=self.novo_jogo)

        self.menu_jogo.add_command(
            label="Reiniciar", font=("", 12), command=self.reiniciar_jogo)

        self.menu_jogo.add_command(
            label="Resolver (Beta)", font=("", 12), command=self.resolver_jogo)

        self.menu_ajuda = tk.Menu(self.menu, tearoff=0)

        self.menu.add_cascade(label="Tabuleiro", font=(
            'Arial', FONTE_2), menu=self.menu_jogo)

        self.menu.add_cascade(label="Ajuda", font=(
            'Arial', FONTE_2), menu=self.menu_ajuda)

        self.menu.add_cascade(label="Sobre", font=(
            'Arial', FONTE_2), menu=self.menu_ajuda)

        self.menu.add_command(label="Modo anotação (F1)", font=(
            'Arial', FONTE_2), command=lambda: self.ativar_anotacoes(None))

        self.menu.add_separator()

        self.master.config(menu=self.menu)

    def renderizar_tabuleiro(self):
        self.container = tk.Frame(
            self.master, background=COR_1, cursor='hand2')
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
                        btn: Celula = Celula(
                            frame_btns)
                        botoes.append(btn)
                        btn.bind_all('<Button-1>', lambda event, btn=btn, coord=(i, j),
                                     quad=frame_quad: self.selecionado(btn, coord, quad))
                        btn.bind_all('<Button-3>', lambda event, btn=btn, coord=(i, j), quad=frame_quad: Popup_numeros(
                            root=self.master, app=self, btn=btn, coord=coord, quad=quad))
                        btn.bind_all('<Button-2>', lambda event, btn=btn, coord=(i, j),
                                     quad=frame_quad: self.limpar_valor(event, btn, coord, quad))
                    else:
                        btn: Celula = Celula(
                            master=frame_btns, valor=matriz[i][j], cor_valor=COR_1)
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
                        btn: Celula = Celula(
                            frame_btns)
                        botoes.append(btn)
                        btn.bind_all('<Button-1>', lambda event, btn=btn, coord=(i, j),
                                     quad=frame_quad: self.selecionado(btn, coord, quad))
                        btn.bind_all('<Button-3>', lambda event, btn=btn, coord=(i, j), quad=frame_quad: Popup_numeros(
                            root=self.master, app=self, btn=btn, coord=coord, quad=quad))
                        btn.bind_all('<Button-2>', lambda event, btn=btn, coord=(i, j),
                                     quad=frame_quad: self.limpar_valor(event, btn, coord, quad))
                    else:
                        btn: Celula = Celula(
                            master=frame_btns, valor=matriz[i][j], cor_valor=COR_1)
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
                        btn: Celula = Celula(
                            frame_btns)
                        botoes.append(btn)
                        btn.bind_all('<Button-1>', lambda event, btn=btn, coord=(i, j),
                                     quad=frame_quad: self.selecionado(btn, coord, quad))
                        btn.bind_all('<Button-3>', lambda event, btn=btn, coord=(i, j), quad=frame_quad: Popup_numeros(
                            root=self.master, app=self, btn=btn, coord=coord, quad=quad))
                        btn.bind_all('<Button-2>', lambda event, btn=btn, coord=(i, j),
                                     quad=frame_quad: self.limpar_valor(event, btn, coord, quad))
                    else:
                        btn: Celula = Celula(
                            master=frame_btns, valor=matriz[i][j], cor_valor=COR_1)
                        botoes.append(btn)
                    btn.pack(side=LEFT)

                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)

    def ativar_anotacoes(self, event):
        self.modo_anotacao = not self.modo_anotacao

        if self.modo_anotacao:
            self.container.config(cursor='pencil')
        else:
            self.container.config(cursor='hand2')

    def selecionado(self, btn, coord, quad):
        if self.selecao is not None:
            if self.selecao.label_valor['text'] != '':
                self.restaurar_botoes_invalidos(int(self.selecao.label_valor['text']), int(
                    self.quad_selecao['class']), int(self.coord_selecao[0]), int(self.coord_selecao[1]))

            self.selecao.alterar_fundo('white')

        self.selecao = btn
        self.quad_selecao = quad
        self.coord_selecao = coord

        if self.selecao.label_valor['text'] != '':
            self.alterar_botoes_invalidos(
                int(self.selecao.label_valor['text']))

        if self.selecao.label_valor['foreground'] != 'red':
            self.selecao.alterar_fundo('#B0DBEE')
        else:
            self.selecao.alterar_fundo('#FA9F85')

    def alterar_valor(self, event):

        if not self.modo_anotacao:
            quad = int(self.quad_selecao['class'])
            linha, coluna = self.coord_selecao
            if event.char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:

                self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = int(
                    event.char)
                if self.selecao.label_valor['text'] != '':
                    # print(self.selecao['text']).label_valor
                    self.restaurar_botoes_invalidos(
                        int(self.selecao.label_valor['text']), quad, linha, coluna)

                self.alterar_botoes_invalidos(int(event.char))

                self.selecao.label_valor.configure(text=event.char,)
                self.espacos_preenchidos += 1
                print(self.espacos_preenchidos)

            if event.keycode == 8:
                valor = int(self.selecao.label_valor['text'])
                self.selecao.label_valor.configure(
                    text='', fg='black')
                self.selecao.alterar_fundo('#B0DBEE')
                self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = 0
                self.restaurar_botoes_invalidos(valor, quad, linha, coluna)

        else:
            if event.keycode == 8:
                self.selecao.limpar_anotacoes()
            else:
                self.selecao.fazer_anotacao(int(event.char))

    def alterar_valor_popup(self, event, valor):

        if not self.modo_anotacao:

            quad = int(self.quad_selecao['class'])
            linha, coluna = self.coord_selecao

            self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = valor
            if self.selecao.label_valor['text'] != '':
                print(self.selecao.label_valor['text'])
                self.restaurar_botoes_invalidos(
                    int(self.selecao.label_valor['text']), quad, linha, coluna)

            self.alterar_botoes_invalidos(valor)
            self.selecao.label_valor.configure(text=valor,)

            self.espacos_preenchidos += 1
            print(self.espacos_preenchidos)

        else:
            self.selecao.fazer_anotacao(int(valor))

    def limpar_valor(self, event, btn, coord, quad):

        if self.modo_anotacao:
            btn.limpar_anotacoes()

        else:
            linha, coluna = coord
            valor = int(btn.label_valor['text'])
            btn.label_valor.configure(text='', fg='black')
            self.tabuleiro.quadrantes[int(
                quad['class'])].matriz[linha][coluna] = 0
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
            self.selecao.alterar_fundo('#FA9F85',)
            self.selecao.label_valor.configure(fg='red')
            for q, i, j in posicoes_invalidas:
                self.quadrantes_botoes[q][i][j].label_valor.configure(
                    fg='red', disabledforeground='red',)
                self.quadrantes_botoes[q][i][j].alterar_fundo(
                    '#FA9F85')
        else:
            self.selecao.label_valor.configure(fg='black')
            self.selecao.alterar_fundo('#B0DBEE')

    def restaurar_botoes_invalidos(self, valor, quad, linha, coluna):

        coords = []

        # Retira as marcações de erro do botão atual
        for q, i, j in self.tabuleiro.encontrar_valores_invalidos(quad, valor, linha, coluna):
            botao = self.quadrantes_botoes[q][i][j]
            cor_de_fundo = 'white'
            if botao.label_valor['state'] == 'disabled':
                cor_de_fundo = FUNDO_1
            else:
                coords.append((q, i, j))
            botao.label_valor.configure(
                fg=COR_1, disabledforeground=COR_1)
            botao.alterar_fundo(cor_de_fundo)

        # Verifica se alguma casa continua inválida mesmo após apagar o botão principal
        for coord in coords:
            quadrante, i, j = coord
            posicoes = self.tabuleiro.encontrar_valores_invalidos(
                quadrante, valor, i, j)

            # Se sim, mantém o texto em vermelho
            if len(posicoes) > 0:
                self.quadrantes_botoes[quadrante][i][j].label_valor.configure(
                    fg='red',)

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

icone = resource_filename(__name__, './assets/icon.ico')
root.iconbitmap(icone)
root.title('Sudoku!')
root.mainloop()
