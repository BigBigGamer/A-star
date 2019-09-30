import math
class Node():
    def __init__(self,x,y):
        self.id = (x,y)
        self.x = x
        self.y = y
        self.neighbours = []
        self.costs = []
        self.is_start = False 
        self.is_end = False
        self.is_wall = False 
        self.dte = 0
    
    def ns(self):
        return  len(self.neighbours)
    
    def set_start(self):
        self.is_start = True
        return self
    
    def set_end(self):
        self.is_end = True
        return self
    def get_dte(self, node):
        self.dte = math.sqrt((node.x-self.x)**2 + (node.y-self.y)**2)
    

# Create 100x100 grid of nodes
width = 100
height = 100

# Initialize 100x100 grid of nodes
nodes = [ [None] * width for i in range(0,height) ]
for i in range(0,height):
    for j in range(0,width):
        nodes[i][j] = Node(j,i)


# Neighbours&costs finding
for i in range(0,height):
    for j in range(0,width):

        if i >= 1:
            nodes[i][j].neighbours.append(nodes[i-1][j])
            nodes[i][j].costs.append(1)
            if j >= 1:
                nodes[i][j].neighbours.append(nodes[i-1][j-1])
                nodes[i][j].costs.append(math.sqrt(2))
            if j <= width-2:
                nodes[i][j].neighbours.append(nodes[i-1][j+1])
                nodes[i][j].costs.append(math.sqrt(2))

        if i <= height-2:
            nodes[i][j].neighbours.append(nodes[i+1][j])
            nodes[i][j].costs.append(1)
            if j >= 1:
                nodes[i][j].neighbours.append(nodes[i+1][j-1])
                nodes[i][j].costs.append(math.sqrt(2))
            if j <= width-2:
                nodes[i][j].neighbours.append(nodes[i+1][j+1])
                nodes[i][j].costs.append(math.sqrt(2))

        if j >= 1:
            nodes[i][j].neighbours.append(nodes[i][j-1])
            nodes[i][j].costs.append(1)
        if j <= width-2:
            nodes[i][j].neighbours.append(nodes[i][j+1])
            nodes[i][j].costs.append(1)
        
# Set start to 0,0
start = nodes[0][0].set_start()

# Set end to 60,20
end = nodes[0][10].set_end()

start.get_dte(end)

## Walls setting

nodes[0][1].is_wall = True
nodes[1][1].is_wall = True
nodes[2][1].is_wall = True
nodes[3][1].is_wall = True
nodes[4][1].is_wall = True

## Initialize the program 

node = start
path = []
steps = 0

Queue = [[node,node,0,node.dte,0,node.id]]
Queue[0][4] = Queue[0][2] + Queue[0][0].dte

while not(Queue[0][0].is_end):
    if steps>200:
        print("to much steps")
        break
    steps += 1

    ## Get info about the expanding node 
    node = Queue[0][0]
    node_origin = Queue[0][1]
    path_covered = Queue[0][2]

    Queue.pop(0)
    for i in range(0,node.ns()):
        next_node = node.neighbours[i]
        next_node.get_dte(end)
        score = next_node.dte + path_covered + node.costs[i]
        adjusted = False
        if next_node.is_end :
            Queue.append( [ next_node, node, path_covered + node.costs[i], next_node.dte, score, next_node.id] )
            break
        if not(next_node.id == node_origin.id) and not(next_node.is_wall):
            for j in range(0,len(Queue)):
                if (Queue[j][0].id == next_node.id) and (Queue[j][2] >= path_covered + node.costs[i]):
                    Queue[j][1] = node   
                    Queue[j][2] = path_covered + node.costs[i]     
                    Queue[j][4] = path_covered + node.costs[i] + Queue[j][0].dte    
                    adjusted = True
            if not(adjusted):
                Queue.append( [ next_node, node, path_covered + node.costs[i], next_node.dte, score, next_node.id] )
    Queue.sort(key = lambda Querry: Querry[4])
    path.append(Queue[0])

print('Looks like im done!')
print('Steps: ',steps)
index = (10,0)
for i in range(len(path)-1,0,-1):
    if path[i][0].id == index:
        print(index)
        index = path[i][1].id

