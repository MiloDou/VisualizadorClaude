import tkinter as tk
from tkinter import ttk, messagebox
from ui_components import StructureFrame


class SinglyLinkedListFrame(StructureFrame):
    """Marco para operaciones y visualización de Lista Enlazada Simple."""

    def __init__(self, parent):
        super().__init__(parent, "Lista Enlazada Simple")
        from structures import SinglyLinkedList
        self.structure = SinglyLinkedList()
        self.update_info()

        # Configurar el canvas con un fondo blanco
        self.canvas.configure(bg="white")

        # Forzar un redibujado inicial después de configuración
        self.canvas.update_idletasks()
        self.after(100, self.update_visualization)

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Tamaño: 0")
        self.head_var = tk.StringVar(value="Cabeza: Ninguna")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.head_var).pack(anchor=tk.W, padx=5, pady=2)

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

        ttk.Button(button_frame, text="Insertar al inicio",
                   command=self.insert_at_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insertar al final",
                   command=self.insert_at_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar desde el inicio",
                   command=self.delete_from_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar al final",
                   command=self.delete_from_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Buscar",
                   command=self.search).pack(side=tk.LEFT, padx=5)

    def insert_at_beginning(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_beginning(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insertar", f"Valor {converted_value} insertado al inicio")

    def insert_at_end(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_end(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insertar", f"Valor {converted_value} insertado al final")

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

    def search(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor para buscar")
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

    def update_visualization(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        # Obtener los nodos
        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Asegurarse de que el canvas tiene un tamaño antes de calcular posiciones
        canvas_width = self.canvas.winfo_width() or 400  # Valor por defecto si el ancho es 0
        canvas_height = self.canvas.winfo_height() or 200  # Valor por defecto si la altura es 0

        # Dibujar la lista enlazada de izquierda a derecha
        box_width = 80
        box_height = 40
        x_left = 80  # Aumentado desde 30 para mover a la derecha
        y_center = canvas_height // 2

        # Imprimir información de depuración
        print(f"Tamaño del canvas: {canvas_width}x{canvas_height}")
        print(f"Número de nodos: {len(nodes)}")
        print(f"Datos de nodos: {[str(node.data) for node in nodes]}")

        for i, node in enumerate(nodes):
            # Calcular la posición
            x = x_left + i * (box_width + 50)
            y = y_center - box_height // 2

            # Dibujar la caja del nodo
            node_id = self.canvas.create_rectangle(x, y, x + box_width, y + box_height,
                                                   fill="lightyellow", outline="black", width=2)

            # Dibujar el valor - asegurarse de que sea una cadena y usar color negro
            try:
                node_text = str(node.data)
                text_id = self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                                  text=node_text, fill="black", font=("Arial", 12, "bold"))
                print(f"Texto creado '{node_text}' con ID {text_id} en ({x + box_width // 2}, {y + box_height // 2})")
            except Exception as e:
                print(f"Error creando texto: {e}")
                # Intentar un texto genérico si falla la conversión
                self.canvas.create_text(x + box_width // 2, y + box_height // 2,
                                        text="[ERROR]", fill="red")

            # Dibujar el puntero (excepto para el último nodo)
            if i < len(nodes) - 1:
                self.canvas.create_line(x + box_width, y + box_height // 2,
                                        x + box_width + 50, y + box_height // 2,
                                        arrow=tk.LAST, fill="black", width=2)

                # Añadir texto para el puntero "siguiente"
                next_text_x = x + box_width + 25
                self.canvas.create_text(next_text_x, y + box_height // 2 - 15,
                                        text="siguiente", fill="darkgreen", font=("Arial", 8))

        # Marcar el puntero "cabeza"
        if nodes:
            self.canvas.create_text(x_left - 25, y_center, text="cabeza",
                                    anchor=tk.E, fill="red", font=("Arial", 10, "bold"))
            self.canvas.create_line(x_left - 20, y_center,
                                    x_left, y_center, arrow=tk.LAST, fill="red", width=2)

        # Forzar actualización del canvas
        self.canvas.update_idletasks()


class CircularLinkedListFrame(StructureFrame):
    """Marco para operaciones y visualización de Lista Enlazada Circular."""

    def __init__(self, parent):
        super().__init__(parent, "Lista Enlazada Circular")
        from structures import CircularLinkedList
        self.structure = CircularLinkedList()
        self.update_info()

        # Configurar el canvas con un fondo blanco
        self.canvas.configure(bg="white")

        # Forzar un redibujado inicial después de configuración
        self.canvas.update_idletasks()
        self.after(100, self.update_visualization)

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Tamaño: 0")
        self.head_var = tk.StringVar(value="Cabeza: Ninguna")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.head_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Marco de entrada
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Valor:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Botones de acción
        button_frame1 = ttk.Frame(parent_frame)
        button_frame1.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame1, text="Insertar al inicio",
                   command=self.insert_at_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Insertar al final",
                   command=self.insert_at_end).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Eliminar desde el inicio",
                   command=self.delete_from_beginning).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame1, text="Eliminar al final",
                   command=self.delete_from_end).pack(side=tk.LEFT, padx=5)

        button_frame2 = ttk.Frame(parent_frame)
        button_frame2.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame2, text="Buscar",
                   command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="Rotar a la Izquierda",
                   command=self.rotate_left).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame2, text="Rotar a la Derecha",
                   command=self.rotate_right).pack(side=tk.LEFT, padx=5)

    def insert_at_beginning(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_beginning(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insertar", f"Valor {converted_value} insertado al inicio")

    def insert_at_end(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert_at_end(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insertar", f"Valor {converted_value} insertado al final")

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

    def search(self):
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error de Entrada", "Por favor ingrese un valor para buscar")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            position = self.structure.search(converted_value)
            if position >= 0:
                messagebox.showinfo("Resultado de Búsqueda", f"Valor encontrado en posición: {position}")
            else:
                messagebox.showinfo("Resultado de Búsqueda", "Valor no encontrado")

    def rotate_left(self):
        if not self.structure.head:
            messagebox.showinfo("Lista Vacía", "La lista está vacía")
            return

        self.structure.rotate_left()
        self.update_info()
        self.update_visualization()
        messagebox.showinfo("Rotar a la Izquierda", "La lista ha sido rotada a la izquierda")

    def rotate_right(self):
        if not self.structure.head:
            messagebox.showinfo("Lista Vacía", "La lista está vacía")
            return

        self.structure.rotate_right()
        self.update_info()
        self.update_visualization()
        messagebox.showinfo("Rotar a la Derecha", "La lista ha sido rotada a la derecha")

    def update_info(self):
        self.size_var.set(f"Tamaño: {self.structure.size}")
        head_value = self.structure.head.data if self.structure.head else "Ninguno"
        self.head_var.set(f"Cabeza: {head_value}")

    def update_visualization(self):
        # Limpiar el canvas
        self.canvas.delete("all")

        nodes = self.structure.get_nodes()
        if not nodes:
            return

        # Asegurarse de que el canvas tiene un tamaño antes de calcular posiciones
        canvas_width = self.canvas.winfo_width() or 400  # Valor por defecto si el ancho es 0
        canvas_height = self.canvas.winfo_height() or 200  # Valor por defecto si la altura es 0

        # Dibujar lista enlazada circular en un círculo
        center_x = canvas_width // 2
        center_y = canvas_height // 2
        radius = min(center_x, center_y) - 70  # Reducido para dejar más espacio

        # Imprimir información de depuración
        print(f"Tamaño del canvas: {canvas_width}x{canvas_height}")
        print(f"Centro: ({center_x}, {center_y}), Radio: {radius}")
        print(f"Número de nodos: {len(nodes)}")
        print(f"Datos de nodos: {[str(node.data) for node in nodes]}")

        # Calcular posiciones para nodos
        node_positions = []
        for i in range(len(nodes)):
            angle = 2 * 3.14159 * i / len(nodes)
            x = center_x + radius * (math_cos := [1, 0, -1, 0])[int(angle // (3.14159 / 2))]
            y = center_y + radius * (math_sin := [0, 1, 0, -1])[int(angle // (3.14159 / 2))]
            node_positions.append((x, y))

        # Dibujar nodos
        box_width = 60
        box_height = 40
        for i, node in enumerate(nodes):
            x, y = node_positions[i]

            # Dibujar caja del nodo
            x1 = x - box_width // 2
            y1 = y - box_height // 2
            x2 = x + box_width // 2
            y2 = y + box_height // 2

            self.canvas.create_rectangle(x1, y1, x2, y2,
                                         fill="lightpink", outline="black", width=2)

            # Dibujar valor - asegurarse de que sea una cadena y usar color negro
            try:
                node_text = str(node.data)
                text_id = self.canvas.create_text(x, y, text=node_text,
                                                  fill="black", font=("Arial", 12, "bold"))
                print(f"Texto creado '{node_text}' con ID {text_id} en ({x}, {y})")
            except Exception as e:
                print(f"Error creando texto: {e}")
                # Intentar un texto genérico si falla la conversión
                self.canvas.create_text(x, y, text="[ERROR]", fill="red")

        # Dibujar conexiones entre nodos
        for i in range(len(nodes)):
            start_x, start_y = node_positions[i]
            end_x, end_y = node_positions[(i + 1) % len(nodes)]

            # Calcular la dirección desde inicio hasta fin
            dx = end_x - start_x
            dy = end_y - start_y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            # Calcular puntos de inicio y fin para la flecha
            if dist > 0:
                nx = dx / dist
                ny = dy / dist
            else:
                nx, ny = 0, 0

            # Ajustar puntos de inicio y fin para estar en los límites de la caja
            start_x = start_x + nx * (box_width // 2)
            start_y = start_y + ny * (box_height // 2)
            end_x = end_x - nx * (box_width // 2)
            end_y = end_y - ny * (box_height // 2)

            # Dibujar la flecha
            self.canvas.create_line(start_x, start_y, end_x, end_y,
                                    arrow=tk.LAST, fill="black", width=2)

            # Añadir etiqueta "siguiente" a mitad de camino
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            offset_x = -ny * 10  # Desplazamiento perpendicular para el texto
            offset_y = nx * 10
            self.canvas.create_text(mid_x + offset_x, mid_y + offset_y,
                                    text="siguiente", fill="darkgreen", font=("Arial", 8))

        # Marcar el puntero "cabeza"
        if nodes:
            head_x, head_y = node_positions[0]
            # Mover el texto de cabeza a una mejor posición
            head_text_x = center_x
            head_text_y = center_y - radius - 20  # Movido hacia arriba para evitar superposición

            self.canvas.create_text(head_text_x, head_text_y, text="cabeza",
                                    font=("Arial", 10, "bold"), fill="red")
            self.canvas.create_line(head_text_x, head_text_y + 10,
                                    head_x, head_y - box_height // 2,
                                    arrow=tk.LAST, dash=(4, 2), fill="red", width=2)

        # Forzar actualización del canvas
        self.canvas.update_idletasks()