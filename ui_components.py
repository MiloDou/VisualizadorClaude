import tkinter as tk
from tkinter import ttk, messagebox


class StructureFrame(ttk.Frame):
    """Marco base para mostrar e interactuar con una estructura de datos."""

    def __init__(self, parent, structure_type):
        super().__init__(parent)
        self.parent = parent
        self.structure_type = structure_type
        self.structure = None
        self.data_type = tk.StringVar(value="int")  # Tipo de dato por defecto

        self._create_widgets()

    def _create_widgets(self):
        # Marco superior de control
        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Selección de tipo de dato
        ttk.Label(control_frame, text="Tipo de dato:").pack(side=tk.LEFT, padx=5)
        data_types = ["int", "float", "str", "bool"]
        data_type_combo = ttk.Combobox(control_frame, textvariable=self.data_type,
                                       values=data_types, state="readonly", width=10)
        data_type_combo.pack(side=tk.LEFT, padx=5)

        # Marco de información de la estructura
        self.info_frame = ttk.LabelFrame(self, text=f"Información de {self.structure_type}")
        self.info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Crear widgets de información específicos según el tipo de estructura
        self._create_info_widgets()

        # Marco de acciones
        actions_frame = ttk.LabelFrame(self, text="Acciones")
        actions_frame.pack(fill=tk.X, padx=10, pady=5)

        # Crear botones de acción según el tipo de estructura
        self._create_action_widgets(actions_frame)

        # Marco de visualización
        self.viz_frame = ttk.LabelFrame(self, text="Visualización")
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Canvas para dibujar la estructura
        self.canvas = tk.Canvas(self.viz_frame, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_info_widgets(self):
        """Crear widgets para mostrar información de la estructura.
        Sobreescribir en subclases."""
        ttk.Label(self.info_frame, text="Tamaño: 0").pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        """Crear botones de acción específicos para la estructura.
        Sobreescribir en subclases."""
        pass

    def convert_input_value(self, value_str):
        """Convertir cadena de entrada al tipo de dato seleccionado."""
        try:
            if self.data_type.get() == "int":
                return int(value_str)
            elif self.data_type.get() == "float":
                return float(value_str)
            elif self.data_type.get() == "bool":
                return value_str.lower() in ['true', 'yes', '1', 't', 'y']
            else:  # Por defecto a string
                return value_str
        except (ValueError, TypeError):
            messagebox.showerror("Error de Tipo",
                                 f"No se puede convertir '{value_str}' a {self.data_type.get()}")
            return None

    def update_visualization(self):
        """Actualizar la visualización de la estructura. Sobreescribir en subclases."""
        pass


class StackFrame(StructureFrame):
    """Marco para operaciones y visualización de Pila."""

    def __init__(self, parent):
        super().__init__(parent, "Pila")
        from structures import Stack
        self.structure = Stack()
        self.update_info()

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Tamaño: 0")
        self.top_var = tk.StringVar(value="Tope: Ninguno")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.top_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Marco de entrada
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Valor:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Botones de acción
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Push", command=self.push).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Pop", command=self.pop).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Peek", command=self.peek).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)

    def push(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.push(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def pop(self):
        if self.structure.is_empty():
            messagebox.showinfo("Pila Vacía", "La pila está vacía")
            return

        value = self.structure.pop()
        messagebox.showinfo("Resultado de Pop", f"Valor extraído: {value}")
        self.update_info()
        self.update_visualization()

    def peek(self):
        if self.structure.is_empty():
            messagebox.showinfo("Pila Vacía", "La pila está vacía")
            return

        value = self.structure.peek()
        messagebox.showinfo("Resultado de Peek", f"Valor en tope: {value}")

    def search(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor a buscar")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            position = self.structure.search(converted_value)
            if position >= 0:
                messagebox.showinfo("Resultado de Búsqueda", f"Valor encontrado en posición: {position}")
            else:
                messagebox.showinfo("Resultado de Búsqueda", "Valor no encontrado")

    def update_info(self):
        self.size_var.set(f"Tamaño: {self.structure.size}")
        top_value = self.structure.peek() if not self.structure.is_empty() else "Ninguno"
        self.top_var.set(f"Tope: {top_value}")

    def update_visualization(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Dibujar la pila desde abajo hacia arriba
        box_width = 100
        box_height = 40
        x_center = self.canvas.winfo_width() // 2
        y_bottom = self.canvas.winfo_height() - 30

        for i, node in enumerate(reversed(nodes)):
            # Calcular posición
            x = x_center - box_width // 2
            y = y_bottom - i * (box_height + 10)

            # Dibujar caja del nodo
            self.canvas.create_rectangle(x, y, x + box_width, y - box_height,
                                         fill="lightblue", outline="black")

            # Dibujar valor
            self.canvas.create_text(x + box_width // 2, y - box_height // 2,
                                    text=str(node.data))

            # Dibujar dirección de memoria
            self.canvas.create_text(x + box_width // 2, y - box_height - 5,
                                    text=f"Mem: {hex(node.memory_address)}",
                                    font=("Arial", 8))

            # Dibujar puntero (excepto para el nodo superior)
            if i < len(nodes) - 1:
                self.canvas.create_line(x_center, y - box_height - 5,
                                        x_center, y - box_height - 10,
                                        arrow=tk.LAST, fill="black")


class QueueFrame(StructureFrame):
    """Marco para operaciones y visualización de Cola."""

    def __init__(self, parent):
        super().__init__(parent, "Cola")
        from structures import Queue
        self.structure = Queue()
        self.update_info()

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Tamaño: 0")
        self.front_var = tk.StringVar(value="Frente: Ninguno")
        self.rear_var = tk.StringVar(value="Final: Ninguno")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.front_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.rear_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Marco de entrada
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Valor:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Botones de acción
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Enqueue", command=self.enqueue).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Dequeue", command=self.dequeue).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Peek", command=self.peek).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)

    def enqueue(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.enqueue(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def dequeue(self):
        if self.structure.is_empty():
            messagebox.showinfo("Cola Vacía", "La cola está vacía")
            return

        value = self.structure.dequeue()
        messagebox.showinfo("Resultado de Dequeue", f"Valor extraído: {value}")
        self.update_info()
        self.update_visualization()

    def peek(self):
        if self.structure.is_empty():
            messagebox.showinfo("Cola Vacía", "La cola está vacía")
            return

        value = self.structure.peek()
        messagebox.showinfo("Resultado de Peek", f"Valor en frente: {value}")

    def search(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor a buscar")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            position = self.structure.search(converted_value)
            if position >= 0:
                messagebox.showinfo("Resultado de Búsqueda", f"Valor encontrado en posición: {position}")
            else:
                messagebox.showinfo("Resultado de Búsqueda", "Valor no encontrado")

    def update_info(self):
        self.size_var.set(f"Tamaño: {self.structure.size}")
        front_value = self.structure.peek() if not self.structure.is_empty() else "Ninguno"
        self.front_var.set(f"Frente: {front_value}")

        # Para el valor final, necesitamos encontrar el último nodo si existe
        if self.structure.rear:
            self.rear_var.set(f"Final: {self.structure.rear.data}")
        else:
            self.rear_var.set("Final: Ninguno")

    def update_visualization(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Dibujar la cola de izquierda a derecha
        box_width = 80
        box_height = 40
        x_left = 30
        y_center = self.canvas.winfo_height() // 2

        for i, node in enumerate(nodes):
            # Calcular posición
            x = x_left + i * (box_width + 20)
            y = y_center - box_height // 2

            # Dibujar caja del nodo
            self.canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                         fill="lightgreen", outline="black")

            # Dibujar valor
            self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                    text=str(node.data))

            # Dibujar dirección de memoria
            self.canvas.create_text(x + box_width // 2, y - 15,
                                    text=f"Mem: {hex(node.memory_address)}",
                                    font=("Arial", 8))

            # Dibujar puntero (excepto para el último nodo)
            if i < len(nodes) - 1:
                self.canvas.create_line(x + box_width, y + box_height // 2,
                                        x + box_width + 20, y + box_height // 2,
                                        arrow=tk.LAST, fill="black")

        # Etiquetar frente y final
        if nodes:
            self.canvas.create_text(x_left + box_width // 2, y_center + box_height // 2 + 25,
                                    text="Frente", font=("Arial", 10, "bold"))

            last_x = x_left + (len(nodes) - 1) * (box_width + 20)
            self.canvas.create_text(last_x + box_width // 2, y_center + box_height // 2 + 25,
                                    text="Final", font=("Arial", 10, "bold"))

# Más componentes de UI para otras estructuras de datos seguirán el mismo patrón
# Serán implementados en artefactos de código posteriores