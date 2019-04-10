# This one is able to find a 'least expensive' path between start and end
# Its reeeeeally dumb
# The grid is counted as equidistant, and it is the same hard_to_get value for each node 
#
# Node() - is a class for node, containing most info about it, as well as neighbour nodes of this node, 
# and distances to them in .costs. Also it has distance to end as .dte and markers for start \ end \ wall



class Node():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.costs = []
        self.is_start = False 
        self.is_end = False
        self.is_wall = False  # isn't really used here, but has some potential
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
        self.dte = max([abs(node.x-self.x), abs(node.y-self.y)])
    

# Create 100x100 grid of nodes
width = 100
height = 100

# Initialize 100x100 grid of nodes
nodes = [ [None] * width for i in range(0,height) ]
for i in range(0,height):
    for j in range(0,width):
        nodes[i][j] = Node(j,i)


# Neighbours finding
for i in range(0,height):
    for j in range(0,width):

        if i >= 1:
            nodes[i][j].neighbours.append(nodes[i-1][j])
            nodes[i][j].costs.append(1)
            if j >= 1:
                nodes[i][j].neighbours.append(nodes[i-1][j-1])
                nodes[i][j].costs.append(1)
            if j <= width-2:
                nodes[i][j].neighbours.append(nodes[i-1][j+1])
                nodes[i][j].costs.append(1)

        if i <= height-2:
            nodes[i][j].neighbours.append(nodes[i+1][j])
            nodes[i][j].costs.append(1)
            if j >= 1:
                nodes[i][j].neighbours.append(nodes[i+1][j-1])
                nodes[i][j].costs.append(1)
            if j <= width-2:
                nodes[i][j].neighbours.append(nodes[i+1][j+1])
                nodes[i][j].costs.append(1)

        if j >= 1:
            nodes[i][j].neighbours.append(nodes[i][j-1])
            nodes[i][j].costs.append(1)
        if j <= width-2:
            nodes[i][j].neighbours.append(nodes[i][j+1])
            nodes[i][j].costs.append(1)
        
# Set start to 0,0
start = nodes[0][0].set_start()

# Set end to 60,20
end = nodes[60][0].set_end()



node = start
path = []
steps = 0
while not(node.is_end):
    steps += 1
    path.append(node)
    score = []
    low_score = width
    low_ind = 0
    for i in range(0,node.ns()):
        if not(node.is_wall):
            node.neighbours[i].get_dte(end)
            score.append( node.neighbours[i].dte + node.costs[i] )
            if score[i] <= low_score:
                low_score = score[i]
                low_ind = i
    node = node.neighbours[low_ind]

print('Looks like im done!')
print('Steps: ',steps)
