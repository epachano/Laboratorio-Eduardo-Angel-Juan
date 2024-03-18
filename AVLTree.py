from Node import Node
import os 

class AVLTree:
    
    def __init__(self) -> None:
        self.root = None
        
    def readFiles(self):
        for type in os.listdir(f'{os.getcwd()}/archive/data'): 
            for file in os.listdir(f'{os.getcwd()}/archive/data/{type}'):
                self.insertNode(file, f'{os.getcwd()}/archive/data/{type}/{file}', type)

    #Actualizar Altura de un Nodo
    def update_height(self, node):
        if node is not None:
            left_height = node.left.height if node.left else 0 
            right_height = node.right.height if node.right else 0 
            node.height = max(left_height, right_height) + 1

    #Insertar un Nodo y Balancear Árbol
    def insertNode (self, name, data, type):
        if self.root is None:
            self.root = Node(name, data, type, None)
        else:
            self.root = self.insert(self.root, None, name, data, type)
    
    def insert(self, root, parent, name, data, type):
        if root is None:
            root = Node(name, data, type, parent)
            print(f'Insertado Nodo:  {root}')
        elif root.name > name:
            
            root.left = self.insert(root.left, root, name, data, type)
            left_height = root.left.height if root.left else 0
            right_height = root.right.height if root.right else 0
            if abs(left_height - right_height) == 2:
                if name < root.left.name:
                    root = self.Left2Rot(root)
                else:
                    root = self.LeftRot(root)
        elif root.name < name:
            
            root.right = self.insert(root.right, root, name, data, type)
            left_height = root.left.height if root.left else 0
            right_height = root.right.height if root.right else 0
            if abs(left_height - right_height) == 2:
                if name < root.right.name:
                    root = self.RightRot(root)
                else:
                    root = self.Right2Rot(root)
                    
        self.update_height(root)  
        return root  
    
    def Left2Rot (self, root):
        tmpnode = root.left
        root.left = tmpnode.right
        if tmpnode.right:
            tmpnode.right.parent = root
        tmpnode.right = root
        tmpnode.parent = root.parent
        root.parent = tmpnode
        if tmpnode.parent:
            if root.name < tmpnode.parent.name:
                tmpnode.parent.left = tmpnode
            else:
                tmpnode.parent.right = tmpnode
        self.update_height(root)
        self.update_height(tmpnode)
        return tmpnode
    
    # Rotación Doble a la Izquierda
    def Right2Rot (self, root):
        tmpnode = root.right
        root.right = tmpnode.left
        if tmpnode.left:
            tmpnode.left.parent = root
        tmpnode.left = root
        tmpnode.parent = root.parent
        root.parent = tmpnode
        if tmpnode.parent:
            if root.name < tmpnode.parent.name:
                tmpnode.parent.left = tmpnode
            else:
                tmpnode.parent.right = tmpnode
        self.update_height(root)
        self.update_height(tmpnode)
        return tmpnode
    
    # Rotacion a la Izquierda
    def LeftRot (self, root):
        root.left = self.RRR(root.left)
        return self.LLR(root)
    
    # Rotacion a la Derecha
    def RightRot (self, root):
        root.right = self.LLR(root.right)
        return self.RRR(root)
    

    def preOrden (self):
        self.print_preorder(self.root)
    
    def print_preorder(self, root):
        if root:
            parent_name = root.parent.name if root.parent else "NULL"  
            print(f"Node: {root.name}, parent Node: {parent_name}")  
            self.print_preorder(root.left)  
            self.print_preorder(root.right) 
            
    # Busqueda
    def search (self, name=None, type=None, range=[]):
        return self.avl_search (self.root, name, type, range, [])
    
    def avl_search(self, root, name, type, range, list):
        if root is None:
            return list
        else:
            if all([True if name is None else root.name == name,
                  True if type is None else root.type == type,
                  True if len(range) != 2 else root.weight >= range[0] and root.weight <= range[1]]):
                list.append(root)
        
            list = self.avl_search(root.left, name, type, range, list)
            list = self.avl_search(root.right, name, type, range, list)
            return list
    
    # Balancear Árbol para un determinado Nodo
    def balance(self, root):
        first_height = 0
        second_height = 0
        if root.left:
            first_height = root.left.height
        if root.right:
            second_height = root.right.height
        if abs(first_height - second_height) == 2:
            if first_height < second_height:
                rightheight1 = 0
                rightheight2 = 0
                if root.right.right:
                    rightheight2 = root.right.right.height
                if root.right.left:
                    rightheight1 = root.right.left.height
                if rightheight1 > rightheight2:
                    root = self.RightRot(root)
                else:
                    root = self.Right2Rot(root)
            else:
                leftheight1 = 0
                leftheight2 = 0
                if root.left.right:
                    leftheight2 = root.left.right.height
                if root.left.left:
                    leftheight1 = root.left.left.height
                if leftheight1 > leftheight2:
                    root = self.Left2Rot(root)
                else:
                    root = self.LeftRot(root)
        return root
    
    def balance_factor (self, root):
        first_height = 0
        second_height = 0
        if root.left:
            first_height = root.left.height
        if root.right:
            second_height = root.right.height
        return abs(first_height - second_height)
    
    # Eliminar un Nodo del Árbol AVL y balancearlo nuevamente
    def deleteNode (self, name):
        self.delete(self.root, name)
    
    def delete(self, root, name):
        if root:
            if root.name == name:
                if root.right is None and root.left is not None:
                    if root.parent:
                        if root.parent.name < root.name:
                            root.parent.right = root.left
                        else:
                            root.parent.left = root.left
                        self.update_height(root.parent)
                    root.left.parent = root.parent
                    root.left = self.balance(root.left)
                    return root.left
                elif root.left is None and root.right is not None:
                    if root.parent:
                        if root.parent.name < root.name:
                            root.parent.right = root.right
                        else:
                            root.parent.left = root.right
                        self.update_height(root.parent)
                    root.right.parent = root.parent
                    root.right = self.balance(root.right)
                    return root.right
                elif root.left is None and root.right is None:
                    if root.parent:
                        if root.parent.name < root.name:
                            root.parent.right = None
                        else:
                            root.parent.left = None
                        self.update_height(root.parent)
                    root = None
                    return None
                else:
                    tmp_node = root
                    tmp_node = tmp_node.right
                    while tmp_node.left:
                        tmp_node = tmp_node.left
                    val = tmp_node.name
                    root.right = self.delete(root.right, tmp_node.name)
                    root.name = val
                    root = self.balance(root)
            elif root.name < name:
                root.right = self.delete(root.right, name)
                root = self.balance(root)
            elif root.name > name:
                root.left = self.delete(root.left, name)
                root = self.balance(root)
            self.update_height(root)
        return root
    
    def getHeight(self, name):
        results = self.search(name=name)
    
    # Imprimir recorrido por orden de niveles
    def printLevelOrder(self):
        h = self.root.height
        for i in range(1, h+1):
            print("\n-----------------------------------------------------------------------------\n")
            print(f"Nivel {i}")
            print("\n-----------------------------------------------------------------------------\n")
            self.printCurrentLevel(self.root, i)
 
    def printCurrentLevel(self, root, level):
        if root is None:
            return
        if level == 1:
            print(root, end=" | ")
        elif level > 1:
            self.printCurrentLevel(root.left, level-1)
            self.printCurrentLevel(root.right, level-1)
        
 
# Main function to demonstrate AVL tree operations
tree = AVLTree()

#print(tree.search('bike_324.bmp')[0].height)
option = 0
while (option == 6):
    print('''1. Insertar un nodo.
    2. Eliminar un nodo utilizando la métrica dada.
    3. Buscar un nodo utilizando la métrica dada.
    4. Buscar todos los nodos que cumplan los siguientes criterios
    5. Mostrar el recorrido por niveles del árbol (de manera recursiva).
    6. Salir''')
    option = int(input("\nIngrese el número según la opción que desea realizar:\n"))

    if (option == 1):
        dir = input("\nIngrese dirección del archivo de imagen a ingresar\n")
        name = dir.split("\\")[-1]
        type = dir.split("\\")[-2]
        tree.insertNode(name, dir, type)
        
    elif (option == 2):
        name = input("\nIngrese el nombre del Nodo a Eliminar\n")
        tree.deleteNode(name)
    elif (option == 3):
        name = input("\nIngrese el nombre del Nodo a Buscar\n")
        res = tree.search(name=name)
    elif (option == 4):
        type = input("\nIngrese la categoría del Nodo a Buscar| dejar vacío si no se desea usar\n")
        print("\nIngrese el rango de peso en bytes del Nodo a Buscar | dejar vacío si no se desea usar\n")
        range1 = input("Intervalo inferior:")
        range2 = input("Intervalo superior:")
        
        type = type if len(type) > 0 else None
        range = [int(range1, range2)] if len(range1) > 0 and len(range2) > 0 else []
        res = tree.search(type=type, range=range)
    elif (option == 5):
        tree.printLevelOrder()


    if (option == 3 or option == 4):
        
        if (option == 3):
            node = res[0]
        elif (option == 4):
            print(res)
            for i, node in enumerate(res):
                print(f'{i} | {node}')
            num = int(input("\nSeleccione el nodo que desea ejecutar la operación\n"))
            node = res[num]
        
        print('''\n1. Obtener el nivel del nodo.
    2. Obtener el factor de balanceo (equilibrio) del nodo.
    3. Encontrar el padre del nodo.
    4. Encontrar el abuelo del nodo.
    5. Encontrar el tío del nodo.''')
        option = int(input("\nIngrese el número según la opción que desea realizar:\n"))
        
        if (option == 1):
            print(tree.getHeight(node.name))
        elif (option == 2):
            print(tree.balance_factor(node))
        elif (option == 3):
            print(node.parent.name)
        elif (option == 4):
            print(node.parent.parent.name)
        elif (option == 5):
            if (node.parent.left == node):
                print(node.parent.right.name)
            else:
                print(node.parent.left.name)