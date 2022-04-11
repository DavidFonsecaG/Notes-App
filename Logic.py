import json

#Adicion de una tarea (Create)
def Create(notes, noteId, newNote):
    notes[noteId] = newNote
    #print(notes)
    #print("\n** Tarea {} actualizada **\n".format(tareaId))
    return notes

#Leer DataBase (Aricho .json)
def Read(rutaArchivo='DataBase.json'):
    diccionarioNotes = {}
    try:
        with open(rutaArchivo) as f:
            diccionarioNotes = json.load(f)
    except:
        print("\n** No se pudo cargar la informacion de la capa de datos **\n")
        return False
    return diccionarioNotes
   
#Actualizar una tarea especifica (Update)
def Update(notes, noteId, updatedNote):
    #Revisar los campos que llegan con informacion para actualizar
    for id_campo, campo in updatedNote.items():
        if campo:            
            notes[noteId][id_campo] = campo #Actualiza el campo del diccionario
    #print(notes)
    #print("\n** Tarea {} actualizada **\n".format(tareaId))

#Eliminar una tarea especifica (Delete)
def Delete(notes, noteId):
    notes.pop(noteId)
    #print(notes)    
    #print("\n** Tarea {} eliminada **\n".format(tareaId))

#Operacion de escritura en la capa de datos al cierre de la aplicacion
def Write(notes, rutaArchivo='DataBase.json'):
    #Descargar contenedor de datos con las modificaciones realizadas por la App
    try:
        with open(rutaArchivo, 'w') as archivo_json:
            json.dump(notes, archivo_json)
    except:
        print("\n** Error: No se pudo guardar la informacion en la capa de datos **\n")
        return False
    #Si la escritura fue exitosa
    return True