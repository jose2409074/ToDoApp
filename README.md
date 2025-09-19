Aplicación de Gestión de Tareas
Descripción del Proyecto
Este es un gestor de tareas multiplista desarrollado con Python y la biblioteca Tkinter. La aplicación permite a los usuarios organizar sus tareas en diferentes listas, las cuales se guardan de forma persistente para que no se pierdan entre sesiones. El diseño es modular y responsivo, garantizando una interfaz de usuario clara y adaptable.

Características Clave
Gestión de Listas: Crea, visualiza, renombra y elimina listas de tareas.

Gestión de Tareas: Añade, edita, marca como completadas y elimina tareas individuales.

Persistencia de Datos: Todos los datos se guardan automáticamente en un archivo todos.json, asegurando que no se pierdan al cerrar la aplicación.

Diseño Responsivo: La interfaz se adapta dinámicamente al tamaño de la ventana gracias al uso del gestor de geometría grid.

Interfaz de Usuario: Interfaz de usuario intuitiva y visualmente atractiva, mejorada con íconos para cada acción.

Estructura del Proyecto
La arquitectura del proyecto está organizada de forma modular para una mejor claridad y mantenimiento.

.
├── assets/
│   ├── (Archivos .png de los iconos)
│   ├── app_icon.png
│   ├── notes_icon.png
│   ├── ...
├── data/
│   └── todos.json
├── src/
│   ├── __init__.py
│   ├── app.py
│   └── views.py
├── .gitignore
├── main.py
└── requirements.txt


Instalación y Uso
1. Requisitos
El proyecto utiliza la biblioteca Pillow para el manejo de imágenes. Asegúrate de tenerla instalada.

pip install Pillow

2. Ejecutar la Aplicación
Navega a la carpeta principal del proyecto y ejecuta el archivo main.py.

python main.py


Licencia
Este proyecto está bajo la licencia MIT.