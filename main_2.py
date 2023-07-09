import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tabuleiro import Tabuleiro
from pkg_resources import resource_filename
from threading import Thread,enumerate
import copy
from quadrante import BlockedException
import time
from queue import Queue

class T_resolve(Thread):
    def __init__(self, tabuleiro,queue):
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
                for quadrante in self.tabuleiro.quadrantes:
                    try:
                        quadrante.resolver_quadrante()       
                    except BlockedException:
                        flag = False
                        break
        finally:
            self.queue.put(self.tabuleiro)
            self.queue.task_done()
            print(self.name)
class App():
    def __init__(self, master) -> None:
        
        self.master = master
        self.master.bind('<Key>' , self.alterar_valor)
        self.selecao = None
        self.quad_selecao = None
        self.coord_selecao = None
        self.quadrantes_botoes = []
        #8A8771
        self.container = tk.Frame(self.master, background='#8A8771')
        self.container.pack(fill=BOTH,expand=YES)

        self.frame_1 = tk.Frame(self.container, background='#8A8771')
        self.frame_1.pack(side=TOP,pady=(6,3),padx = 3,fill = BOTH, expand=YES)

        self.frame_2 = tk.Frame(self.container, background='#8A8771')
        self.frame_2.pack(side= TOP,pady = 3,padx = 3,fill = BOTH, expand=YES)

        self.frame_3 = tk.Frame(self.container, background='#8A8771')
        self.frame_3.pack(side= TOP, pady=(3,6),padx = 3,fill = BOTH, expand=YES)
        
        self.frames_botoes = tk.Frame(self.container,background='#8A8771')
        self.frames_botoes.pack()

        self.btn_resolver = tk.Button(self.frames_botoes, text= 'Resolver', font= ('Arial',35),command= lambda: Thread(target=self.resolver_jogo).start())
        self.btn_resolver.pack()

        self.tabuleiro = Tabuleiro()
        self.tabuleiro.zerar_quadrantes()
        # self.tabuleiro.gerar_jogo()


        for q in range(3):
            matriz = self.tabuleiro.quadrantes[q].matriz
            frame_quad = tk.Frame(self.frame_1, class_=q)
            frame_quad.pack(side=LEFT,padx=(3))
            matriz_botoes= []
            # ttk.Separator(master=frame_quad,orient=VERTICAL).pack(side = LEFT,fill=Y, padx=10)
            for i in range(3):
                frame_btns = tk.Frame(frame_quad,)
                frame_btns.pack(side=TOP,)
                botoes = []
                for j in range(3):
                    valor = matriz[i][j]

                    btn = tk.Button(frame_btns , text='  ',width=3,background='white', font= ('Arial',35))
                    botoes.append(btn)
                    btn.bind('<Button-1>', lambda event, btn = btn,coord = (i,j),quad = frame_quad  : self.selecionado(btn,coord,quad))
                    btn.pack(side=LEFT)

                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)

        
        for q in range(3,6):
            matriz = self.tabuleiro.quadrantes[q].matriz
            frame_quad = tk.Frame(self.frame_2,class_=q)
            frame_quad.pack(side=LEFT,padx=(3))
            matriz_botoes = []
            # ttk.Separator(master=frame_quad,orient=VERTICAL).pack(side = LEFT,fill=Y, padx=10)
            for i in range(3):
                frame_btns = tk.Frame(frame_quad)
                frame_btns.pack(side=TOP,)
                botoes = []
                for j in range(3):
                    valor = matriz[i][j]
 
                    btn = tk.Button(frame_btns,background='white',text='  ',width=3, font= ('Arial',35))
                    botoes.append(btn)
                    btn.bind('<Button-1>', lambda event, btn = btn,coord = (i,j),quad = frame_quad  : self.selecionado(btn,coord,quad))
                    btn.pack(side=LEFT)

                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)
        for q in range(6,9):
            matriz = self.tabuleiro.quadrantes[q].matriz
            frame_quad = tk.Frame(self.frame_3, class_=q)
            frame_quad.pack(side=LEFT,padx=(3))
            matriz_botoes = []
            # ttk.Separator(master=frame_quad,orient=VERTICAL).pack(side = LEFT,fill=Y, padx=10)
            for i in range(3):
                frame_btns = tk.Frame(frame_quad)
                frame_btns.pack(side=TOP,)
                botoes = []
                for j in range(3):
                    valor = matriz[i][j]

                    btn = tk.Button(frame_btns , text='  ',background='white',width=3, font= ('Arial',35))
                    botoes.append(btn)
                    
                    btn.bind('<Button-1>', lambda event, btn = btn,coord = (i,j),quad = frame_quad  : self.selecionado(btn,coord,quad))
                    btn.pack(side=LEFT)
                
                matriz_botoes.append(botoes)

            self.quadrantes_botoes.append(matriz_botoes)

        print(len(self.quadrantes_botoes))

    def selecionado(self,btn,coord,quad):
        if self.selecao is not None:
            if self.selecao['text'] != '  ':
                self.restaurar_botoes_invalidos(int(self.selecao['text']),int(self.quad_selecao['class']),int(self.coord_selecao[0]),int(self.coord_selecao[1]) )
                self.selecao.configure(bg='#DED9C3')
            else:
                self.selecao.configure(bg='white')


        self.selecao = btn
        self.quad_selecao  = quad
        self.coord_selecao = coord

        if self.selecao['text'] != '  ':
            self.alterar_botoes_invalidos(int(self.selecao['text']))

        if self.selecao['foreground'] != 'red':
            self.selecao.configure(bg ='#B0DBEE')
        else:
            self.selecao.configure(bg ='#FA9F85')           

    def alterar_valor(self,event):
        quad = int(self.quad_selecao['class'])
        linha, coluna = self.coord_selecao
        if event.char in ['1','2','3','4','5','6','7','8','9']:
            
            self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = int(event.char)
            if self.selecao['text'] != '  ':
                print(self.selecao['text'])
                self.restaurar_botoes_invalidos(int(self.selecao['text']),quad,linha,coluna)
            
            self.alterar_botoes_invalidos(int(event.char))

            self.selecao.configure(text = event.char,background='#DED9C3' )
 

        if event.keycode == 8:
            valor = int(self.selecao['text'])
            self.selecao.configure(text = '  ',bg ='#B0DBEE', fg='black')
            self.tabuleiro.quadrantes[quad].matriz[linha][coluna] = 0
            self.restaurar_botoes_invalidos(valor,quad,linha,coluna)

    
    def alterar_botoes_invalidos(self, valor):
        quad = int(self.quad_selecao['class'])
        linha, coluna = self.coord_selecao
        posicoes_invalidas = self.tabuleiro.encontrar_valores_invalidos(quad,valor,linha,coluna)
        if len(posicoes_invalidas)>0:
            self.selecao.configure(fg='red', bg='#FA9F85',)
            for q,i,j in posicoes_invalidas:
                self.quadrantes_botoes[q][i][j].configure(fg='red', disabledforeground='red',bg='#FA9F85')
        else:
            self.selecao.configure(fg= 'black', bg = '#B0DBEE')    

    def restaurar_botoes_invalidos(self,valor,quad,linha,coluna):

        coord = []
        for q,i,j in self.tabuleiro.encontrar_valores_invalidos(quad,valor,linha,coluna):
            botao = self.quadrantes_botoes[q][i][j]
            cor_de_fundo = 'white'
            if botao['state'] == 'disabled':
                cor_de_fundo = '#DED9C3'
            else:
                coord.append((q,i,j))
            botao.configure(fg = 'black',disabledforeground='#8A8771', bg = cor_de_fundo)

        for c in coord:
            q, i, j = c
            posicoes = self.tabuleiro.encontrar_valores_invalidos(q,valor,i,j)
            # print(posicoes)
            if len(posicoes)>0:
                self.quadrantes_botoes[q][i][j].configure(fg='red',)

    def resolver_jogo(self):
        
        self.tabuleiro.print_tabuleiro()
        # self.tabuleiro.resolver_jogo()
        tempo_inicial = time.time()
        self.queue = Queue()
        for _ in range(5):

            tabuleiro = copy.deepcopy(self.tabuleiro)
            trabalhador = T_resolve(tabuleiro,self.queue)
            trabalhador.name=f't{_}'
            trabalhador.daemon = True
            trabalhador.start()

        self.queue.join()
        self.tabuleiro = self.queue.get()

        for i in range(9):
            for linha in range(3):
                for coluna in range(3):
                    valor = self.tabuleiro.quadrantes[i].matriz[linha][coluna]
                    self.quadrantes_botoes[i][linha][coluna].configure(text=valor, state = 'disabled', bg='white')       
                    self.quadrantes_botoes[i][linha][coluna].unbind('<Button-1>')

        tempo_final = time.time()
        print(tempo_final-tempo_inicial)

root = tk.Tk()

app = App(root)
root.resizable(0,0)
root.eval('tk::PlaceWindow . center')

icone = resource_filename(__name__, 'icon.ico')
root.iconbitmap(icone)
root.title('Sudoku!')
root.mainloop()
