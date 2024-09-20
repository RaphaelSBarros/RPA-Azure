import sys
import os

# Adiciona o caminho da pasta RPA - AZURE ao sys.path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root)

from module import *

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x200")
        self.grid_columnconfigure((0), weight=1)
        
        self.is_canceled = None

        self.label = customtkinter.CTkLabel(self, text="Faça login no Azure antes de continuar")
        self.label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        
        self.continue_btn = customtkinter.CTkButton(self, text='continuar', fg_color='#ff8200', hover_color='#ff7100', text_color='black', command=lambda: self.click_event(False))
        self.continue_btn.grid(row=1, column=0,padx=20, pady=20)
        
        self.cancel_btn = customtkinter.CTkButton(self, text='cancelar', fg_color='white', hover_color='gray', text_color='black', command=lambda: self.click_event(True))
        self.cancel_btn.grid(row=1, column=1,padx=20, pady=20)
    
    def click_event(self, bool:bool):
        self.is_canceled = bool
        self.grab_release()
        self.destroy()
        
    def get_click_option(self):
        self.master.wait_window(self)
        return self.is_canceled
    