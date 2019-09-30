# Realization of A*-pathfinding algorithm
#
# Node() - is a class for node, containing most info about it, as well as neighbour nodes of this node,
# and distances to them in .costs. Also it has distance to end as .dte and markers for start\end\wall
#
# The "Queue" concept is used here, there is, quite literally, a Queue variable,
# Which is a list, containing nodes with info:
# Queue:
# [[Node object, Node origin, Path length, dte, Score, ID],
#   ..................................................]
#   \ Node object - is a node itself
#   \ Node origin - is from which node the algorithm got to this node (e.g. from (1,0) to (1,1))
#   \ Path length - is a summary path lenght, algorithm covered to get from start to here
#   \ dte - distance to end (between two points)
#   \ Score - is a sum (Path length + dte). The less, the better.

import math


class Node():
    def __init__(self, x, y):
        self.id = (x, y)
        self.x = x
        self.y = y
        self.neighbours = []
        self.costs = []
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.dte = 0

    def ns(self):
        return len(self.neighbours)

    def set_start(self):
        self.is_start = True
        return self

    def set_end(self):
        self.is_end = True
        return self
    # Calculate the euclidean distance between this node and given (end,usually)

    def get_dte(self, node):
        self.dte = math.sqrt((node.x-self.x)**2 + (node.y-self.y)**2)


class Queue():
    def __init__(self, start_node):
        self.queue = [[start_node, start_node, 0,
                       start_node.dte, start_node.dte, start_node.id]]

    def expand(self):
        self.path = []
        while not(self.queue[0][0].is_end):
            # Get info about the expanding node
            self.node = self.queue[0][0]
            self.node_origin = self.queue[0][1]
            self.path_covered = self.queue[0][2]
            # Delete expanding node from list, to reduce backtracking
            self.queue.pop(0)
            self.expand_node()
            # Sorting the Queue to expand the best variant next
            self.queue.sort(key=lambda Querry: Querry[4])
            # Add the first element of the Queue to path to later backtrack the shortest path
            self.path.append(self.queue[0])

    def expand_node(self):
        for i in range(0, self.node.ns()):
            next_node = self.node.neighbours[i]
            next_node.get_dte(end)
            self.score = next_node.dte + self.path_covered + self.node.costs[i]
            self.adjusted = False
            if next_node.is_end:
                self.queue.append([next_node, self.node, self.path_covered +
                                   self.node.costs[i], next_node.dte, self.score, next_node.id])
                break
            if not(next_node.id == self.node_origin.id) and not(next_node.is_wall):
                self.check_queue(next_node, i)
                if not(self.adjusted):
                    self.queue.append([next_node, self.node, self.path_covered +
                                       self.node.costs[i], next_node.dte, self.score, next_node.id])

    def check_queue(self, next_node, i):
        for j in range(0, len(self.queue)):
            if (self.queue[j][0].id == next_node.id) and (self.queue[j][2] >= self.path_covered + self.node.costs[i]):
                self.queue[j][1] = self.node
                self.queue[j][2] = self.path_covered + self.node.costs[i]
                self.queue[j][4] = self.path_covered + \
                    self.node.costs[i] + self.queue[j][0].dte
                self.adjusted = True


# Create 100x100 grid of nodes
width = 100
height = 100

# Initialize 100x100 grid of nodes
nodes = [[None] * width for i in range(0, height)]
for i in range(0, height):
    for j in range(0, width):
        nodes[i][j] = Node(j, i)


# Neighbours&costs finding
for i in range(0, height):
    for j in range(0, width):

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

# Walls setting

nodes[0][1].is_wall = True
nodes[1][1].is_wall = True
nodes[2][1].is_wall = True
nodes[3][1].is_wall = True
nodes[4][1].is_wall = True

# Initialize the program

node = start
path = []
steps = 0

Q = Queue(node)
Q.expand()
path = Q.path
# debuging
# for i in range(0,len(Queue)):
#     print('Node: ',Queue[i][0].id,' From: ',Queue[i][1].id,' Score: ',Queue[i][4])
# print('loop')

print('Looks like im done!')
print('Steps: ', steps)
# for i in range(0,len(path)):
#     print(path[i],'came from:',path[i][1].id)
index = (10, 0)
for i in range(len(path)-1, 0, -1):
    if path[i][0].id == index:
        print(index)
        index = path[i][1].id
