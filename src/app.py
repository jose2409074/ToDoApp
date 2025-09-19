import tkinter as tk
from tkinter import messagebox
#Utilicé un archivo json para almacenar las listas de tareas y evitar que se borren en cada cierre de app.
import json
import os
#Utilicé Pillow para mejorar la imagen de la interfaz con iconos
from PIL import Image, ImageTk

from views import MainMenu, ListsView, ListView

class ToDoApp(tk.Tk):
    """
    Clase principal de la aplicación.
    Gestiona el estado de la aplicación, el cambio de vistas y la persistencia de datos.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Gestor de Tareas")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Configurar el ícono de la ventana
        try:
            # Ruta al ícono, se utiliza el directorio assets, como sugiere el docente en la instrucción de la actividad.
            icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'app_icon.png'))
            if os.path.exists(icon_path):
                self.iconphoto(False, tk.PhotoImage(file=icon_path))
            else:
                print("Advertencia: No se encontró el archivo app_icon.png en el directorio assets.")
        except Exception as e:
            print(f"Error al cargar el ícono de la aplicación: {e}")

        #Se agrego la carpeta data, en donde se contiene el archivo todos.json, para almacenar las listas creadas.
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.data_file = os.path.join(self.data_dir, "todos.json")
        self.task_lists = self.load_data()

        self.current_frame = None
        self.show_main_menu()

    def load_data(self):
        """Carga los datos desde el archivo JSON, o devuelve un diccionario vacío si el archivo no existe."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save_data(self):
        """Guarda los datos en el archivo JSON."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.task_lists, file, ensure_ascii=False, indent=4)
        except IOError:
            messagebox.showerror("Error de Guardado", "No se pudo guardar la información.")

    def show_frame(self, frame_class, list_name=None):
        """
        Muestra la vista seleccionada y destruye la vista anterior. Lo vimos en una clase cuando creamos un videojuego de space invaders.
        """
        if self.current_frame:
            self.current_frame.destroy()
        
        if list_name:
            new_frame = frame_class(self, self, list_name)
        else:
            new_frame = frame_class(self, self)
        
        self.current_frame = new_frame
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def show_main_menu(self):
        self.show_frame(MainMenu)

    def show_lists_view(self):
        self.show_frame(ListsView)
    
    def show_list_view(self, list_name):
        self.show_frame(ListView, list_name)
        
    def add_list(self, list_name):
        """Añade una nueva lista vacía."""
        if list_name not in self.task_lists:
            self.task_lists[list_name] = []
            self.save_data()

    def rename_list(self, old_name, new_name):
        """Cambia el nombre de una lista existente y la guarda."""
        if old_name in self.task_lists:
            self.task_lists[new_name] = self.task_lists.pop(old_name)
            self.save_data()
    
    def delete_list(self, list_name):
        """Elimina una lista y la guarda."""
        if list_name in self.task_lists:
            del self.task_lists[list_name]
            self.save_data()
    
    #Fui agregando funciones según las necesidades que no previ en la planeación de la app, esta estructura me resultó muy útil para eso.
    def edit_task(self, list_name, old_text, new_text):
        """
        Edita una tarea en la lista especificada.
        """
        if list_name in self.task_lists:
            for task in self.task_lists[list_name]:
                if task["text"] == old_text:
                    task["text"] = new_text
                    self.save_data()
                    break
