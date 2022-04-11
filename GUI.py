import tkinter as tk
from tkinter import ttk
import Logic

LARGE_FONT = ('Segoe UI', 13, 'bold')
SMALL_FONT = ('Segoe UI', 9)
TITLE_FONT = ('Segoe UI', 10, 'bold')
PADDING = {'padx': 0, 'pady': 5}

class Info:
    def __init__(self):
        self.notes = {}
        self.listbox = "No Listbox"
        self.textboxCreate = "No Textbox"
        self.textboxUpdate = "No Textbox"
        self.noteTitle = "Titulo"
        self.noteBody = "Cuerpo"         
    
    #----Setters----
    def setNotes(self, notes):
        self.notes = notes
        
    def setListbox(self, listbox):
        self.listbox = listbox
    
    def setTextboxCreate(self, textbox):
        self.textboxCreate = textbox
        
    def setTextboxUpdate(self, textbox):
        self.textboxUpdate = textbox
       
    def setIdTitleBody(self, title):
        self.noteTitle = title
        for campoId, campo in self.notes.items():
            if self.notes[campoId]['title'] == self.noteTitle:
                self.infoId = campoId
                self.noteBody = self.notes[campoId]['body'] 
                break     
    
    #----Getters----
    def getTitleBody(self):
        return self.noteTitle, self.noteBody
    
    def getId(self):
        return self.infoId
    
    #----
    def encapsularInfoFormulario(self, accion):
        if accion == 'Create':
            self.infoTitle = self.textboxCreate.get("1.0","1.50")
            self.infoId = str(self.listbox.size() + 1)
            while self.infoId in self.notes.keys():
                self.infoId = str(int(self.infoId)+1)
            self.infoBody = self.textboxCreate.get("2.0", tk.END)
            while self.infoBody.endswith("\n"):
                self.infoBody = self.infoBody[:-1]
            self.infoNote = {
            "title": self.infoTitle,
            "time": "9:34 PM", 
            "date": "6/14/2021", 
            "body": self.infoBody
            }
        elif accion == 'Update':
            self.infoTitle = self.textboxUpdate.get("1.0","1.50")
            for campoId, campo in self.notes.items():
                if self.notes[campoId]['title'] == self.infoTitle:
                    self.infoId = str(campoId)
                    break
            self.infoBody = self.textboxUpdate.get("2.0", tk.END)
            while self.infoBody.endswith("\n"):
                self.infoBody = self.infoBody[:-1]
            self.infoNote = {
            "title": self.infoTitle,
            "time": "9:34 PM", 
            "date": "6/14/2021", 
            "body": self.infoBody
            }
        elif accion == 'Delete':
            self.infoTitle = "Delete"
            self.infoNote = "Delete"
        
        return self.infoId, self.infoTitle, self.infoNote

class Main(tk.Tk):
    
    info = Info()
    
    def __init__(self, notes, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #----Creando root----
        tk.Tk.title(self, "Notes")
        tk.Tk.protocol(self, "WM_DELETE_WINDOW", self.salirGuardar)
        tk.Tk.resizable(self, False, False)
        tk.Tk.iconbitmap(self, "Icon.ico")
        container = ttk.Frame(self, borderwidth=2, relief='flat', padding=(10,5,10,5))
        container.grid(column=0, row=0)
        #----Depositar diccionario notes en class info----
        self.info.setNotes(notes)
        #----Creating Pages----
        self.frames = {}
        for F in (StartPage, PageCreate, PageUpdate):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        #----Mostar StartPage----
        self.show_frame(StartPage)

    #----Funcion para mostar pagina
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
    #----Funciones Listbox----
    def cargarListbox(self):
        try:
            for campoId, campo in self.info.notes.items():
                self.info.listbox.insert(int(campoId), self.info.notes[campoId]['title'])
        except:
            return
        
    def cargarNoteSeleccionada(self):
        #Extraer informacion de la interfaz
        self.infoTitle = self.info.listbox.get(self.info.listbox.curselection())
        #Depositar informacion en class info
        self.info.setIdTitleBody(self.infoTitle)
        #Limpiar Textbox PageONe
        self.limpiarTextboxUpdate()
        #Depositar informacion en Textbox PageUpdate
        self.descargarTextboxUpdate()
        #Ir a Nota (ir a PageOne)
        self.show_frame(PageUpdate)
    
    #----CRUD functions----    
    def adicionarNote(self):
        self.infoId, self.infoTitle, self.infoNote = self.info.encapsularInfoFormulario('Create')
        if self.infoTitle != "" and self.infoNote != "":
            self.limpiarTextboxCreate()
            self.info.listbox.insert(self.infoId, self.infoTitle)
            Logic.Create(self.info.notes, self.infoId, self.infoNote)
        self.show_frame(StartPage)
            
    def actualizarNote(self):
        self.infoId, self.infoTitle, self.infoNote = self.info.encapsularInfoFormulario('Update')
        if self.infoTitle != "" and self.infoNote != "":
            self.limpiarTextboxUpdate()
            self.info.listbox.delete(0, self.info.listbox.size())
            Logic.Update(self.info.notes, self.infoId, self.infoNote)
            self.cargarListbox()
        self.show_frame(StartPage)
        
    def eliminarNoteUpdate(self):
        self.infoId, self.infoTitle, self.infoNote = self.info.encapsularInfoFormulario('Delete')
        if self.infoTitle != "" and self.infoNote != "":
            self.limpiarTextboxUpdate()
            self.info.listbox.delete(0, self.info.listbox.size())
            Logic.Delete(self.info.notes, self.infoId)
            self.cargarListbox()
        self.show_frame(StartPage)
        
    def eliminarNoteStart(self):
        self.infoTitle = self.info.listbox.get(self.info.listbox.curselection())
        self.info.setIdTitleBody(self.infoTitle)
        self.eliminarNoteUpdate()
        
        
    def salirGuardar(self):
        Logic.Write(self.info.notes)
        tk.Tk.destroy(self)
        
    #----Funciones Textbox----
    def descargarTextboxUpdate(self):
        self.title, self.body = self.info.getTitleBody()
        self.info.textboxUpdate.insert('insert', self.title +"\n", ('title'))
        self.info.textboxUpdate.insert('end', self.body +"\n", ('body'))
        self.info.textboxUpdate.tag_config('title', font=TITLE_FONT)
        
    def limpiarTextboxUpdate(self):
        self.info.textboxUpdate.delete('1.0',tk.END)
        
    def limpiarTextboxCreate(self):
        self.info.textboxCreate.delete('1.0',tk.END)
    
    def CreateNewNote(self):
        self.limpiarTextboxCreate()
        self.show_frame(PageCreate)
        
    def CreateNewNoteCreate(self):
        self.adicionarNote()
        self.limpiarTextboxCreate()
        self.show_frame(PageCreate)
        
    def CreateNewNoteUpdate(self):
        self.actualizarNote()
        self.limpiarTextboxCreate()
        self.show_frame(PageCreate)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #----Creating page widgets----
        #Label
        label = ttk.Label(self, text="Notes", font=LARGE_FONT)
        label.grid(row=0, column=0, sticky='w')
        #List Notes    
        self.listbox = tk.Listbox(self, height=10, width=50, relief='flat', font=SMALL_FONT)
        self.listbox.grid(row=1, column=0)
        self.listbox.bind('<Double-1>', lambda x: controller.cargarNoteSeleccionada()) #Escuchar eventos de listbox
        self.listbox.bind('<Return>', lambda x: controller.cargarNoteSeleccionada()) #Escuchar eventos de listbox
        self.listbox.bind('<Delete>', lambda x: controller.eliminarNoteStart()) #Escuchar eventos de listbox
        #New-Note Button        
        button = ttk.Button(self, text="New Note", command=lambda: controller.CreateNewNote())
        button.grid(row=2, column=0, sticky='e', **PADDING)
        #----Depositar listbox en class info----
        controller.info.setListbox(self.listbox)
        controller.cargarListbox()
        
class PageCreate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #----Creating page widgets----
        #Back-to-Notes Button
        button1 = ttk.Button(self, text="< Notes", command=lambda: controller.adicionarNote())
        button1.grid(row=0, column=0, sticky='w', **PADDING)
        #Textbox Form        
        self.textboxCreate = tk.Text(self, height=10, width=50, relief='flat', font=SMALL_FONT)
        self.textboxCreate.grid(row=1, column=0, columnspan=4)
        #Delete Button         
        button4 = ttk.Button(self, text="Delete", command=lambda: controller.limpiarTextboxCreate())
        button4.grid(row=2, column=2, sticky='e', **PADDING)
        #New Note Button   
        button5 = ttk.Button(self, text="New Note", command=lambda: controller.CreateNewNoteCreate())
        button5.grid(row=2, column=3, sticky='e', **PADDING)
        #----Depositar textbox create en class info----
        controller.info.setTextboxCreate(self.textboxCreate)
        
class PageUpdate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #----Creating page widgets----
        #Back-to-Notes Button
        button1 = ttk.Button(self, text="< Notes", command=lambda: controller.actualizarNote())
        button1.grid(row=0, column=0, sticky='w', **PADDING)
        #Textbox Form        
        self.textboxUpdate = tk.Text(self, height=10, width=50, relief='flat', font=SMALL_FONT)
        self.textboxUpdate.grid(row=1, column=0, columnspan=4)
        #Delete Button         
        button4 = ttk.Button(self, text="Delete", command=lambda: controller.eliminarNoteUpdate())
        button4.grid(row=2, column=2, sticky='e', **PADDING)
        #New Note Button   
        button5 = ttk.Button(self, text="New Note", command=lambda: controller.CreateNewNoteUpdate())
        button5.grid(row=2, column=3, sticky='e', **PADDING)
        #----Depositar textbox update en class info----
        controller.info.setTextboxUpdate(self.textboxUpdate)