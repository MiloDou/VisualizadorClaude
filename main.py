import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import StackFrame, QueueFrame
from ui_components_linked_lists import SinglyLinkedListFrame, CircularLinkedListFrame
from ui_components_double_linked_list import DoublyLinkedListFrame
from ui_components_trees import BinaryTreeFrame, BinarySearchTreeFrame
from file_manager import FileManager


class DataStructureVisualizer(tk.Tk):
    """Aplicación principal para visualizar estructuras de datos."""

    def __init__(self):
        super().__init__()

        self.title("Visualizador de Estructuras de Datos")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Crear menú
        self.create_menu()

        # Crear contenido principal
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear selector de estructura
        self.create_structure_selector()

        # Marco actual activo
        self.current_frame = None

        # Mensaje de bienvenida
        self.show_welcome()

    def create_menu(self):
        """Crear el menú de la aplicación."""
        menu_bar = tk.Menu(self)

        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.new_structure)
        file_menu.add_command(label="Abrir", command=self.load_structure)
        file_menu.add_command(label="Guardar", command=self.save_structure)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.quit)

        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Ayuda
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self.show_about)

        menu_bar.add_cascade(label="Ayuda", menu=help_menu)

        self.config(menu=menu_bar)

    def create_structure_selector(self):
        """Crear menú desplegable para seleccionar tipo de estructura de datos."""
        selector_frame = ttk.Frame(self.content_frame)
        selector_frame.pack(fill=tk.X, pady=10)

        ttk.Label(selector_frame, text="Seleccionar Estructura:").pack(side=tk.LEFT, padx=5)

        self.structure_var = tk.StringVar()
        structures = [
            "Pila",
            "Cola",
            "Lista simplemente ligada",
            "Lista circular",
            "Lista doblemente ligada",
            "Árbol binario",
            "Árbol de búsqueda"
        ]

        structure_combo = ttk.Combobox(selector_frame, textvariable=self.structure_var,
                                       values=structures, state="readonly", width=20)
        structure_combo.pack(side=tk.LEFT, padx=5)
        structure_combo.bind("<<ComboboxSelected>>", self.on_structure_selected)

    def on_structure_selected(self, event):
        """Manejar selección de tipo de estructura de datos."""
        structure_type = self.structure_var.get()

        # Limpiar marco actual si existe
        if self.current_frame:
            # Desvincular eventos existentes antes de destruir
            self.unbind("<Configure>")
            self.current_frame.destroy()

        # Crear nuevo marco basado en la selección
        if structure_type == "Pila":
            self.current_frame = StackFrame(self.content_frame)
        elif structure_type == "Cola":
            self.current_frame = QueueFrame(self.content_frame)
        elif structure_type == "Lista simplemente ligada":
            self.current_frame = SinglyLinkedListFrame(self.content_frame)
        elif structure_type == "Lista circular":
            self.current_frame = CircularLinkedListFrame(self.content_frame)
        elif structure_type == "Lista doblemente ligada":
            self.current_frame = DoublyLinkedListFrame(self.content_frame)
        elif structure_type == "Árbol binario":
            self.current_frame = BinaryTreeFrame(self.content_frame)
        elif structure_type == "Árbol de búsqueda":
            self.current_frame = BinarySearchTreeFrame(self.content_frame)

        # Mostrar el marco
        if self.current_frame:
            self.current_frame.pack(fill=tk.BOTH, expand=True)

            # Crear manejador seguro para redimensionamiento
            def safe_resize_handler(event):
                if self.current_frame and self.current_frame.winfo_exists():
                    try:
                        self.current_frame.update_visualization()
                    except (tk.TclError, AttributeError):
                        # Ignorar silenciosamente errores si el widget ya no existe
                        pass

            # Vincular evento de redimensionamiento para actualizar visualización
            self.bind("<Configure>", safe_resize_handler)

    def new_structure(self):
        """Crear una nueva estructura de datos."""
        if self.current_frame:
            if messagebox.askyesno("Nueva Estructura",
                                   "Esto limpiará la estructura actual. ¿Continuar?"):
                # Desvincular eventos antes de destruir
                self.unbind("<Configure>")
                self.current_frame.destroy()
                self.current_frame = None
                self.structure_var.set("")

    def save_structure(self):
        """Guardar estructura actual en un archivo."""
        if not self.current_frame:
            messagebox.showinfo("Guardar", "No hay estructura para guardar.")
            return

        success = FileManager.save_structure(
            self.current_frame.structure,
            self.structure_var.get()
        )

        if success:
            messagebox.showinfo("Guardar", "Estructura guardada exitosamente.")

    def load_structure(self):
        """Cargar estructura desde un archivo."""
        structure_type, structure = FileManager.load_structure()

        if not structure_type or not structure:
            return

        # Limpiar marco actual si existe
        if self.current_frame:
            # Desvincular eventos existentes antes de destruir
            self.unbind("<Configure>")
            self.current_frame.destroy()

        # Establecer el combobox al tipo de estructura cargado
        self.structure_var.set(structure_type)

        # Crear nuevo marco basado en el tipo de estructura cargado
        if structure_type == "Stack":
            self.current_frame = StackFrame(self.content_frame)
        elif structure_type == "Queue":
            self.current_frame = QueueFrame(self.content_frame)
        elif structure_type == "Singly Linked List":
            self.current_frame = SinglyLinkedListFrame(self.content_frame)
        elif structure_type == "Circular Linked List":
            self.current_frame = CircularLinkedListFrame(self.content_frame)
        elif structure_type == "Doubly Linked List":
            self.current_frame = DoublyLinkedListFrame(self.content_frame)
        elif structure_type == "Binary Tree":
            self.current_frame = BinaryTreeFrame(self.content_frame)
        elif structure_type == "Binary Search Tree":
            self.current_frame = BinarySearchTreeFrame(self.content_frame)

        # Reemplazar la estructura con la cargada
        if self.current_frame:
            self.current_frame.structure = structure
            self.current_frame.update_info()
            self.current_frame.pack(fill=tk.BOTH, expand=True)
            self.current_frame.update_visualization()

            # Crear manejador seguro para redimensionamiento
            def safe_resize_handler(event):
                if self.current_frame and self.current_frame.winfo_exists():
                    try:
                        self.current_frame.update_visualization()
                    except (tk.TclError, AttributeError):
                        # Ignorar silenciosamente errores si el widget ya no existe
                        pass

            # Vincular evento de redimensionamiento para actualizar visualización
            self.bind("<Configure>", safe_resize_handler)

            messagebox.showinfo("Cargar", "Estructura cargada exitosamente.")

    def show_welcome(self):
        """Mostrar marco de mensaje de bienvenida."""
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(welcome_frame,
                  text="Visualizador de Estructuras de Datos",
                  font=("TkDefaultFont", 24, "bold")).pack(pady=(100, 20))

        ttk.Label(welcome_frame,
                  text="Seleccione un tipo de estructura de datos del menú desplegable para comenzar.",
                  font=("TkDefaultFont", 12)).pack(pady=10)

        ttk.Label(welcome_frame,
                  text="Esta herramienta permite visualizar e interactuar con varias estructuras de datos,\n"
                       "ayudando a comprender cómo funcionan.",
                  font=("TkDefaultFont", 10)).pack(pady=10)

        self.current_frame = welcome_frame

    def show_about(self):
        """Mostrar diálogo Acerca de."""
        about_text = "Visualizador de Estructuras de Datos\n\n" \
                     "Creado para el curso de Estructuras de Datos.\n" \
                     "Esta aplicación ayuda a los estudiantes a entender\n" \
                     "diferentes estructuras de datos mediante visualización.\n\n" \
                     "© 2025 - Todos los derechos reservados"

        messagebox.showinfo("Acerca de", about_text)


if __name__ == "__main__":
    app = DataStructureVisualizer()
    app.mainloop()