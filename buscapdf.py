#tkinter Busca pdf - Karl Probst - 1/18/2023 - v1.1 - Orange Business Services 

#TO DO:

#SCROLLBARS!!
# highlighter
# status bar
# blink when correct
# greyed out found list when nothing is there
# images miniatures
# image viewer on side
# full responsive aligned gui
# sugestion box thtat sends mail
# show dir
# add page indication wehre found
# add font change button
# night mode


import os.path
from os import path
import tkinter as tk
from tkinter import filedialog, ttk
import fitz
import os, re, sys
import subprocess
from pathlib import Path
import atexit


# initializing vars
file_buscas_salvas="./buscas_salvas.txt"
buscas_salvas = []
pdf_folder = ""
pdfs = []

# read txt of buscas_salvas
if path.exists(file_buscas_salvas):
    
    with open(file_buscas_salvas, 'r') as f:
       
        buscas_salvas = f.readlines()
        buscas_salvas = [x for x in buscas_salvas if x != '\n']
        
else:
    filename = file_buscas_salvas
    with open(file_buscas_salvas, 'w') as f:
        f.write("")

# Open directory
def chose_folder(): 
    global pdf_folder
    files = []
    # open browser dialog to select dir
    try:
        folder = filedialog.askdirectory()
    except:
        pass
    if folder is None: 
        return

    pdf_folder=folder
    # get .pdf files from dir
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            files.append(file)
    
    update_pdf_list(files)


# search pdf func
def find_in_pdf(files,strings):
    global pdf_folder
    # look for each file
    found_files_list=[]
    for file in files:
        try:
            doc = fitz.open(os.path.join(pdf_folder,file))
            matches = []
        

            for page in doc:  
                # actual search 
                for s in strings:
                    # add found word to list
                    if len(page.search_for(s))>0:
                        matches.append(s)
                        
            # if list has all of strings keywords
            if(all(item in matches for item in strings)):
                #found file
                found_files_list.append(file)
            doc.close()
        except:
            pass
        
    # return list of pdf with found string
    return found_files_list


        
# GUI
root = tk.Tk()
try:
    root.iconbitmap("icon.ico")
except:
    pass
    #print("ícone não encontrado no diretório")

root.option_add("*Font", "Calibri 12 ")
root.option_add("*Background", "white")
root.option_add("*Foreground", "white")

root.option_add("relief","SUNKEN")

root.title("Busca PDF")
root.geometry("720x480")


n_rows = 5
n_columns =4

for i in range(n_columns):
    root.grid_columnconfigure(i,  weight =1)
    
    
# input
busca_input_string = tk.StringVar()
busca_input_string.set("Palavra chave que deseja pesquisar")

#clear input
def clear_busca_input_on_click():
    if busca_input.get() == "Palavra chave que deseja pesquisar":
        busca_input.delete('0', 'end')

rel_var="flat"
button_color="#5B5B5B"
text_color="black"
#frames
buscas_salvas_frame = tk.Frame(root)
pdf_list_frame = tk.Frame(root)
buscas_salvas_frame.grid_columnconfigure(0,  weight = 10)
# widgets
dir_btn = tk.Button(root, text ='Escolha o diretório contendo os PDFs', command = lambda:chose_folder(),bd=3,relief=rel_var,background=button_color) 
busca_input = tk.Entry(root, text=busca_input_string,bd=2,highlightthickness = 2, relief=rel_var,foreground=text_color)
#buscas_salvas_label = tk.Label(root, text='Buscas recentes: ',bd=0)
buscas_salvas_scrollbar = tk.Scrollbar(buscas_salvas_frame, orient="vertical",relief=rel_var)
pdf_list_scrollbar = tk.Scrollbar(pdf_list_frame, orient="vertical",relief=rel_var)
buscas_salvas_inp = tk.Listbox(buscas_salvas_frame,height = 3,yscrollcommand=buscas_salvas_scrollbar.set, relief=rel_var,foreground=text_color)
save_btn = tk.Button(root,text="Buscar!",relief=rel_var,background=button_color)
pdf_list = tk.Listbox(root,height=30,yscrollcommand=pdf_list_scrollbar.set, relief=rel_var,foreground=text_color)
found_pdf_label = tk.Label(root, text='Encontrados na busca: ',foreground=text_color)
found_pdf_list = tk.Listbox(root,height=30 ,foreground=text_color)
# placing in grid

found_pdf_label.grid(row=4,column=1, sticky='nsew', padx=5, pady=5)

found_pdf_list.grid(row=5,column=1, sticky='nsew', ipadx=25,padx=5, pady=5)
dir_btn.grid(row=0, column=0, padx=5, pady=5,sticky='nsew')
busca_input.grid(row=1,column=0, sticky='nsew', padx=5, pady=5)
#buscas_salvas_label.grid(row=2,column=0, sticky='nsew', padx=5, pady=0)
buscas_salvas_inp.grid(row=3,column=0, sticky='nsew', padx=5, pady=5)
buscas_salvas_scrollbar.grid(row=3,column=1,sticky='nsew',)

buscas_salvas_frame.grid(row=3,column=0, sticky='nsew', padx=5, pady=5)
pdf_list_scrollbar.grid(row=5,column=1,sticky='nsew')
save_btn.grid(row=4,column=0, sticky='nsew', ipadx=5, ipady=5,padx=5, pady=5)
pdf_list.grid(row=5,column=0, sticky='nsew', padx=5, pady=5)
# configs
busca_input.bind("<FocusIn>", lambda args:clear_busca_input_on_click())
buscas_salvas_scrollbar.config(command=buscas_salvas_inp.yview)

def update_buscas_salvas(string):
    global buscas_salvas
    #clear
    try:
        buscas_salvas_inp.delete(0,tk.END)    
        #insert into buscas_salvas
        if string!="":
            if len(buscas_salvas)>20:
                buscas_salvas.insert(0, string)
                buscas_salvas.pop()
            else:
                buscas_salvas.insert(0, string)
        #insert into listbox
        buscas_salvas_inp.insert(tk.END, *buscas_salvas)
    except:
        pass
print(buscas_salvas)
update_buscas_salvas("")

def callback_buscas_salvas(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        busca_input_string.set(data)
   
        
buscas_salvas_inp.bind("<<ListboxSelect>>", callback_buscas_salvas)

#data_folder = Path("D:/")
#file_to_open = data_folder / "pgmt_passaporte.pdf"
#print(file_to_open)
#subprocess.Popen([file_to_open], shell=True)

def open_file(pdf_folder,data):
    try:
        #linux
        subprocess.call(["xdg-open", os.path.join(pdf_folder,data)])
    except:
        #windows
        subprocess.Popen([os.path.join(pdf_folder,data)], shell=True)
# list of pdfs in folder
def callback_pdf_list(event):
    global pdf_folder
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        open_file(pdf_folder,data)
        




pdf_list.bind("<<ListboxSelect>>", callback_pdf_list)
# update list of pdfs
def update_pdf_list(list):
    pdf_list.delete(0,tk.END)
    global pdfs
    pdfs=[]
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
        open_file(pdf_folder,data)



found_pdf_list.bind("<<ListboxSelect>>", callback_found_pdf_list)

def update_found_pdf_list(list):
    found_pdf_list.delete(0,tk.END)
    if len(list)==0:
        return
    for pdf in list:
        found_pdf_list.insert(tk.END, pdf)



def Buscar():
    global pdfs
    global pdf_folder
    print(pdf_folder)
    # buscar btn
    # validation checks
    
    # split by comma into a list 
    search_strings = busca_input.get().split(',')
    # remove empty strings
    search_strings = [x for x in search_strings if x != '']
    # returns if nothing is found on input
    if len(search_strings)<1:
        return
    if search_strings=="Palavra chave que deseja pesquisar":
        return
    if not pdf_folder:
        return
    #add to recent searches
   
    update_buscas_salvas(busca_input.get())
    #with open(file_buscas_salvas, 'a') as myfile:
    #    myfile.write(str(busca_input.get())+ "\n")
    # find in pdf
    
    update_found_pdf_list(find_in_pdf(pdfs,search_strings))
    
        
    #status_bar.configure(text='Nova busca salva!')

save_btn.configure(command=Buscar)
root.mainloop()

#on exit save 
def exit_handler():
    print("JLDJLKJKLD")
    global buscas_salvas
    update_buscas_salvas("")
    try:
        with open(file_buscas_salvas, 'w') as f:
            for line in buscas_salvas:
                f.write(f"{line}\n")
        print(buscas_salvas)
        print("DONE!")
    except:
        pass
atexit.register(exit_handler)