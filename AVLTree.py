from Node import Node
import os 
import graphviz

os.environ["PATH"] += os.pathsep + f'{os.getcwd()}/Graphviz/bin/'

class AVLTree:
    
    def __init__(self) -> None:
        self.root = None
        # self.readFiles()
        
    def readFiles(self):
        for type in os.listdir(f'{os.getcwd()}/archive/data'): 
            for file in os.listdir(f'{os.getcwd()}/archive/data/{type}'):
                try:
                    self.insertNode(file, f'{os.getcwd()}/archive/data/{type}/{file}', type)
                except:
                    pass

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
        root.left = self.Right2Rot(root.left)
        return self.Left2Rot(root)
    
    # Rotacion a la Derecha
    def RightRot (self, root):
        root.right = self.Left2Rot(root.right)
        return self.Right2Rot(root)
    

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
        
    def graphTree (self):
        tree = graphviz.Digraph()
        tree, counter = self.graph (self.root, 0, tree)
        tree.render('graph', view=True)
    
    def graph (self, root, counter, tree):
        tree.node(f'{root.name}', f'{root.name}')
        
        if root.left:
            tree, counter = self.graph(root.left, counter+1, tree)
            tree.edge(f'{root.name}', f'{root.left.name}', '')
            
            
        if root.right:
            tree, counter = self.graph(root.right, counter+1, tree)
            tree.edge(f'{root.name}', f'{root.right.name}', '')
            
        return tree, counter
    
    def is_rec_eulerian(self, root):
        if root is None:
            return True
        balance = self.balance_factor(root)
        return abs(balance) <= 1 and self.is_rec_eulerian(root.left) and self.is_rec_eulerian(root.right)
    
    def is_rec_complete(self, root, index, node_count):
        if root is None:
            return True

        if index >= node_count:
            return False

        return (self.is_rec_complete(root.left, 2 * index + 1, node_count) and
                self.is_rec_complete(root.right, 2 * index + 2, node_count))

    def count_nodes(self, root):
        if root is None:
            return 0
        return 1 + self.count_nodes(root.left) + self.count_nodes(root.right)

    def is_rec_acyclic(self, node, visited):
        if node is None:
            return True

        if node in visited:
            return False

        visited.add(node)
        return self.is_rec_acyclic(node.left, visited) and self.is_rec_acyclic(node.right, visited)
    
    def is_rec_r_regular(self, root, r, current_degree):
        if root is None:
            return True

        if current_degree == -1:
            current_degree = r if root.left else 0

        if current_degree != r:
            return False

        return (self.is_rec_r_regular(root.left, r, r if root.right else 0) and
                self.is_rec_r_regular(root.right, r, r if root.left else 0))
    
    def find_rec_path(self, root, name, path):
        if root is None:
            return False

        path.append(root.name)

        if root.name == name:
            return True

        if (root.left and self.find_rec_path(root.left, name, path)) or \
           (root.right and self.find_rec_path(root.right, name, path)):
            return True

        path.pop()
        return False
    
    
    def is_complete(self):
        node_count = self.count_nodes(self.root)
        return self.is_rec_complete(self.root, 0, node_count)
    
    def is_acyclic(self):
        visited = set()
        return self.is_rec_acyclic(self.root, visited)
    
    def is_eulerian(self):
        return self.is_rec_eulerian(self.root)
    
    def is_r_regular(self, r):
        return self.is_rec_r_regular(self.root, r, -1)
    
    def path (self, start_name, end_name):
        path = []
        start = self.search(name=start_name)[0]
        end = self.search(name=end_name)[0]
        if self.find_rec_path(start, end, path):
            return path
        return None