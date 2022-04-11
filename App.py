import tkinter as tk
import sys
import Logic
from GUI import Main

#Carga de DataBase
notes = Logic.Read()
if notes == {}:
    notes = {"1":{"title":"Welcome to Notes", "body":"Start Creating Notes"}}
if not(notes):
    sys.exit(1)

#Iniciar Mainloop de la app GUI
#------------------------------
#Carga de la interfaz
m = Main(notes)
#La ventana va a estar escuchando todos los eventos
m.mainloop()