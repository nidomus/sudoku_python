import ttkbootstrap as tb
import tkinter as tk
from ttkbootstrap.constants import *
from pathlib import Path
from ttkbootstrap.tooltip import ToolTip


PATH = Path(__file__).parent.parent.parent / 'assets' / 'emojis'
from ttkbootstrap.icons import Emoji

FONT = 20
COR_1 = "#344861"

class Popup_numeros():
    def __init__(self,root=None, app =None, btn = None,coord =None,quad = None):

        x = root.winfo_pointerx() 
        y = root.winfo_pointery()
        
        self.app = app
        app.selecionado(btn,coord,quad)
        self.janela = tk.Toplevel(root)
        
        self.janela.geometry(f'+{x}+{y}')
        
        self.root = root

        self.janela.wm_overrideredirect(True)
        self.janela.focus()

        for i in range(3):

            frame = tk.Frame(self.janela)
            frame.pack(side=TOP)

            for j in range(3):
                button = tk.Button(frame, 
                    text=str(j+1 + (i*3)), 
                    width=3,
                    font=('Arial', FONT),
                    fg = COR_1,
                    background='white' )
                button.pack(side=LEFT)

                button.bind('<Button-1>', lambda event,valor = j+1 + (i*3): self.on_click(event,valor))

        # self.focus()



        self.janela.bind("<FocusOut>", lambda a: self.on_focus_out())
    
    def on_focus_out(self):

        self.janela.destroy()

    def on_click(self,event,valor):
        self.app.alterar_valor_popup(event,valor)
        self.janela.destroy()