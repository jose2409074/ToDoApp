import sys
import os

# Se utiliza la carpeta src para organizar la estructura modular de la app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from app import ToDoApp

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()