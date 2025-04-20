import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui_components import StructureFrame


class DoublyLinkedListFrame(StructureFrame):
    """Marco para operaciones y visualización de Lista Doblemente Enlazada."""

    def __init__(self, parent):
        super().__init__(parent, "Lista doblemente enlazada")
        from structures import DoublyLinkedList
        self.structure = DoublyLinkedList()
        self.update_info()

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Size: 0")
        self.head_var = tk.StringVar(value="Head: None")
        self.tail_var = tk.StringVar(value="Tail: None")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.head_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.tail_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Marco de entrada
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Value:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Botones de acción para inserción
        insert_frame = ttk.LabelFrame(parent_frame, text="Operaciones de Inserción")
        insert_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(insert_frame, text="Insertar al inicio",
                   command=self.insert_at_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(insert_frame, text="Insertar al Final",
                   command=self.insert_at_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(insert_frame, text="Insertar en posición",
                   command=self.insert_at_position).pack(side=tk.LEFT, padx=5)

        # Botones de acción para eliminación
        delete_frame = ttk.LabelFrame(parent_frame, text="Operaciones de Eliminación")
        delete_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(delete_frame, text="Eliminar al inicio",
                   command=self.delete_from_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(delete_frame, text="Eliminar al final",
                   command=self.delete_from_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(delete_frame, text="Eliminar en posición ",
                   command=self.delete_at_position).pack(side=tk.LEFT, padx=5)

        # Botón de búsqueda
        search_frame = ttk.Frame(parent_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(search_frame, text="Buscar",
                   command=self.search).pack(side=tk.LEFT, padx=5)

    def insert_at_beginning(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_beginning(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def insert_at_end(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_end(converted_value)
            self.update_info()
            self.update_visualization()
            self.value_entry.delete(0, tk.END)

    def insert_at_position(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        position = simpledialog.askinteger("Posición",
                                           f"Ingrese posición (0-{self.structure.size}):",
                                           minvalue=0, maxvalue=self.structure.size)
        if position is None:  # Usuario canceló
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            if self.structure.insert_at_position(position, converted_value):
                self.update_info()
                self.update_visualization()
                self.value_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error de Inserción", "Fallo al insertar en la posición")

    def delete_from_beginning(self):
        if not self.structure.head:
            messagebox.showinfo("Lista Vacía", "La lista está vacía")
            return

        value = self.structure.delete_from_beginning()
        messagebox.showinfo("Resultado de Eliminación", f"Valor eliminado: {value}")
        self.update_info()
        self.update_visualization()

    def delete_from_end(self):
        if not self.structure.head:
            messagebox.showinfo("Lista Vacía", "La lista está vacía")
            return

        value = self.structure.delete_from_end()
        messagebox.showinfo("Resultado de Eliminación", f"Valor eliminado: {value}")
        self.update_info()
        self.update_visualization()

    def delete_at_position(self):
        if not self.structure.head:
            messagebox.showinfo("Lista Vacía", "La lista está vacía")
            return

        position = simpledialog.askinteger("Posición",
                                           f"Ingrese posición (0-{self.structure.size - 1}):",
                                           minvalue=0, maxvalue=self.structure.size - 1)
        if position is None:  # Usuario canceló
            return

        value = self.structure.delete_at_position(position)
        if value is not None:
            messagebox.showinfo("Resultado de Eliminación", f"Valor eliminado: {value}")
            self.update_info()
            self.update_visualization()
        else:
            messagebox.showerror("Error de Eliminación", "Fallo al eliminar en la posición")

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
        head_value = self.structure.head.data if self.structure.head else "Ninguno"
        self.head_var.set(f"Cabeza: {head_value}")
        tail_value = self.structure.tail.data if self.structure.tail else "Ninguno"
        self.tail_var.set(f"Cola: {tail_value}")

    def update_visualization(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Dibujar la lista doblemente enlazada de izquierda a derecha
        box_width = 80
        box_height = 40
        x_left = 30
        y_center = self.canvas.winfo_height() // 2

        for i, node in enumerate(nodes):
            # Calcular posición
            x = x_left + i * (box_width + 80)
            y = y_center - box_height // 2

            # Dibujar caja del nodo
            self.canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                         fill="lightblue", outline="black")

            # Dibujar valor
            self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                    text=str(node.data))

            # Dibujar dirección de memoria
            self.canvas.create_text(x + box_width // 2, y - 15,
                                    text=f"Mem: {hex(node.memory_address)}",
                                    font=("Arial", 8))

            # Dibujar puntero next (excepto para el último nodo)
            if i < len(nodes) - 1:
                self.canvas.create_line(x + box_width, y + box_height // 3,
                                        x + box_width + 80, y + box_height // 3,
                                        arrow=tk.LAST, fill="black")

                # Añadir texto de puntero next
                next_text_x = x + box_width + 40
                self.canvas.create_text(next_text_x, y + box_height // 3 - 10,
                                        text="next", font=("Arial", 8))

            # Dibujar puntero prev (excepto para el primer nodo)
            if i > 0:
                self.canvas.create_line(x, y + 2 * box_height // 3,
                                        x - 80, y + 2 * box_height // 3,
                                        arrow=tk.LAST, fill="blue")

                # Añadir texto de puntero prev
                prev_text_x = x - 40
                self.canvas.create_text(prev_text_x, y + 2 * box_height // 3 - 10,
                                        text="prev", font=("Arial", 8))

        # Marcar el puntero "head"
        if nodes:
            self.canvas.create_text(x_left - 15, y_center - 10, text="head",
                                    anchor=tk.E, font=("Arial", 10, "bold"))
            self.canvas.create_line(x_left - 10, y_center - 10,
                                    x_left, y_center - 10, arrow=tk.LAST)

            # Marcar el puntero "tail"
            last_x = x_left + (len(nodes) - 1) * (box_width + 80)
            self.canvas.create_text(last_x + box_width + 15, y_center - 10,
                                    text="tail", anchor=tk.W, font=("Arial", 10, "bold"))
            self.canvas.create_line(last_x + box_width + 10, y_center - 10,
                                    last_x + box_width, y_center - 10, arrow=tk.LAST)