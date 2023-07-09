import tkinter as tk


class Celula(tk.Frame):

    def __init__(self, master=None, valor='', cor_valor='black') -> None:
        super().__init__(master)

        self.config(background="black", borderwidth=1)

        self.anotacoes: list[tk.Label] = []

        self.in_frame = tk.Frame(self, background='white')

        for i in range(5):
            lbl = tk.Label(
                self.in_frame, text=i+1, disabledforeground='white', state='disabled', background='white')

            lbl.grid(row=0, column=i)
            self.anotacoes.append(lbl)

        self.label_valor = tk.Label(self.in_frame, text=valor, width=3, font=(
            'Arial', 30), background='white', fg=cor_valor, disabledforeground=cor_valor)

        self.label_valor.grid(row=1, column=0, columnspan=5)
        # self.label_valor.bind('<Button-1>', lambda evt: self.alterar_fundo('blue'))

        for i in range(4):
            lbl = tk.Label(self.in_frame, text=i+6,
                           disabledforeground='white', state='disabled', background='white')

            lbl.grid(row=2, column=i)
            self.anotacoes.append(lbl)

        # self.bind('<Button-1>', lambda evt: self.alterar_fundo('blue'))
        self.in_frame.pack()
        self.anotacoes.append(self.label_valor)

    def alterar_fundo(self, cor):

        for chd in self.anotacoes:
            chd.config(background=cor, disabledforeground=cor)

        self.in_frame.config(background=cor)

    def bind_all(self, evento, funcao):

        for chd in self.anotacoes:
            chd.bind(evento, funcao)

        self.bind(evento, funcao)

    def fazer_anotacao(self, valor):

        if self.anotacoes[valor-1]['state'] == 'disabled':
            self.anotacoes[valor-1]['state'] = 'normal'
        else:
            self.anotacoes[valor-1]['state'] = 'disabled'

    def limpar_anotacoes(self):
        for i in range(9):
            self.anotacoes[i]['state'] = 'disabled'
# root = tk.Tk()

# Celula(root).pack()

# root.eval('tk::PlaceWindow . center')
# root.mainloop()
