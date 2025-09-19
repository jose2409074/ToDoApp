import tkinter as tk
from tkinter import font, messagebox, simpledialog
from PIL import Image, ImageTk
import os

# Este módulo contiene todas las clases de las vistas de la aplicación.
# Para la consideración de división por clases se consideraron las diferentes interfaces, cada clase es una interfaz diferente.

def get_image(filename):
    """Carga una imagen del directorio 'assets'"""
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
    image_path = os.path.join(assets_dir, filename)
    
    if os.path.exists(image_path):
        # Usar un tamaño de 32x32 píxeles para mayor calidad
        return ImageTk.PhotoImage(Image.open(image_path).resize((32, 32), Image.Resampling.LANCZOS))
    else:
        # Devuelve un icono de un placeholder si el archivo no existe
        return None

#Determiné crear esta estructura por la indicación de la actividad sobre tener dinamismo y crear pestañas.
    #Se utilizan principalmente layout grid porque eso me permitió tener una mejor relación de responsividad que pack.
        #Se tuvo que agregar algunos espacios vacíos para mejorar el orden de la estructura. 
class MainMenu(tk.Frame):
    """
    Vista del menú principal que permite crear y ver listas.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(self, text="Gestor de Tareas", font=font.Font(family="Helvetica", size=32, weight="bold"), bg="#f0f0f0", fg="#333333")
        title_label.grid(row=1, column=0, pady=(20, 40))

        buttons_frame = tk.Frame(self, bg="#f0f0f0")
        buttons_frame.grid(row=2, column=0, sticky="nsew", padx=50)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_rowconfigure(1, weight=1)
        
        create_icon = get_image("notes_icon.png")
        create_button = tk.Button(buttons_frame, text="Crear Nueva Lista", font=font.Font(family="Helvetica", size=16), command=self.create_new_list, image=create_icon, compound="left")
        create_button.image = create_icon
        create_button.grid(row=0, column=0, sticky="nsew", pady=(10, 5))

        view_icon = get_image("view_lists_icon.png")
        view_button = tk.Button(buttons_frame, text="Ver Listas Existentes", font=font.Font(family="Helvetica", size=16), command=self.controller.show_lists_view, image=view_icon, compound="left")
        view_button.image = view_icon
        view_button.grid(row=1, column=0, sticky="nsew", pady=(5, 10))

    def create_new_list(self):
        """Diálogo para que el usuario cree una nueva lista."""
        list_name = simpledialog.askstring("Crear Lista", "Ingresa el nombre de la nueva lista:", parent=self)
        if list_name and list_name not in self.controller.task_lists:
            self.controller.add_list(list_name)
            self.controller.show_list_view(list_name)
        elif list_name:
            messagebox.showwarning("Nombre Inválido", "Ese nombre de lista ya existe. Por favor, elige otro.")

class ListsView(tk.Frame):
    """
    Vista que muestra la lista de todas las listas de tareas existentes.
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        back_icon = get_image("back_icon.png")
        back_button = tk.Button(header_frame, text="Menú Principal", command=self.controller.show_main_menu, font=font.Font(family="Helvetica", size=12), image=back_icon, compound="left")
        back_button.image = back_icon
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        title_label = tk.Label(header_frame, text="Listas Existentes", font=font.Font(family="Helvetica", size=24, weight="bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=1, pady=(20, 10))

        lists_canvas = tk.Canvas(self, bg="#B0E0E6", highlightthickness=0)
        lists_scrollbar = tk.Scrollbar(self, orient="vertical", command=lists_canvas.yview)
        lists_canvas.configure(yscrollcommand=lists_scrollbar.set)
        
        lists_scrollbar.grid(row=1, column=1, sticky="ns")
        lists_canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.lists_frame = tk.Frame(lists_canvas, bg="#B0E0E6")
        lists_canvas.create_window((0, 0), window=self.lists_frame, anchor="nw")
        self.lists_frame.bind("<Configure>", lambda e: lists_canvas.configure(scrollregion=lists_canvas.bbox("all")))

        self.load_lists()
    
    def load_lists(self):
        """Muestra todas las listas existentes en la vista."""
        # Limpiar widgets.
        for widget in self.lists_frame.winfo_children():
            widget.destroy()

        if not self.controller.task_lists:
            tk.Label(self.lists_frame, text="No hay listas creadas.", font=font.Font(family="Helvetica", size=14), bg="#B0E0E6").pack(pady=20, fill="x")
        else:
            for list_name in self.controller.task_lists.keys():
                self.create_list_widget(list_name)

    def create_list_widget(self, list_name):
        """Crea un widget para una lista de tareas con botones para ver, renombrar y eliminar."""
        list_widget_frame = tk.Frame(self.lists_frame, bg="#B0E0E6")
        list_widget_frame.pack(fill="x", padx=10, pady=5)
        list_widget_frame.grid_columnconfigure(0, weight=1)

        view_button = tk.Button(list_widget_frame, text=list_name, font=font.Font(family="Helvetica", size=14), command=lambda: self.controller.show_list_view(list_name))
        view_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        
        rename_icon = get_image("rename_list_icon.png")
        rename_button = tk.Button(list_widget_frame, text="Renombrar", command=lambda: self.rename_list_ui(list_name), font=font.Font(family="Helvetica", size=14), image=rename_icon, compound="left")
        rename_button.image = rename_icon
        rename_button.grid(row=0, column=1, sticky="e", padx=(5, 5))

        delete_icon = get_image("delete_task_icon.png")
        delete_button = tk.Button(list_widget_frame, text="Eliminar", command=lambda: self.delete_list_ui(list_name), font=font.Font(family="Helvetica", size=14), image=delete_icon, compound="left")
        delete_button.image = delete_icon
        delete_button.grid(row=0, column=2, sticky="e", padx=(5, 0))

    def rename_list_ui(self, old_name):
        """Abre un diálogo para renombrar una lista."""
        new_name = simpledialog.askstring("Renombrar Lista", f"Renombra la lista '{old_name}':", parent=self)
        if new_name and new_name != old_name:
            if new_name in self.controller.task_lists:
                messagebox.showwarning("Nombre Inválido", "Ese nombre de lista ya existe. Por favor, elige otro.")
            else:
                self.controller.rename_list(old_name, new_name)
                self.load_lists()

    def delete_list_ui(self, list_name):
        """Elimina una lista de la interfaz de usuario y del controlador."""
        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar la lista '{list_name}'?"):
            self.controller.delete_list(list_name)
            self.load_lists() # Recargar la vista para reflejar el cambio

class ListView(tk.Frame):
    """
    Vista que muestra el contenido de una lista de tareas específica.
    """
    def __init__(self, parent, controller, list_name):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.list_name = list_name
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.grid(row=0, column=0, sticky="nsew")
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        back_icon = get_image("back_icon.png")
        back_button = tk.Button(header_frame, text="Volver", command=self.controller.show_lists_view, font=font.Font(family="Helvetica", size=12), image=back_icon, compound="left")
        back_button.image = back_icon
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        title_label = tk.Label(header_frame, text=list_name, font=font.Font(family="Helvetica", size=24, weight="bold"), bg="#f0f0f0", fg="#333333")
        title_label.grid(row=0, column=1, pady=(20, 10))

        input_frame = tk.Frame(self, bg="#f0f0f0")
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.task_entry = tk.Entry(input_frame, font=font.Font(family="Helvetica", size=14))
        self.task_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")

        add_icon = get_image("add_task_icon.png")
        add_button = tk.Button(input_frame, text="Añadir", command=self.add_task, font=font.Font(family="Helvetica", size=14), image=add_icon, compound="left")
        add_button.image = add_icon
        add_button.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        self.task_canvas = tk.Canvas(self, bg="#B0E0E6", highlightthickness=0)
        self.task_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.task_canvas.yview)
        self.task_canvas.configure(yscrollcommand=self.task_scrollbar.set)
        
        self.task_scrollbar.grid(row=2, column=1, sticky="ns", padx=(0, 10))
        self.task_canvas.grid(row=2, column=0, sticky="nsew", padx=(10, 0), pady=10)
        
        self.task_list_frame = tk.Frame(self.task_canvas, bg="#B0E0E6")
        self.task_canvas.create_window((0, 0), window=self.task_list_frame, anchor="nw")
        self.task_list_frame.bind("<Configure>", lambda e: self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all")))

        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        self.load_tasks()

    def add_task(self):
        """Agrega una nueva tarea a la lista actual y la guarda."""
        task = self.task_entry.get()
        if task:
            self.task_entry.delete(0, tk.END)
            self.controller.task_lists[self.list_name].append({"text": task, "completed": False})
            self.controller.save_data()
            self.create_task_widget({"text": task, "completed": False})
        else:
            messagebox.showwarning("Entrada Vacía", "Por favor, escribe una tarea.")

    def create_task_widget(self, task_data):
        """Crea un widget para una tarea individual."""
        task_frame = tk.Frame(self.task_list_frame, bg="#B0E0E6")
        task_frame.grid(sticky="ew", padx=5, pady=5)
        self.task_list_frame.grid_columnconfigure(0, weight=1)

        is_completed = tk.BooleanVar(value=task_data["completed"])
        
        checkbox = tk.Checkbutton(
            task_frame,
            text=task_data["text"],
            font=font.Font(family="Helvetica", size=20),
            bg="#B0E0E6",
            variable=is_completed,
            command=lambda: self.toggle_completed(checkbox, is_completed, task_data["text"])
        )
        checkbox.grid(row=0, column=0, padx=(10, 0), pady=5, sticky="w")
        task_frame.grid_columnconfigure(0, weight=1)
        
        if is_completed.get():
            checkbox.configure(font=font.Font(family="Helvetica", size=20, overstrike=1), fg="green")
            
        # Botón para editar la tarea
        edit_icon = get_image("rename_task_icon.png") # Nuevo icono para editar
        edit_button = tk.Button(task_frame, text="Editar", command=lambda: self.edit_task_ui(task_data), font=font.Font(family="Helvetica", size=14), image=edit_icon, compound="left")
        edit_button.image = edit_icon
        edit_button.grid(row=0, column=1, padx=(0, 5), pady=5, sticky="e")
        
        # Botón para eliminar la tarea
        delete_icon = get_image("delete_task_icon.png")
        delete_button = tk.Button(task_frame, text="Eliminar", command=lambda: self.delete_task(task_frame, task_data["text"]), font=font.Font(family="Helvetica", size=14), image=delete_icon, compound="left")
        delete_button.image = delete_icon
        delete_button.grid(row=0, column=2, padx=(0, 10), pady=5, sticky="e")


    def toggle_completed(self, checkbox, is_completed, text):
        """Alterna el estado de una tarea y lo guarda."""
        if is_completed.get():
            checkbox.configure(font=font.Font(family="Helvetica", size=20, overstrike=1), fg="green")
        else:
            checkbox.configure(font=font.Font(family="Helvetica", size=20), fg="black")
        
        for task in self.controller.task_lists[self.list_name]:
            if task["text"] == text:
                task["completed"] = is_completed.get()
                break
        self.controller.save_data()

    def delete_task(self, task_frame, text):
        """Elimina un widget de tarea y lo quita de la lista y lo guarda."""
        self.controller.task_lists[self.list_name] = [task for task in self.controller.task_lists[self.list_name] if task["text"] != text]
        task_frame.destroy()
        self.controller.save_data()

    def edit_task_ui(self, task_data):
        """
        Abre un diálogo para editar el texto de una tarea.
        """
        old_text = task_data["text"]
        new_text = simpledialog.askstring("Editar Tarea", "Edita el texto de la tarea:", parent=self, initialvalue=old_text)
        
        if new_text and new_text != old_text:
            self.controller.edit_task(self.list_name, old_text, new_text)
            self.load_tasks()
            
    def load_tasks(self):
        """Carga las tareas al mostrar la vista de la lista."""
        # Limpiar los widgets existentes
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()

        for task_data in self.controller.task_lists.get(self.list_name, []):
            self.create_task_widget(task_data)
