#Paper Lenses Busca pdf/docx- Karl Probst - 09/Feb/2023 - v1.4 - Orange Business Services 

#TO DO:

# status bar
# greyed out found list when nothing is there
# images miniatures
# full responsive aligned gui
# sugestion box thtat sends mail

# add page indication wehre found
# add font change button
# night mode

# save images to memory

# Pdf viewer controls 
# save image button

import time
import glob
import shutil
import os.path
from os import path
import tkinter as tk
from tkinter import filedialog, ttk, PhotoImage
import fitz
import os, re, sys
import subprocess
from pathlib import Path
import atexit
from PIL import ImageTk,Image
from itertools import count
from docx2pdf import convert
import itertools
import threading 
import tempfile

tempdir = tempfile.gettempdir()
# initializing vars
buscas_salvas_path="./buscas_salvas.txt"
img_path="IMG"
buscas_salvas = []
pdf_path = "PDF"
search_strings=[]
pdfs = []
current_img = []
current_img_counter = 0
WIDTH=800
HEIGHT=600
# adding temp path to the folders 
img_path = str(os.path.join(tempdir,img_path))
pdf_path = str(os.path.join(tempdir,pdf_path))
buscas_salvas_path = str(os.path.join(tempdir,buscas_salvas_path))
# read txt of buscas_salvas
if path.exists(buscas_salvas_path):
    
    with open(buscas_salvas_path, 'r') as f:
       
        buscas_salvas = f.readlines()
        buscas_salvas = [x for x in buscas_salvas if x != '\n']
        
else:
    filename = buscas_salvas_path
    with open(buscas_salvas_path, 'w') as f:
        f.write("")
#creates pdf folder if not exist
if not path.exists(pdf_path):
    os.makedirs(pdf_path)
if not path.exists(img_path):
    os.makedirs(img_path)

# status bar
def print_status(string):
    pass
# Open directory

def chose_folder(): 
    global pdf_path
    global loading_bar
    files = []
    # open browser dialog to select dir
    try:
        folder = filedialog.askdirectory()
    except:
        pass
    if folder is None: 
        return
   
    
    

    # get .pdf files from dir
    try:
        for file in os.listdir(folder):
            if file.endswith(".docx"):
                print(str(os.path.join(pdf_path,os.path.splitext(file)[0]+'.pdf')))
                try:
                    convert(file, os.path.join(pdf_path,os.path.splitext(file)[0]+'.pdf'))
                except:
                    pass
    except Exception as e:
        print(e)
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            print(file)
            shutil.copy(os.path.join(folder,file), pdf_path)
            

    update_pdf_list()
    loading_bar.unload()

# search pdf func
def find_in_pdf(files,strings,save_img):

    global pdf_path
    global img_path
    global current_img
    global loading_bar
    # look for each file
    found_files_list=[]
    for file in files:
        try:
            doc = fitz.open(os.path.join(pdf_path,file))
            
            matches = []
            page_counter=0
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
                     
                if save_img:
                    if(all(item in matches for item in strings)):
                        for inst in text_instances:
                            
                            highlight = page.add_highlight_annot(inst)
                            zoom_mat = fitz.Matrix(1, 1)
                            pix = page.get_pixmap(matrix=zoom_mat)  
                            
                        try:
                            
                            temp_img_path=os.path.join(img_path,file.rsplit('.', 1)[0]+str(page_counter)+'.png')
                            current_img.append(temp_img_path)
                            pix.save(temp_img_path)
                            img = ImageTk.PhotoImage(Image.open(current_img[0]).resize((int(WIDTH/2), HEIGHT), Image.ANTIALIAS))
                            image_label.configure(image=img)
                            image_label.image = img
                        except:
                            print_status("não foi possível salvar "+temp_img_path)
                
                page_counter+=1
                                   
            # if list has all of strings keywords
            if(all(item in matches for item in strings)):
                #found file
              
                found_files_list.append(file)
                
            doc.close()
      
            print_status()
        except:
            print_status("Não foi possível abrir aquivo "+file)
        
    # return list of pdf with found string
    return found_files_list

def next_img():
    global current_img
    global current_img_counter
    if current_img_counter>=len(current_img)-1:
        return
    current_img_counter+=1
    
    img = ImageTk.PhotoImage(Image.open(current_img[current_img_counter]).resize((int(WIDTH/2), HEIGHT), Image.ANTIALIAS))
    image_label.configure(image=img)
    image_label.image = img
def prev_img():
    global current_img
    global current_img_counter
    if current_img_counter<=0:
        return
    current_img_counter-=1
   
    img = ImageTk.PhotoImage(Image.open(current_img[current_img_counter]).resize((int(WIDTH/2), HEIGHT), Image.ANTIALIAS))
    image_label.configure(image=img)
    image_label.image = img

# GUI
root = tk.Tk()
img = Image.new("RGB", (800, 600), (200, 200, 200))
img.save("image.png", "PNG")
my_img=ImageTk.PhotoImage(Image.open("image.png").resize((int(WIDTH/2), HEIGHT), Image.ANTIALIAS))



root.option_add("*Font", "Calibri 12 ")
root.option_add("*Background", "white")
root.option_add("*Foreground", "blue")
root.option_add("sel", "red")
root.option_add("relief","SUNKEN")
rel_var="flat"
button_color="#5B5B5B"
text_color="black"
button_foreground_color="white"
root.title("Busca PDF")
root.geometry("900x700")


  
    
# input
busca_input_string = tk.StringVar()
busca_input_string.set("2. Palavras chave (separe com ,)")

#clear input
def clear_busca_input_on_click():
    if busca_input.get() == "2. Palavras chave (separe com ,)":
        busca_input.delete('0', 'end')


#frames
buscas_salvas_frame = tk.Frame(root)
pdf_list_frame = tk.Frame(root)
found_pdf_list_frame = tk.Frame(root)
image_frame = tk.Frame(root)
#
buscas_salvas_frame.grid_columnconfigure(0,  weight = 10)
pdf_list_frame.grid_columnconfigure(0,  weight = 10)
found_pdf_list_frame.grid_columnconfigure(0,  weight = 10)
image_frame.grid_columnconfigure(0,  weight = 1)
# widgets
dir_btn = tk.Button(root, text ='1.Escolha diretórios contendo .docx ou .pdf', command = lambda:chose_folder(),bd=3,relief=rel_var,background=button_color,foreground=button_foreground_color) 
next_img_btn = tk.Button(root, text ='Página anterior<<', command = lambda:prev_img(),bd=3,relief=rel_var,background=button_color,foreground=button_foreground_color) 
prev_img_btn= tk.Button(root, text ='>>Próxima página', command = lambda:next_img(),bd=3,relief=rel_var,background=button_color,foreground=button_foreground_color) 
busca_input = tk.Entry(root, text=busca_input_string,bd=2,highlightthickness = 2, relief=rel_var,foreground=text_color)


#buscas_salvas_label = tk.Label(root, text='Buscas recentes: ',bd=0)

#scrollbars
buscas_salvas_scrollbar = tk.Scrollbar(buscas_salvas_frame, orient="vertical",relief=rel_var)
pdf_list_scrollbar = tk.Scrollbar(pdf_list_frame, orient="vertical",relief=rel_var)
found_pdf_list_scrollbar = tk.Scrollbar(found_pdf_list_frame, orient="vertical",relief=rel_var)

buscas_salvas_list = tk.Listbox(buscas_salvas_frame,height = 3,yscrollcommand=buscas_salvas_scrollbar.set, relief=rel_var,foreground=text_color)
search_btn = tk.Button(root,text="3. Buscar!",relief=rel_var,background=button_color,foreground=button_foreground_color)
pdf_list = tk.Listbox(pdf_list_frame,height=21,yscrollcommand=pdf_list_scrollbar.set, relief=rel_var,foreground=text_color)
found_pdf_label = tk.Label(root, text='Encontrados na busca:',foreground=text_color)
found_pdf_list = tk.Listbox(found_pdf_list_frame,yscrollcommand=found_pdf_list_scrollbar.set, relief=rel_var,height=21 ,foreground=text_color)
#image


image_label = tk.Label(image=my_img)
# placing in grid

image_label.grid(row=2,column=4, sticky='nsew',rowspan=5 , padx=5, pady=5,columnspan=3,)
found_pdf_label.grid(row=4,column=2, sticky='nsew', padx=5, pady=5)
found_pdf_list.grid(row=6,column=2, sticky='nsew' ,padx=5, pady=5)
dir_btn.grid(row=0, column=0, padx=5, pady=5,sticky='nsew')
next_img_btn.grid(row=1, column=4, padx=30, pady=5,sticky='nsew')
prev_img_btn.grid(row=1, column=5, padx=30, pady=5,sticky='nsew')

busca_input.grid(row=1,column=0, sticky='nsew', padx=5, pady=5)
#buscas_salvas_label.grid(row=2,column=0, sticky='nsew', padx=5, pady=0)
buscas_salvas_list.grid(row=3,column=0, sticky='nsew', padx=5, pady=5)
buscas_salvas_scrollbar.grid(row=3,column=1,sticky='nsew',)
pdf_list_scrollbar.grid(row=6,column=2,sticky='nsew',)
found_pdf_list_scrollbar.grid(row=6,column=3,sticky='nsew',)
buscas_salvas_frame.grid(row=3,column=0, sticky='nsew', padx=5, pady=5)
pdf_list_scrollbar.grid(row=6,column=1,sticky='nsew')
search_btn.grid(row=4,column=0, sticky='nsew', ipadx=5, ipady=5,padx=5, pady=5)
pdf_list.grid(row=6,column=0, sticky='nsew', padx=5, pady=5)
pdf_list_frame.grid(row=6,column=0, sticky='nsew', padx=5, pady=5)
found_pdf_list_frame.grid(row=6,column=2, sticky='nsew', padx=5, pady=5)

#  configs
busca_input.bind("<FocusIn>", lambda args:clear_busca_input_on_click())
buscas_salvas_scrollbar.config(command=buscas_salvas_list.yview)
pdf_list_scrollbar.config(command=pdf_list.yview)
found_pdf_list_scrollbar.config(command=found_pdf_list.yview)
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
   
        
buscas_salvas_list.bind("<<ListboxSelect>>", callback_buscas_salvas)

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
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        open_file(pdf_path,data)
        




pdf_list.bind("<<ListboxSelect>>", callback_pdf_list)
# update list of pdfs
def update_pdf_list():
    try:
        pdf_list.delete(0,tk.END)
    except:
        pass
    global pdf_path
    global pdfs
    pdfs = []
    for file in os.listdir(pdf_path):
        if file.endswith(".pdf"):
            pdfs.append(file)
            pdf_list.insert(tk.END, file)

def load_gif():
    loading_bar = ImageLabel(root) 
    loading_bar.grid(row=0 ,column=2, sticky='nsew', padx=5, pady=5,rowspan=4)

def callback_found_pdf_list(event):
    global pdf_path
    global search_strings
    global current_img
    global current_img_counter
    global loading_bar
    current_img_counter = 0

    current_img=[]
    selection = event.widget.curselection()
    if selection:
        t = threading.Thread(target=load_gif)
        t.start()
        
        files= []
        index = selection[0]
        data = event.widget.get(index)
        files.append(data)
        find_in_pdf(files,search_strings,True)
  
        #open_file(pdf_path,data)



found_pdf_list.bind("<<ListboxSelect>>", callback_found_pdf_list)

def update_found_pdf_list(list):
    try:
        found_pdf_list.delete(0,tk.END)
    except:
        pass
    if len(list)==0:
        return
    for pdf in list:
        found_pdf_list.insert(tk.END, pdf)



def Buscar():
    global pdfs
    global pdf_path
    
    global search_strings
    # buscar btn
    # validation checks
    
   
    print(type(search_strings))
    
    # split by comma into a list 
    search_strings = busca_input.get().split(',')
    print(search_strings)
    if "2. Palavras chave (separe com ,)" in search_strings:
        return
    # remove empty strings
    search_strings = [x for x in search_strings if x != '']
    #remove spaces at the end and start
    for s in range(len(search_strings)):
       search_strings[s] = search_strings[s].rstrip()
       search_strings[s] = search_strings[s].lstrip()
    print(search_strings)
    # returns if nothing is found on input
    if len(search_strings)<1:
        return
    
    if not pdf_path:
        return
    #add to recent searches
   
    update_buscas_salvas(busca_input.get())
    # find in pdf
    update_found_pdf_list(find_in_pdf(pdfs,search_strings,False))     
    #status_bar.configure(text='Nova busca salva!')




class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs -- from:https://stackoverflow.com/questions/43770847/play-an-animated-gif-in-python-with-tkinter"""
    def load(self, im):
        try:
            if isinstance(im, str):
                im = Image.open(im)
            self.loc = 0
            self.frames = []
        except:
            pass
        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
                
        except EOFError:
            pass
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
           
            self.next_frame()
        
    def unload(self):
        print("UNLOADED GIF")
        self.config(image="")
        self.frames = None
    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)
# loading bar
loading_bar = ImageLabel(root) 
loading_bar.grid(row=0 ,column=2, sticky='nsew', padx=5, pady=5,rowspan=4)

#loading_bar.unload()
#on exit save 
def exit_handler():
    # delete temp images
    for img_file in os.scandir(img_path):
        if img_file.name.endswith(".png"):
            os.remove(img_file.path)
    # delete temp pdf
    for pdf_file in os.scandir(pdf_path):
        if pdf_file.name.endswith(".pdf"):
            os.remove(pdf_file.path)
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
root.mainloop()
update_pdf_list() 