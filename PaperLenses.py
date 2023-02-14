#Paper Lenses Busca pdf/docx- Karl Probst - 12/Feb/2023 - v1.5 - Orange Business Services 
#pyinstaller --onefile --windowed --add-data "orange.png;." --add-data "icon.ico;." --icon "icon.ico" PaperLenses.py
#TO DO:

# greyed out found list when nothing is there
# images miniatures

# sugestion box thtat sends mail

# add font change button
# night mode
# Help page
# tirar o 1,2,3,4
# fonte bold
# tudo em inglês
# pasta ao invez de arquivos
# nightmode
import time
import glob
import shutil
import os.path
from os import path
import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
from tkinter.font import Font, nametofont
import fitz
import os, re, sys
import subprocess
from pathlib import Path
import atexit
from PIL import ImageTk,Image
from itertools import count
import itertools
import threading 
import tempfile
import docx2txt




#path of installed resources
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# get system temp folder
tempdir = tempfile.gettempdir()
# initializing vars

buscas_salvas = []
root_path=os.path.join(tempdir,"paperlenses")
pdf_path = os.path.join(root_path,"PDF")
doc_path = os.path.join(root_path,"DOC")
docx_path = os.path.join(root_path,"DOCX")
img_path= os.path.join(root_path,"IMG")
buscas_salvas_path = os.path.join(root_path,"buscas_salvas.txt")
search_strings=[]
documents_list = []
found_documents = []
current_img = []
current_img_counter = 0
a=0
WIDTH=800
HEIGHT=800
# adding temp path to the folders 

#creates folders if not exist
if not path.exists(root_path):
    os.makedirs(root_path)
if not path.exists(pdf_path):
    os.makedirs(pdf_path)
if not path.exists(img_path):
    os.makedirs(img_path)
if not path.exists(doc_path):
    os.makedirs(doc_path)
if not path.exists(docx_path):
    os.makedirs(docx_path)
# status bar
# read txt of buscas_salvas
if path.exists(buscas_salvas_path): 
    with open(buscas_salvas_path, 'r') as f:  
        buscas_salvas = f.readlines()
        buscas_salvas = [x for x in buscas_salvas if x != '\n']       
else:
    filename = buscas_salvas_path
    with open(buscas_salvas_path, 'w') as f:
        f.write("")

def print_status(string):
    try:
        status_bar.config(text = string)
    except:
        pass
# Open directory
def save_found():
    global pdf_path
    global doc_path
    global docx_path
    global found_documents
    counter=0
    try:
        folder = filedialog.askdirectory()
    except:
        pass
    if folder is None: 
        return
    try:
        for file in found_documents:
            counter+=1
            if file.endswith('.docx'):
                shutil.copy(os.path.join(docx_path,file), folder)   
            if file.endswith('.pdf'):
                shutil.copy(os.path.join(pdf_path,file), folder)

            print_status(""+str(counter)+" files where saved to "+str(folder))    
    except:
        print_status("It was not possible to save.")
def chose_folder(): 
    global pdf_path
    global doc_path
    global docx_path
    files = []
    # open browser dialog to select dir
    try:
        folder = filedialog.askdirectory()
    except:
        pass
    if files is None: 
        return
    counter=0
    print_status("Importing documents...")
    
    # get .pdf files from dir   
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            shutil.copy(os.path.join(folder,file), pdf_path)
            counter+=1
           
    # get .docx files from dir   
    for file in os.listdir(folder):
        if file.endswith(".docx"):
            print(file)
            shutil.copy(os.path.join(folder,file), docx_path)
          
            counter+=1
    if(counter>1):
        print_status(""+str(counter)+" documents where imported, type a filter and search!\n You can search for multiple words at the same time with a comma(,)")
    else:
        print_status("1 document was imported, type a filter and search!\n You can search for multiple words at the same time with a comma ,")
    update_documents_list()
    
print(doc_path)
# search pdf func
def find_in_pdf(files,strings):
    
    global pdf_path
    global doc_path
    global docx_path
    global img_path
    # look for each file
    found_files_list=[]
    firstfile= 0
    matches = []
    page_counter=0
    for file in files:
        firstfile=file
        #DOCX SEARCH
        if file.endswith('.docx'):
           
            
            txt = docx2txt.process(os.path.join(docx_path,file))
            
            txt = txt.lower()
            for s in strings:
                if s in txt: 
                    matches.append(s)    
        
      
           
        #PDF SEARCH
        if file.endswith('.pdf'):
            try:
                print_status("Processing "+file)
                doc = fitz.open(os.path.join(pdf_path,file))  
                
                for page in doc:  
                    text_instances=[]
                    # actual search 
                    for s in strings:
                        # add found word to list
                        temp_search=page.search_for(s)
                        if len(temp_search)>0:
                            matches.append(s)
                            #save image with highlighter
                            text_instances.append(temp_search)  
                    page_counter+=1
                doc.close()
      
            except:
                print_status("It was not possible to open "+file)

        # if list has all of strings keywords
        if all(item in matches for item in strings):
            #found file 
            print_status("Match in "+file)
            found_files_list.append(file) 
            
    # return list of pdf with found string
    
    flen=len(found_files_list)
    if flen == 0:
        print_status(str(busca_input.get())+" Was not found on the imported documents.")
    elif flen == 1:
        print_status("Found in document\n "+str(firstfile[0:60])+" \nListed on the right. Click on each item on the list to open the document.")
    else:
        print_status(str(busca_input.get())+"Was found on "+str(flen)+ " documents\n  Listed on the right. Click on each item on the list to open the document.")
    return found_files_list


# GUI
root = tk.Tk()
root["bg"] = "white"
root.option_add("*Font", "Calibri 12 ")
root.option_add("*Background", "white")
root.option_add("*Foreground", "black")
root.option_add("sel", "red")
root.option_add("relief","SUNKEN")

try:
    root.iconbitmap(resource_path("icon.ico"))
except:
    pass
root.resizable(False, False)
rel_var="flat"
button_color="#FF7900"
text_color="black"
button_foreground_color="white"
root.title("Paper Lenses v1.0")
#root.geometry("652x665")
root.geometry("542x572")

class ShadowButton(tk.Frame):

    def __init__(self, parent=None,**options):
        sc="grey"
        si=1
        tk.Frame.__init__(self, parent, bg=sc)
        self.label = tk.Button(self, text=options["text"], padx=15, pady=10)
        self.label.pack(expand=1, fill="both", padx=(0, si), pady=(0, si))
  
    
# input
busca_input_string = tk.StringVar()
busca_input_string.set('Keywords to search (ex: cisco,english)')

status_string ="""
Welcome to Paper Lenses!
1. Select a folder containing all .pdf or .docx (you can do this multiple times)
2. Type words to be searched (multiple search is possible with a comma)
3. Click in Search to filter
4. Save all the found documents on a chosen directory.
"""


#clear input
def clear_busca_input_on_click():
    if busca_input.get() == 'Keywords to search (ex: cisco,english)':
        busca_input.delete('0', 'end')



bfont = Font(family='"Helvetica Neue"', size=11,weight="bold")
cfont = Font(family='"Helvetica Neue"', size=10,weight="bold")

#orange logo

print(resource_path) 
#orangelogo

#orange_label=tk.Label(root,background=button_color,foreground=button_color)
#orange_label.grid(row=1,column=1, sticky='nesw',rowspan=4 , padx=5, pady=5,columnspan=4)
try:
    orange_image = ImageTk.PhotoImage((Image.open(resource_path("orange.png"))).resize((int(WIDTH/5.6), int(HEIGHT/5.6 )), Image.LANCZOS))
    orange_image_label = tk.Label(image=orange_image)
    orange_image_label.grid(row=1,column=1, sticky='ns',rowspan=4 , padx=5, pady=5,columnspan=4,)
except:
    pass

#frames
buscas_salvas_frame = tk.Frame(root)
pdf_list_frame = tk.Frame(root)
found_documents_list_frame = tk.Frame(root)
buscas_salvas_frame.grid_columnconfigure(0,  weight = 10)
pdf_list_frame.grid_columnconfigure(0,  weight = 10)
found_documents_list_frame.grid_columnconfigure(0,  weight = 10)

# widgets
status_bar = tk.Label(root, text=status_string,bd=2,highlightthickness = 2, relief=rel_var,foreground=text_color,font=cfont,height=7,width=50)
dir_btn = tk.Button(root, text ='Select a folder containing .pdf or .docx', command = lambda:chose_folder(),bd=3,relief=rel_var,background=button_color,foreground=button_foreground_color,font=bfont) 
busca_input = tk.Entry(root, text=busca_input_string,bd=2,highlightthickness = 2, relief=rel_var,foreground=text_color,font=bfont)
save_found_btn = tk.Button(root, text ='Save all filtered documents', command = lambda:save_found(),bd=3,relief=rel_var,background=button_color,foreground=button_foreground_color,font=bfont) 

#scrollbars
buscas_salvas_scrollbar = tk.Scrollbar(buscas_salvas_frame, orient="vertical",relief=rel_var)
pdf_list_scrollbar = tk.Scrollbar(pdf_list_frame, orient="vertical",relief=rel_var)
found_documents_list_scrollbar = tk.Scrollbar(found_documents_list_frame, orient="vertical",relief=rel_var)

buscas_salvas_list = tk.Listbox(buscas_salvas_frame,height = 3,yscrollcommand=buscas_salvas_scrollbar.set, relief=rel_var,foreground=text_color,font=bfont)
search_btn = tk.Button(root,text="Search!",relief=rel_var,background=button_color,foreground=button_foreground_color,font=bfont)
#
pdf_list = tk.Listbox(pdf_list_frame,height=10,yscrollcommand=pdf_list_scrollbar.set, relief=rel_var,foreground=text_color,font=bfont,width=25)
found_pdf_label = tk.Label(root, text='Filtered files:',foreground=text_color,font=bfont)
found_documents_list = tk.Listbox(found_documents_list_frame,yscrollcommand=found_documents_list_scrollbar.set, relief=rel_var,height=10 ,foreground=text_color,font=bfont,width=25)

# placing in grid

status_bar.grid(row=0,column=0, sticky='nsew' ,padx=5, pady=5,columnspan=10)
found_documents_list.grid(row=7,column=2, sticky='nsew' ,padx=5, pady=5)
dir_btn.grid(row=1, column=0, padx=5, pady=5,sticky='nsew')

save_found_btn.grid(row=5, column=2, padx=5, pady=5,sticky='nsew')

busca_input.grid(row=2,column=0, sticky='nsew', padx=5, pady=5)
#buscas_salvas_label.grid(row=2,column=0, sticky='nsew', padx=5, pady=0)
buscas_salvas_list.grid(row=4,column=0, sticky='nsew', padx=5, pady=5)
buscas_salvas_scrollbar.grid(row=4,column=1,sticky='nsew',)
pdf_list_scrollbar.grid(row=7,column=2,sticky='nsew',)
found_documents_list_scrollbar.grid(row=7,column=3,sticky='nsew',)
buscas_salvas_frame.grid(row=4,column=0, sticky='nsew', padx=5, pady=5)
pdf_list_scrollbar.grid(row=7,column=1,sticky='nsew')
search_btn.grid(row=5,column=0, sticky='nsew', ipadx=5, ipady=5,padx=5, pady=5)
pdf_list.grid(row=7,column=0, sticky='nsew', padx=5, pady=5)
pdf_list_frame.grid(row=7,column=0, sticky='nsew', padx=5, pady=5)
found_documents_list_frame.grid(row=7,column=2, sticky='nsew', padx=5, pady=5)

#  configs
busca_input.bind("<FocusIn>", lambda args:clear_busca_input_on_click())
buscas_salvas_scrollbar.config(command=buscas_salvas_list.yview)
pdf_list_scrollbar.config(command=pdf_list.yview)
found_documents_list_scrollbar.config(command=found_documents_list.yview)


def update_buscas_salvas(string):
    global buscas_salvas
    #clear
    try:
        buscas_salvas_list.delete(0,tk.END)    
        #insert into buscas_salvas
        if string!="":
            if len(buscas_salvas)>50:
                buscas_salvas.insert(0, string)
                buscas_salvas.pop()
            else:
                buscas_salvas.insert(0, string)
        #insert into listbox
        buscas_salvas_list.insert(tk.END, *buscas_salvas)
    except:
        pass

update_buscas_salvas("")

def callback_buscas_salvas(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        busca_input_string.set(data)
   
        


#data_folder = Path("D:/")
#file_to_open = data_folder / "pgmt_passaporte.pdf"
#print(file_to_open)
#subprocess.Popen([file_to_open], shell=True)


def open_file(pdf_path,data):
    try:
        #linux
        subprocess.call(["xdg-open", os.path.join(pdf_path,data)])
    except:
        #windows
        
        subprocess.Popen([os.path.join(pdf_path,data)], shell=True)
# list of pdfs in folder
def callback_pdf_list(event):
    global pdf_path
    global docx_path
    
   
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        
        print_status("Opening "+data+"...")
        if data.endswith(".pdf"):
                open_file(pdf_path,data)
        if data.endswith(".docx"):
                open_file(docx_path,data)




# update list of pdfs
def update_documents_list():
    try:
        pdf_list.delete(0,tk.END)
    except:
        pass
    global pdf_path
    global doc_path
    global docx_path
    global documents_list
    documents_list = []
    for file in os.listdir(pdf_path):
        if file.endswith(".pdf"):
            documents_list.append(file)
            pdf_list.insert(tk.END, file)
    for file in os.listdir(doc_path):
        if file.endswith(".doc"):
            documents_list.append(file)
            pdf_list.insert(tk.END, file)
    for file in os.listdir(docx_path):
        if file.endswith(".docx"):
            documents_list.append(file)
            pdf_list.insert(tk.END, file)

def callback_found_documents_list(event):
    global pdf_path
    global docx_path
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        
        
         # get .pdf files from dir   
        print_status("Opening "+data+"...")
        if data.endswith(".pdf"):
                open_file(pdf_path,data)
        if data.endswith(".docx"):
                open_file(docx_path,data)
  
#open image externally on click
def callback_image_open(event):
    global current_img
    global current_img_counter
    print(str(current_img[current_img_counter]))
    os.startfile(str(current_img[current_img_counter]))
#on click do:
buscas_salvas_list.bind("<<ListboxSelect>>", callback_buscas_salvas)
pdf_list.bind("<<ListboxSelect>>", callback_pdf_list)
found_documents_list.bind("<<ListboxSelect>>", callback_found_documents_list)


#
def update_found_documents_list(list):
    global found_documents
    found_documents = list
    try:
        found_documents_list.delete(0,tk.END)
    except:
        pass
    if len(list)==0:
        return
    for doc in list:
        found_documents_list.insert(tk.END, doc)



def Buscar(event=None):
    
    global documents_list
    global pdf_path
    print_status("Searching in "+str(len(documents_list))+" documents... please wait")
    global search_strings
    # validation checks
    # split by comma into a list 
    search_strings = busca_input.get().split(',')
    if "Keywords to search (ex: cisco,english)" in search_strings:
        return
    # remove empty strings
    search_strings = [x for x in search_strings if x != '']
    #remove spaces at the end and start
    for s in range(len(search_strings)):
       search_strings[s] = search_strings[s].rstrip()
       search_strings[s] = search_strings[s].lstrip()
    # to lower case
    for s in range(len(search_strings)):
       search_strings[s] = search_strings[s].lower()
    # returns if nothing is found on input
    if len(search_strings)<1:
        return
    
    if not pdf_path:
        return
    #add to recent searches
   
    update_buscas_salvas(busca_input.get())
    # find in pdf
    update_found_documents_list(find_in_pdf(documents_list,search_strings))     
    #status_bar.configure(text='Nova busca salva!')

#on exit save 
def exit_handler():
    # delete temp images
    try:
        for img_file in os.scandir(img_path):
            if img_file.name.endswith(".png"):
                os.remove(img_file.path)
    except:
        pass
    # delete temp pdf
    try:
        for file in os.scandir(pdf_path):
            if file.name.endswith(".pdf"):
                os.remove(file.path)
    except:
        pass
    try:
        for file in os.scandir(doc_path):
            if file.name.endswith(".doc"):
                os.remove(file.path)
    except:
        pass
    try:
        for file in os.scandir(docx_path):
            if file.name.endswith(".docx"):
                os.remove(file.path)
    except:
        pass
    global buscas_salvas
    update_buscas_salvas("")
    try:
        with open(buscas_salvas_path, 'w') as f:
            for line in buscas_salvas:
                f.write(f"{line}\n")
     
    except:
        pass

atexit.register(exit_handler)
search_btn.configure(command=Buscar)
busca_input.bind('<Return>', Buscar)
root.mainloop()
