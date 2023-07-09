from classes.quadrante import Quadrante, BlockedException
from threading import Thread
from threading import enumerate
from random import randint
import time
import copy
from queue import Queue


class Tabuleiro():
    def __init__(self) -> None:
        # Inicializa os quadrantes do tabuleiro
        quadrante_1 = Quadrante(0)
        quadrante_2 = Quadrante(1)
        quadrante_3 = Quadrante(2)
        quadrante_4 = Quadrante(3)
        quadrante_5 = Quadrante(4)
        quadrante_6 = Quadrante(5)
        quadrante_7 = Quadrante(6)
        quadrante_8 = Quadrante(7)
        quadrante_9 = Quadrante(8)

        quadrante_1.set_vizinhos_h([quadrante_2, quadrante_3])
        quadrante_1.set_vizinhos_v([quadrante_4, quadrante_7])

        quadrante_2.set_vizinhos_h([quadrante_1, quadrante_3])
        quadrante_2.set_vizinhos_v([quadrante_5, quadrante_8])

        quadrante_3.set_vizinhos_h([quadrante_1, quadrante_2])
        quadrante_3.set_vizinhos_v([quadrante_6, quadrante_9])

        quadrante_4.set_vizinhos_h([quadrante_5, quadrante_6])
        quadrante_4.set_vizinhos_v([quadrante_1, quadrante_7])

        quadrante_5.set_vizinhos_h([quadrante_4, quadrante_6])
        quadrante_5.set_vizinhos_v([quadrante_2, quadrante_8])

        quadrante_6.set_vizinhos_h([quadrante_4, quadrante_5])
        quadrante_6.set_vizinhos_v([quadrante_3, quadrante_9])

        quadrante_7.set_vizinhos_h([quadrante_8, quadrante_9])
        quadrante_7.set_vizinhos_v([quadrante_1, quadrante_4])

        quadrante_8.set_vizinhos_h([quadrante_7, quadrante_9])
        quadrante_8.set_vizinhos_v([quadrante_2, quadrante_5])

        quadrante_9.set_vizinhos_h([quadrante_7, quadrante_8])
        quadrante_9.set_vizinhos_v([quadrante_3, quadrante_6])

        self.quadrantes: list[Quadrante] = [quadrante_1, quadrante_2, quadrante_3,
                                            quadrante_4, quadrante_5, quadrante_6, quadrante_7, quadrante_8, quadrante_9]

        self.quadrantes_copia = []
        self.resolvido = False
        self.solucao = None
        self.preencher_tabuleiro()

    def preencher_tabuleiro(self):

        # Preenche todas as casas do tabuleiro
        flag = False
        while flag == False:
            flag = True
            for quadrante in self.quadrantes:
                try:
                    quadrante.preencher_matriz()
                except BlockedException:
                    self.zerar_quadrantes()
                    flag = False

    def verificar_tabuleiro(self, lista=None):
        if not lista:
            lista = self.quadrantes

        for quadrante in self.quadrantes:
            self.matriz = quadrante.matriz

            for i in range(3):
                for j in range(3):
                    if quadrante.verificar_vizinhos(self.matriz[i][j], i, j):
                        return False
        return True

    def gerar_jogo(self):

        espacos_vazios = 0
        while espacos_vazios <= 46:

            quad = randint(0, 8)
            i = randint(0, 2)
            j = randint(0, 2)
            # and (self.quadrantes[quad].quantidade_valor(0) < 9)
            if self.quadrantes[quad].matriz[i][j] != 0 and (self.quadrantes[quad].quantidade_valor(0) < 9):
                self.quadrantes[quad].matriz[i][j] = 0
                espacos_vazios += 1

    def encontrar_valores_invalidos(self, quad, valor, linha, coluna):

        coordenadas = []

        for i in range(3):
            for j in range(3):
                if self.quadrantes[quad].matriz[i][j] == valor and not (i == linha and j == coluna):
                    coordenadas.append((quad, i, j))

        for vizinho in self.quadrantes[quad].vizinhos_h:
            aux = vizinho.verificar_linha(valor, linha)
            if aux is not None:
                coordenadas.append(aux)

        for vizinho in self.quadrantes[quad].vizinhos_v:
            aux = vizinho.verificar_coluna(valor, coluna)
            if aux is not None:
                coordenadas.append(aux)
        return coordenadas

    def converte_coordenada_local(self, quad, valor):

        for linha in range(9):
            if valor in self.mapa[linha]:
                coluna = self.mapa[linha].index(valor)
                break

        if linha < 3:
            i = linha
        else:
            i = linha % 3

        if coluna < 3:
            j = coluna
        else:
            j = coluna % 3

        return i, j

    def print_tabuleiro(self):
        print('-'*31)
        for i in range(3):
            print(self.quadrantes[0].matriz[i], end='  ')
            print(self.quadrantes[1].matriz[i], end='  ')
            print(self.quadrantes[2].matriz[i], end='  ')
            print()

        print()

        for i in range(3):
            print(self.quadrantes[3].matriz[i], end='  ')
            print(self.quadrantes[4].matriz[i], end='  ')
            print(self.quadrantes[5].matriz[i], end='  ')
            print()

        print()

        for i in range(3):
            print(self.quadrantes[6].matriz[i], end='  ')
            print(self.quadrantes[7].matriz[i], end='  ')
            print(self.quadrantes[8].matriz[i], end='  ')
            print()
        print()

    def zerar_quadrantes(self):
        for quadrante in self.quadrantes:
            quadrante.matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def gerar_mapa(self):
        x = [[], [], [], [], [], [], [], [], []]
        for i in range(9):
            for j in range(9):
                x[i].append(j+(i*9))
        return x

    def resolver_jogo(self):
        # Preenche todas as casas do tabuleiro
        flag = False
        tentativas = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.quadrantes_copia = copy.deepcopy(self.quadrantes)
        while flag == False:
            flag = True
            self.quadrantes = copy.deepcopy(self.quadrantes_copia)
            i = 0
            while i < 9:
                # copia_quadrante = copy.deepcopy(self.quadrantes[i])
                try:
                    if self.quadrantes[i].resolver_quadrante():
                        i += 1

                except BlockedException:
                    i = 0
                    self.quadrantes = copy.deepcopy(
                        self.quadrantes_copia)

                    # tentativas[i] += 1
                    # self.quadrantes[i].matriz = copy.deepcopy(
                    #     self.quadrantes_copia[i].matriz)

                    # if i != 0:
                    #     if 1000 in tentativas:

                    #         print(tentativas)
                    #         pos = tentativas.index(1000)
                    #         i = pos//2
                    #         self.quadrantes[pos//2].matriz = copy.deepcopy(
                    #             self.quadrantes_copia[pos//2].matriz)
                    #         tentativas[pos] = 0
                    #     else:
                    #         self.quadrantes[i-1].matriz = copy.deepcopy(
                    #             self.quadrantes_copia[i-1].matriz)
                    #         i -= 1


class T_resolve(Thread):

    def __init__(self, tabuleiro, queue):
        Thread.__init__(self)
        self.tabuleiro = tabuleiro
        self.queue = queue
        # self.tabuleiro_copia = copy.deepcopy(tabuleiro)

    def run(self):

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


class Teste():
    def __init__(self) -> None:

        self.tabuleiro = Tabuleiro()
        self.tabuleiro.print_tabuleiro()
        self.tabuleiro.gerar_jogo()

        # print(self.tabuleiro_2.quadrantes)
        # print(self.tabuleiro.quadrantes)
        self.tabuleiro.print_tabuleiro()
        queue = Queue()
        for _ in range(15):
            tab = copy.deepcopy(self.tabuleiro)
            trabalhador = T_resolve(tab, queue)
            trabalhador.daemon = True
            trabalhador.start()

        queue.join()
        queue.get().print_tabuleiro()

    # def print_threads(self):
    #     while len(enumerate())>0:
    #         for t in enumerate():
    #             print(t)

    #         time.sleep(5)

# Teste()
