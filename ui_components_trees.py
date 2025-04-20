import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui_components import StructureFrame
import math


class BinaryTreeFrame(StructureFrame):
    """Frame for Binary Tree operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Árbol Binario")
        from structures import BinaryTree
        self.structure = BinaryTree()
        self.update_info()

        # Configurar el canvas con un fondo blanco
        self.canvas.configure(bg="white")

        # Forzar un redibujado inicial después de configuración
        self.canvas.update_idletasks()
        self.after(100, self.update_visualization)

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Tamaño: 0")
        self.height_var = tk.StringVar(value="Altura: 0")
        self.root_var = tk.StringVar(value="Raíz: Ninguna")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.height_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.root_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Input frame
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Valor:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Action buttons
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Insertar raíz",
                   command=self.insert_as_root).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insertar Hijo Izquierdo",
                   command=lambda: self.insert_child(True)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Insertar Hijo Derecho",
                   command=lambda: self.insert_child(False)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar nodo",
                   command=self.delete_node).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Buscar",
                   command=self.search_value).pack(side=tk.LEFT, padx=5)

    def insert_as_root(self):
        """Insert a value as the root of the tree if it's empty."""
        if self.structure.root:
            messagebox.showinfo("Insert Failed", "Tree already has a root. Use other insert methods.")
            return

        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert(None, converted_value)  # None parent means insert at root
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Insert", f"Value {converted_value} inserted as root")

    def insert_child(self, is_left):
        """Insert a value as a left or right child of a parent node."""
        if not self.structure.root:
            messagebox.showinfo("Insert Failed", "Tree is empty. Insert a root first.")
            return

        # Get parent value
        parent_value = simpledialog.askstring("Parent Node", "Enter the value of the parent node:")
        if parent_value is None:  # User cancelled
            return

        try:
            if self.data_type.get() == "int":
                parent_value = int(parent_value)
            elif self.data_type.get() == "float":
                parent_value = float(parent_value)
            elif self.data_type.get() == "bool":
                parent_value = parent_value.lower() in ['true', 'yes', '1', 't', 'y']
        except (ValueError, TypeError):
            messagebox.showerror("Type Error", f"Invalid parent value format")
            return

        # Get new node value
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value for the new node")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            success = self.structure.insert(parent_value, converted_value, is_left)
            if success:
                self.update_info()

                # Esperar a que la interfaz se actualice
                self.canvas.update_idletasks()
                self.update_visualization()

                self.value_entry.delete(0, tk.END)
                side = "left" if is_left else "right"
                messagebox.showinfo("Insert", f"Value {converted_value} inserted as {side} child of {parent_value}")
            else:
                side = "left" if is_left else "right"
                messagebox.showerror("Insert Error",
                                     f"Failed to insert as {side} child. Parent not found or child already exists.")

    def delete_node(self):
        """Delete a node by value."""
        if not self.structure.root:
            messagebox.showinfo("Delete Failed", "Tree is empty.")
            return

        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter the value to delete")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            success = self.structure.delete(converted_value)
            if success:
                messagebox.showinfo("Delete Result", f"Node with value {converted_value} deleted")
                self.update_info()
                self.update_visualization()
                self.value_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Delete Error",
                                     f"Failed to delete node with value {converted_value}. Node not found or has two children.")

    def search_value(self):
        """Search for a value in the tree."""
        if not self.structure.root:
            messagebox.showinfo("Search Result", "Tree is empty")
            return

        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Please enter a value to search")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            found = self.structure.search(converted_value)
            if found:
                messagebox.showinfo("Search Result", f"Value {converted_value} found in the tree")
            else:
                messagebox.showinfo("Search Result", f"Value {converted_value} not found in the tree")

    def update_info(self):
        self.size_var.set(f"Tamaño: {self.structure.size}")
        self.height_var.set(f"Altura: {self.structure.height}")
        root_value = self.structure.root.data if self.structure.root else "Ninguno"
        self.root_var.set(f"Raíz: {root_value}")

    def update_visualization(self):
        # Limpia el canvas
        self.canvas.delete("all")

        # Obtén los nodos por nivel
        nodes_by_level = self.structure.get_nodes_by_level()
        if not nodes_by_level:
            return

        # Asegúrate de que el canvas tiene un tamaño antes de calcular posiciones
        canvas_width = self.canvas.winfo_width() or 800  # Valor por defecto si el ancho es 0
        canvas_height = self.canvas.winfo_height() or 400  # Valor por defecto si la altura es 0

        # Parámetros de visualización
        max_levels = max(nodes_by_level.keys()) + 1
        vertical_spacing = canvas_height / (max_levels + 1)

        # Parámetros de nodo
        node_radius = 25

        # Diccionario para almacenar posiciones de nodos
        node_positions = {}

        # Imprime información de depuración
        print(f"Tamaño de Canvas: {canvas_width}x{canvas_height}")
        print(f"Número de niveles: {max_levels}")

        # Primero calculamos todas las posiciones de los nodos
        for level in range(max_levels):
            if level not in nodes_by_level:
                continue

            nodes = nodes_by_level[level]
            num_nodes = len(nodes)

            # Calculamos el espacio horizontal total disponible
            if level == 0:
                # La raíz está centrada
                horizontal_spacing = canvas_width
                start_x = horizontal_spacing / 2
            else:
                # Los nodos se distribuyen según sus padres
                horizontal_spacing = canvas_width / (2 ** level)
                start_x = horizontal_spacing / 2

            # Calculamos la posición Y para este nivel
            y = (level + 1) * vertical_spacing

            # Posicionamos cada nodo en este nivel
            for i, node in enumerate(nodes):
                if level == 0:
                    # Para la raíz, siempre centramos
                    x = canvas_width / 2
                else:
                    # Para otros niveles, calculamos basado en el índice virtual
                    # dentro de un árbol completo de nivel 'level'
                    virtual_index = self._find_virtual_index(node, nodes_by_level, level)
                    x = start_x + virtual_index * horizontal_spacing

                # Guardamos la posición del nodo
                node_positions[id(node)] = (x, y)

                # Imprime información del nodo
                print(f"Node at level {level}, position {i}: data={node.data}, pos=({x}, {y})")

        # Ahora dibujamos las conexiones primero (para que estén detrás de los nodos)
        for level in range(1, max_levels):  # Comenzamos desde el nivel 1 (los hijos de la raíz)
            if level not in nodes_by_level:
                continue

            nodes = nodes_by_level[level]

            for node in nodes:
                # Encontramos el padre
                parent = self._find_parent(node, nodes_by_level, level)
                if parent:
                    child_x, child_y = node_positions[id(node)]
                    parent_x, parent_y = node_positions[id(parent)]

                    # Dibujamos la conexión diagonal
                    self.canvas.create_line(
                        parent_x, parent_y + node_radius,  # Desde la parte inferior del padre
                        child_x, child_y - node_radius,  # Hasta la parte superior del hijo
                        width=2, fill="black", arrow=tk.LAST
                    )

                    # Añadimos etiqueta "L" o "R"
                    is_left = self._is_left_child(node, parent)
                    child_label = "L" if is_left else "R"

                    # Calculamos el punto medio de la línea para colocar la etiqueta
                    mid_x = (parent_x + child_x) / 2
                    mid_y = (parent_y + child_y) / 2

                    # Añadimos un pequeño desplazamiento para la etiqueta
                    offset_x = 10 if is_left else -10
                    self.canvas.create_text(
                        mid_x + offset_x, mid_y,
                        text=child_label,
                        fill="darkgreen",
                        font=("Arial", 10, "bold")
                    )

        # Finalmente dibujamos los nodos
        for level in range(max_levels):
            if level not in nodes_by_level:
                continue

            nodes = nodes_by_level[level]

            for node in nodes:
                x, y = node_positions[id(node)]

                # Dibujamos el círculo del nodo
                self.canvas.create_oval(
                    x - node_radius, y - node_radius,
                    x + node_radius, y + node_radius,
                    fill="lightgreen", outline="black", width=2
                )

                # Dibujamos el valor del nodo
                try:
                    node_text = str(node.data)
                    self.canvas.create_text(
                        x, y,
                        text=node_text,
                        fill="black",
                        font=("Arial", 12, "bold")
                    )
                except Exception as e:
                    print(f"Error creating text: {e}")
                    self.canvas.create_text(
                        x, y,
                        text="[ERROR]",
                        fill="red",
                        font=("Arial", 10)
                    )

        # Forzar actualización del canvas
        self.canvas.update_idletasks()

    def _find_virtual_index(self, node, nodes_by_level, level):
        """
        Encuentra el índice virtual de un nodo en un nivel como si el árbol fuera completo.
        Esto ayuda a posicionar correctamente los nodos en el canvas.
        """
        if level == 0:
            return 0

        # Encuentra el padre
        parent = self._find_parent(node, nodes_by_level, level)
        if not parent:
            return 0

        # Obtiene el índice virtual del padre
        parent_level = level - 1
        parent_virtual_index = self._find_virtual_index(parent, nodes_by_level, parent_level)

        # Determina si este nodo es hijo izquierdo o derecho
        is_left = self._is_left_child(node, parent)

        # Calcula el índice virtual basado en el padre
        if is_left:
            return parent_virtual_index * 2
        else:
            return parent_virtual_index * 2 + 1

    def _find_parent(self, node, nodes_by_level, level):
        """Encuentra el nodo padre para un nodo dado."""
        if level == 0:
            return None

        parent_level = level - 1
        if parent_level not in nodes_by_level:
            return None

        # Busca entre los nodos del nivel del padre
        for potential_parent in nodes_by_level[parent_level]:
            if potential_parent.left is node or potential_parent.right is node:
                return potential_parent

        return None

    def _is_left_child(self, node, parent):
        """Determina si un nodo es hijo izquierdo o derecho de su padre."""
        if not parent:
            return False

        return parent.left is node


class BinarySearchTreeFrame(StructureFrame):
    """Frame for Binary Search Tree operations and visualization."""

    def __init__(self, parent):
        super().__init__(parent, "Árbol de búsqueda")
        from structures import BinarySearchTree
        self.structure = BinarySearchTree()
        self.update_info()

        # Configurar el canvas con un fondo blanco
        self.canvas.configure(bg="white")

        # Forzar un redibujado inicial después de configuración
        self.canvas.update_idletasks()
        self.after(100, self.update_visualization)

    def _create_info_widgets(self):
        self.size_var = tk.StringVar(value="Tamaño: 0")
        self.height_var = tk.StringVar(value="Altura: 0")
        self.root_var = tk.StringVar(value="Raíz: Ninguna")

        ttk.Label(self.info_frame, textvariable=self.size_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.height_var).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.info_frame, textvariable=self.root_var).pack(anchor=tk.W, padx=5, pady=2)

    def _create_action_widgets(self, parent_frame):
        # Input frame
        input_frame = ttk.Frame(parent_frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(input_frame, text="Valor:").pack(side=tk.LEFT, padx=5)
        self.value_entry = ttk.Entry(input_frame, width=15)
        self.value_entry.pack(side=tk.LEFT, padx=5)

        # Action buttons
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Insertar", command=self.insert_value).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", command=self.delete_value).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Buscar", command=self.search_value).pack(side=tk.LEFT, padx=5)

    def insert_value(self):
        """Insert a value into the BST."""
        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            self.structure.insert(converted_value)
            self.update_info()

            # Esperar a que la interfaz se actualice
            self.canvas.update_idletasks()
            self.update_visualization()

            self.value_entry.delete(0, tk.END)
            messagebox.showinfo("Inserte", f"Valor {converted_value} ")

    def delete_value(self):
        """Delete a value from the BST."""
        if not self.structure.root:
            messagebox.showinfo("Error al Eliminar", "Árbol vacío.")
            return

        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Input Error", "Ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            success = self.structure.delete(converted_value)
            if success:
                messagebox.showinfo("Resultado de Eliminar", f"Nodo con valor {converted_value} eliminado")
                self.update_info()
                self.update_visualization()
                self.value_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error para Eliminar",
                                     f"No se puede eliminar el nodo con valor de {converted_value}. Nodo no encontrado.")

    def search_value(self):
        """Search for a value in the BST."""
        if not self.structure.root:
            messagebox.showinfo("Resultado de la búsqueda", "Árbol vacío")
            return

        value = self.value_entry.get()
        if not value:
            messagebox.showerror("Error", "Ingrese un valor")
            return

        converted_value = self.convert_input_value(value)
        if converted_value is not None:
            found = self.structure.search(converted_value)
            if found:
                messagebox.showinfo("Resultado de la búsqueda", f"Valor {converted_value} ")
            else:
                messagebox.showinfo("Resultado de la búsqueda", f"Valor {converted_value} no encontrado")

    def update_info(self):
        self.size_var.set(f"Tamaño: {self.structure.size}")
        self.height_var.set(f"Altura: {self.structure.height}")
        root_value = self.structure.root.data if self.structure.root else "Ninguno"
        self.root_var.set(f"Raíz: {root_value}")

    def update_visualization(self):
        # Limpia el canvas
        self.canvas.delete("all")

        # Obtén los nodos por nivel
        nodes_by_level = self.structure.get_nodes_by_level()
        if not nodes_by_level:
            return

        # Asegúrate de que el canvas tiene un tamaño antes de calcular posiciones
        canvas_width = self.canvas.winfo_width() or 800  # Valor por defecto si el ancho es 0
        canvas_height = self.canvas.winfo_height() or 400  # Valor por defecto si la altura es 0

        # Parámetros de visualización
        max_levels = max(nodes_by_level.keys()) + 1
        vertical_spacing = canvas_height / (max_levels + 1)

        # Parámetros de nodo
        node_radius = 25

        # Diccionario para almacenar posiciones de nodos
        node_positions = {}

        # Imprime información de depuración
        print(f"tamaño del canvas: {canvas_width}x{canvas_height}")
        print(f"Número de Niveles: {max_levels}")

        # Primero calculamos todas las posiciones de los nodos
        for level in range(max_levels):
            if level not in nodes_by_level:
                continue

            nodes = nodes_by_level[level]
            num_nodes = len(nodes)

            # Para el BST, usamos el mismo algoritmo que para el BinaryTree
            if level == 0:
                # La raíz está centrada
                horizontal_spacing = canvas_width
                start_x = horizontal_spacing / 2
            else:
                # Los nodos se distribuyen según sus padres
                horizontal_spacing = canvas_width / (2 ** level)
                start_x = horizontal_spacing / 2

            # Calculamos la posición Y para este nivel
            y = (level + 1) * vertical_spacing

            # Posicionamos cada nodo en este nivel
            for i, node in enumerate(nodes):
                if level == 0:
                    # Para la raíz, siempre centramos
                    x = canvas_width / 2
                else:
                    # Para BST, calculamos basado en la regla de BST
                    parent = self._find_parent_in_bst(node, nodes_by_level, level)
                    if parent and parent in node_positions:
                        parent_x, _ = node_positions[parent]
                        # Hijo izquierdo o derecho basado en el valor
                        is_left = node.data < parent.data
                        offset = horizontal_spacing / 2
                        x = parent_x - offset if is_left else parent_x + offset
                    else:
                        # Fallback por si no podemos encontrar el padre
                        x = start_x + i * (canvas_width / (num_nodes + 1))

                # Guardamos la posición del nodo
                node_positions[node] = (x, y)

                # Imprime información del nodo
                print(f"Nodo en el nivel {level}, posición {i}: data={node.data}, pos=({x}, {y})")

        # Ahora dibujamos las conexiones primero (para que estén detrás de los nodos)
        for level in range(1, max_levels):  # Comenzamos desde el nivel 1 (los hijos de la raíz)
            if level not in nodes_by_level:
                continue

            nodes = nodes_by_level[level]

            for node in nodes:
                # Encontramos el padre
                parent = self._find_parent_in_bst(node, nodes_by_level, level)
                if parent and parent in node_positions:
                    child_x, child_y = node_positions[node]
                    parent_x, parent_y = node_positions[parent]

                    # Dibujamos la conexión diagonal
                    self.canvas.create_line(
                        parent_x, parent_y + node_radius,  # Desde la parte inferior del padre
                        child_x, child_y - node_radius,  # Hasta la parte superior del hijo
                        width=2, fill="black", arrow=tk.LAST
                    )

                    # Añadimos etiqueta "L" o "R" basado en el valor (regla del BST)
                    is_left = node.data < parent.data
                    child_label = "L" if is_left else "R"

                    # Calculamos el punto medio de la línea para colocar la etiqueta
                    mid_x = (parent_x + child_x) / 2
                    mid_y = (parent_y + child_y) / 2

                    # Añadimos un pequeño desplazamiento para la etiqueta
                    offset_x = 10 if is_left else -10
                    self.canvas.create_text(
                        mid_x + offset_x, mid_y,
                        text=child_label,
                        fill="darkgreen",
                        font=("Arial", 10, "bold")
                    )

        # Finalmente dibujamos los nodos
        for level in range(max_levels):
            if level not in nodes_by_level:
                continue

            nodes = nodes_by_level[level]

            for node in nodes:
                if node not in node_positions:
                    continue

                x, y = node_positions[node]

                # Dibujamos el círculo del nodo
                self.canvas.create_oval(
                    x - node_radius, y - node_radius,
                    x + node_radius, y + node_radius,
                    fill="lightyellow", outline="black", width=2
                )

                # Dibujamos el valor del nodo
                try:
                    node_text = str(node.data)
                    self.canvas.create_text(
                        x, y,
                        text=node_text,
                        fill="black",
                        font=("Arial", 12, "bold")
                    )
                except Exception as e:
                    print(f"Error creating text: {e}")
                    self.canvas.create_text(
                        x, y,
                        text="[ERROR]",
                        fill="red",
                        font=("Arial", 10)
                    )

        # Forzar actualización del canvas
        self.canvas.update_idletasks()

    def _find_parent_in_bst(self, node, nodes_by_level, level):
        """Encuentra el nodo padre en un BST para un nodo dado."""
        if level == 0:
            return None

        parent_level = level - 1
        if parent_level not in nodes_by_level:
            return None

        # Para un BST, el padre es el nodo del nivel superior que tiene
        # a este nodo como hijo izquierdo o derecho
        for potential_parent in nodes_by_level[parent_level]:
            if potential_parent.left is node or potential_parent.right is node:
                return potential_parent

        return None