from AVLTree import AVLTree


tree = AVLTree()

option = 0
while (option != 6):
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
        tree.graphTree()
        
    elif (option == 2):
        name = input("\nIngrese el nombre del Nodo a Eliminar\n")
        tree.deleteNode(name)
        tree.graphTree()
    elif (option == 3):
        name = input("\nIngrese el nombre del Nodo a Buscar\n")
        res = tree.search(name=name)
    elif (option == 4):
        type = input("\nIngrese la categoría del Nodo a Buscar| dejar vacío si no se desea usar\n")
        print("\nIngrese el rango de peso en bytes del Nodo a Buscar | dejar vacío si no se desea usar\n")
        range1 = input("Intervalo inferior:")
        range2 = input("Intervalo superior:")
        
        type = type if len(type) > 0 else None
        range = [int(range1), int(range2)] if len(range1) > 0 and len(range2) > 0 else []
        res = tree.search(type=type, range=range)
    elif (option == 5):
        tree.printLevelOrder()
        print("\n")

 
    if (option == 3 or option == 4 and len(res) > 0):
        
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
            print(f"La altura de {node.name} es:")
            print(tree.getHeight(node.name))
        elif (option == 2):
            print(f"El factor de balance de {node.name} es:")
            print(tree.balance_factor(node))
        elif (option == 3):
            print(f"El padre de {node.name} es:")
            print(node.parent.name)
        elif (option == 4):
            print(f"El abuelo de {node.name} es:")
            print(node.parent.parent.name)
        elif (option == 5):
            print(f"El tio de {node.name} es:")
            padre = node.parent
            abuelo = node.parent.parent
            if (abuelo.left == padre):
                print(abuelo.right.name)
            else:
                print(abuelo.left.name)