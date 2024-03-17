import imageio as iio
import os

class Node:
    def __init__(self, name, data, type, parent):
        self.parent = parent
        self.left = None
        self.right = None
 
        # Stores the data in the node
        self.name = name
        self.data = iio.imread(data)
        self.type = type
        self.weight = os.path.getsize(data)
 
        # Stores the height of the current tree
        self.height = None
        
    def getComparator(self):
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.name}"