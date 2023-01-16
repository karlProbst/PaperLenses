#tkinter gui busca pdf - Karl Probst
import os.path
from os import path
import tkinter as tk
from tkinter import filedialog
import fitz
import os, re, sys
import subprocess
# initializing vars
file_buscas_salvas="./buscas_salvas.txt"
buscas_salvas = []
pdf_folder = ""
pdfs = []

# Open directory
def chose_folder(): 
    global pdf_folder
  
    folder = filedialog.askdirectory()
    if folder is None: 
        return
    folder+="/"
    pdf_folder=folder
    update_pdf_list(get_pdf_files(folder))
# get .pdf files from dir
def get_pdf_files(folder):
    files = []
    #os.path.join(current_directory,folder)
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            files.append(file)
    return files
# search pdf func
def find_in_pdf(files,string):
    global pdf_folder
    # look for each file
    found_files_list=[]
    for file in files:
        try:
            doc = fitz.open(os.path.join(pdf_folder,file))
            for page in doc:  
                # actual search 
                print(page.search_for(string))
                if len(page.search_for(string))>0:
                    found_files_list.append(file)
        except:
            print("Não foi possível ler o arquivo: "+os.path.join(pdf_folder,file))
    # return list of pdf with found string
    return found_files_list
# read txt of buscas_salvas
if path.exists(file_buscas_salvas):
    f = open(file_buscas_salvas,'r')
    with open(file_buscas_salvas, 'r') as f:
        buscas_salvas = [line.strip() for line in f]
else:
    filename = file_buscas_salvas
    with open(file_buscas_salvas, 'w') as f:
        f.write(" ")
        
# GUI
root = tk.Tk()

root.title("BuscaPDF")
root.geometry("400x600")



    
    
#dir button
dir_btn = tk.Button(root, text ='Escolha o diretório contendo os PDFs', command = lambda:chose_folder()) 
dir_btn.grid(row=0, column=0)

# search bar
#busca_label = tk.Label(root, text='Buscar PDF ')
#busca_label.grid(sticky='we',padx=5, pady=5)

# input
busca_input_string = tk.StringVar()
busca_input_string.set("Palavra chave que deseja pesquisar")
busca_input = tk.Entry(root, text=busca_input_string)
busca_input.grid(row=1,column=0, sticky='ew')

busca_input.bind("<FocusIn>", lambda args: busca_input.delete('0', 'end'))
# list of saved 

buscas_salvas_label = tk.Label(root, text='Buscas recentes: ')
buscas_salvas_label.grid(row=2,column=0, sticky='ew')
#search button
save_btn = tk.Button(root,text="Buscar!")
save_btn.grid(row=3,column=0, sticky='ew', ipadx=10, ipady=10)



# list
buscas_salvas_inp = tk.Listbox(root,height=3 )
buscas_salvas_inp.grid(row=4,column=0, sticky='ew', padx=5, pady=5)

def update_buscas_salvas():
    for busca_salva in buscas_salvas:
        buscas_salvas_inp.insert(tk.END, busca_salva)
update_buscas_salvas()
def callback_buscas_salvas(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        busca_input_string.set(data)
   
        
buscas_salvas_inp.bind("<<ListboxSelect>>", callback_buscas_salvas)



# list of pdfs in folder
def callback_pdf_list(event):
    global pdf_folder
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        subprocess.call(["xdg-open", os.path.join(pdf_folder,data)])
pdf_list = tk.Listbox(root,height=30 )
pdf_list.grid(row=5,column=0, sticky='ew', padx=5, pady=5)

pdf_list.bind("<<ListboxSelect>>", callback_pdf_list)
# update list of pdfs
def update_pdf_list(list):
    pdf_list.delete(0,tk.END)
    global pdfs
    if len(list)==0:
        return
    for pdf in list:
        pdfs.append(pdf)
        pdf_list.insert(tk.END, pdf)


# list of found pdfs
def callback_found_pdf_list(event):
    global pdf_folder
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        subprocess.call(["xdg-open", os.path.join(pdf_folder,data)])

found_pdf_list = tk.Listbox(root,height=30 )
found_pdf_list.grid(row=5,column=1, sticky='e', padx=5, pady=5)

found_pdf_list.bind("<<ListboxSelect>>", callback_found_pdf_list)

def update_found_pdf_list(list):
    if len(list)==0:
        return
    for pdf in list:
        found_pdf_list.insert(tk.END, pdf)

def Buscar():
    global pdfs
    global pdf_folder
    # buscar btn
    # validation checks
    print(pdfs)
    print(pdf_folder)
    search_string = busca_input.get()
    if len(search_string)<1:
        return
    
    #add to recent searches
    buscas_salvas.append(search_string)
    update_buscas_salvas()
    with open(file_buscas_salvas, 'a') as myfile:
        myfile.write(search_string+ "\n")
    # find in pdf
    update_found_pdf_list(find_in_pdf(pdfs,search_string))
    
        
    #status_bar.configure(text='Nova busca salva!')

save_btn.configure(command=Buscar)
root.mainloop()