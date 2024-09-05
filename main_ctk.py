import tkinter as tk
import customtkinter
from tkinter import filedialog, messagebox
import os
import time
from shutil import copy2
from pathlib import Path



class FrameSorgente(customtkinter.CTkFrame):

    def __init__(self,master):
        super().__init__(master)

        self.path_sorgente = customtkinter.StringVar()

        self.sorgente_label = customtkinter.CTkLabel(self,text="Cartella sorgente:")
        self.sorgente_label.grid(row=0,column=0, sticky=tk.W, padx=10, pady=(5,0))

        self.sorgente_entry = customtkinter.CTkEntry(self, textvariable=self.path_sorgente)
        self.sorgente_entry.grid(row=1, column=0, sticky=tk.W + tk.E, padx=10, pady=(0,5))

        self.sorgente_btn = customtkinter.CTkButton(self,text="Cerca...", command=self.browse_source)
        self.sorgente_btn.grid(row=2, column=0, sticky=tk.W + tk.E, padx = 10, pady=(0,10))

        self.grid_columnconfigure(0,minsize=255)

    def get(self):
        return self.path_sorgente.get()
        
    def browse_source(self) -> None:
        dir_name = filedialog.askdirectory()
        self.path_sorgente.set(dir_name)

class FrameDestinazione(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.path_destinazione = customtkinter.StringVar()

        self.destinazione_label = customtkinter.CTkLabel(self,text="Cartella destinazione:")
        self.destinazione_label.grid(row=0,column=0, sticky=tk.W, padx=10, pady=(5,0))

        self.destinazione_entry = customtkinter.CTkEntry(self, textvariable=self.path_destinazione)
        self.destinazione_entry.grid(row=1, column=0, sticky=tk.W + tk.E, padx=10, pady=(0,5))

        self.destinazione_btn = customtkinter.CTkButton(self,text="Cerca...", command=self.browse_destination)
        self.destinazione_btn.grid(row=2, column=0, sticky=tk.W + tk.E, padx = 10, pady=(0,10))

        self.grid_columnconfigure(0,minsize=255)

    def get(self):
        return self.path_destinazione.get()
    
    def browse_destination(self) -> None:
        dir_name = filedialog.askdirectory()
        self.path_destinazione.set(dir_name)

class FrameNome(customtkinter.CTkFrame):
    def __init__(self,master):
        super().__init__(master)

        self.nome_files = customtkinter.StringVar()

        self.nome_label = customtkinter.CTkLabel(self,text="Nuovo nome per i file:")
        self.nome_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(5,0))

        self.nome_entry = customtkinter.CTkEntry(self, textvariable=self.nome_files)
        self.nome_entry.grid(row=1, column=0, sticky=tk.W + tk.E, padx=10, pady=(0,10))

        self.grid_columnconfigure(0,minsize=520)

    def get(self):
        return self.nome_files.get()
    

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x295+20+20")
        self.title("EasyFileRenamer")
        self.resizable(0,0)
        
        icon_big = tk.PhotoImage(file="./EFR_Icon_256.png")
        icon_small = tk.PhotoImage(file="./EFR_Icon_64.png")
        self.iconphoto(False,icon_big,icon_small)

        self.completitioncount = customtkinter.IntVar()

        self.title_label = customtkinter.CTkLabel(self,text="Easy File Renamer", font=("Arial", 20))
        self.title_label.grid(row=0,column=0,sticky=tk.W, padx=16,pady=(6,4))

        self.sorgente_frame = FrameSorgente(self)
        self.sorgente_frame.grid(row=1,column=0, sticky=tk.NW+tk.E, padx=(15,2))

        self.destinazione_frame = FrameDestinazione(self)
        self.destinazione_frame.grid(row=1,column=1, sticky=tk.NW+tk.E, padx=(2,15))

        self.nome_frame = FrameNome(self)
        self.nome_frame.grid(row=2, column=0, columnspan=2, sticky=tk.N+tk.E+tk.W, padx=(15,15), pady=(4,2))

        self.copia_btn = customtkinter.CTkButton(self, text="Copia i file!", command= lambda: self.copia_files(self.sorgente_frame.get(), self.destinazione_frame.get(), self.nome_frame.get()))
        self.copia_btn.grid(row=3, column = 0, columnspan = 2, sticky= tk.W+tk.E+tk.N, padx=26, pady=(4,2))

        self.progress_bar = customtkinter.CTkProgressBar(self,variable=self.completitioncount, orientation="horizontal", mode="determinate", progress_color="green")
        self.progress_bar.grid(row=4, column = 0, columnspan = 2, sticky = tk.W+tk.E, padx = 26, pady = (10,16))
        self.completitioncount.set(0)
        self.grid_columnconfigure(0, minsize=275)
        self.grid_columnconfigure(1, minsize=275)

    def copia_files(self,folder_path, dest_path, new_name) -> None:
        try:
            if folder_path == "":
                raise Exception("Non è stata specificata la cartella sorgente.")
            if dest_path == "":
                raise Exception("Non è stato specificata la cartella di destinazione.")
            if new_name == "":
                raise Exception("Non è stato specificato il nuovo nome per i file.")
            lista_files = list(single_file for single_file in os.scandir(folder_path) if single_file.is_file() and not(single_file.name[0] == "."))

            self.progress_bar['maximum'] = len(lista_files)

            for i,individual_file in enumerate(lista_files):
                #Acquisisco data di creazione come float
                c_time = time.ctime(os.path.getctime(individual_file.path))
                #Formatto la data
                ctime_str = time.strftime("%Y-%m-%d_%H-%M-%S",time.strptime(c_time))

                #Compongo il nome del file
                copy2(individual_file.path,f"{dest_path}/{new_name}_{ctime_str}{Path(individual_file.path).suffix}")
                self.progress_bar.set(i+1)
                self.progress_bar.update()

            messagebox.showinfo("Fatto!","La copia ha avuto successo")
            self.progress_bar.set(0)

        except Exception as e:
            messagebox.showerror("Errore",str(e))

if __name__ == "__main__":
    app = App()
    app.mainloop()