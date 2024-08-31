import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import time
from shutil import copy, copy2
from pathlib import Path

VERSION = "0.2.0"
    
class MainApp(tk.Tk):

    folder_path = ""
    file_list = []
    kill_process = False #Variabile di controllo per interrompere processo di copia
    
    def __init__(self, master):
        self.master = master

        # StringVar sono utilizzati come textvariable in label ed affini per cambiare dinamicamente il contenuto delle stesse
        self.folder_path = tk.StringVar() #Testo per la entry riguardante il path di origine
        self.dest_path = tk.StringVar()
        self.new_name = tk.StringVar()
        self.file_list_variable = tk.StringVar() #Testo per la label contenente i nomi dei files
        self.completion_count = tk.IntVar() #variabile per contatore GUI
        self.max_count = tk.IntVar()

        master.title(f"Easy File Renamer {VERSION}")
        master.geometry("550x330")
        master.resizable(0,0)

        title_label = tk.Label(master, text="Easy File Renamer", font="Arial 20")
        title_label.grid(row=0, column=0, sticky=tk.SW, padx=15, pady=5)
        #Frame Principale
        main_frame = tk.Frame(master, padx=10)
        main_frame.grid(row=1, column=0, padx=5)

        #Label cartella sorgente 0x0
        dir_label = tk.Label(main_frame,text="Cartella sorgente:", font="Arial 14")
        dir_label.grid(row=0,column=0, sticky=tk.W)
        
        #Entry per Path Sorgente 1x0 -> 1x8
        path_field = tk.Entry(main_frame,background="white",fg="black", textvariable=self.folder_path)
        path_field.grid(row=1,column=0, columnspan=8, sticky=tk.W+tk.E)
        #Button per finestra Directory selector (con call funzione in lambda)
        path_btn = tk.Button(main_frame, text="...",command = lambda: self.browse_directories()) #Lambda perché altrimenti funzione partiva all'avvio
        path_btn.grid(row=1, column=8, sticky=tk.E)

        #Listbox dei file presenti + scroll bar 2x0 -> 2x9
        file_listbox = tk.Listbox(main_frame,listvariable=self.file_list_variable, height=10, bg="white",fg="black")
        file_sb = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=file_listbox.yview)
        file_listbox['yscrollcommand'] = file_sb.set
        file_sb.grid(row=2, column=9, rowspan=8, sticky=tk.NE+tk.SE)
        file_listbox.grid(row=2, column=0,columnspan=9,rowspan=8, sticky=tk.W+tk.E, padx=2)

        separator = ttk.Separator(main_frame,orient=tk.VERTICAL)
        separator.grid(row=0, column=10, rowspan=11, ipady=125, padx=10, pady=5, sticky=tk.N+tk.S)

        #Label cartella destinazione 0x11
        dest_label = tk.Label(main_frame, text="Cartella destinazione:", font="Arial 14")
        dest_label.grid(row=0, column=11, sticky=tk.W)

        #Entry Path Destinazione 1x11 -> 1x19
        dest_field = tk.Entry(main_frame, background="white", fg="black", textvariable=self.dest_path)
        dest_field.grid(row=1, column=11, columnspan=8, sticky=tk.W+tk.E)
        #Button Browse destinazione
        dest_btn = tk.Button(main_frame, text=">>", command= lambda: self.browse_destination())
        dest_btn.grid(row=1,column=19, sticky=tk.E)
        

        name_label = tk.Label(main_frame, text="Il nome da dare ai file:", font="Arial 14")
        name_label.grid(row=2, column=11, sticky=tk.W+tk.N)

        name_field = tk.Entry(main_frame, background="white", fg="black",textvariable=self.new_name)
        name_field.grid(row=3, column=11, columnspan=9, sticky=tk.W+tk.E+tk.N)

        rename_btn = tk.Button(main_frame,text="Copia", command= lambda: self.sposta_files(self.folder_path.get(), self.dest_path.get(), self.new_name.get()))
        rename_btn.grid(row=4, column=11, columnspan=9,rowspan=2, sticky=tk.W+tk.E+tk.S+tk.N)

        self.progressbar = ttk.Progressbar(master, variable=self.completion_count, orient=tk.HORIZONTAL, mode="determinate")
        self.progressbar.grid(row=2, column=0, sticky=tk.E+tk.W+tk.S, padx=10, ipady=10)

        main_frame.grid_rowconfigure(list(range(0,4)), minsize=20, pad=0, weight = 1)
        main_frame.grid_columnconfigure(list(range(0,20)), minsize=5)


    
    def browse_directories(self) -> None:
        #!!! Focus issue con filedialog.askdirectory()
        dir_name = filedialog.askdirectory()
        self.folder_path.set(dir_name)
        for item in os.scandir(dir_name):
            #Aggiungo solo i file, non le cartelle
            if item.is_file():
                self.file_list.append(item.path)
        self.file_list_variable.set(self.file_list)
        #Magari mostrare solo il nome del file e non tutto il path, valutare estensione oggetto File

    def browse_destination(self) -> None:
        dir_name = filedialog.askdirectory()
        self.dest_path.set(dir_name)

    def sposta_files(self, folder_path, dest_path, new_name) -> None:
        #Creo una lista di soli path di files visibili, ovvero escludo i file che iniziano con il punto
        try:
            if folder_path == "":
                raise Exception("Non è stata specificata la cartella sorgente.")
            if dest_path == "":
                raise Exception("Non è stato specificata la cartella di destinazione.")
            if new_name == "":
                raise Exception("Non è stato specificato il nuovo nome per i file.")
            lista_files = list(single_file for single_file in os.scandir(folder_path) if single_file.is_file() and not(single_file.name[0] == "."))
        
            #self.max_count.set(len(lista_files))
            self.progressbar['maximum'] = len(lista_files)
            #self.progressbar.configure(maximum=len(lista_files))

            for i,individual_file in enumerate(lista_files):
                #Se la cartella di destinazione dei file non esiste, la creo
                if Path(dest_path).is_dir() is False:
                    os.mkdir(dest_path)

                #Copio il file in una cartella apposita mantenendo l'estensione grazie a Path().suffix
                #Aggiungo al nome del file la data di creazione

                #Acquisisco data di creazione come float
                c_time = time.ctime(os.path.getctime(individual_file.path))
                #Formatto la data
                ctime_str = time.strftime("%Y-%m-%d_%H-%M-%S",time.strptime(c_time))

                #Compongo il nome del file
                copy2(individual_file.path,f"{dest_path}/{new_name}_{ctime_str}{Path(individual_file.path).suffix}")
                self.completion_count.set(i+1)
                self.progressbar.update()

            messagebox.showinfo("Fatto","La copia ha avuto successo")
        
        except Exception as e:
            messagebox.showerror("Errore",str(e))

    def sposta_files_worker(self,folder_path, dest_path, new_name) -> None:
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
    