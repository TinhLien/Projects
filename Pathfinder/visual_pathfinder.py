import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
YELLOW = (255, 255, 0)

class Node:         # keeps track of where it is, different types of nodes etc..
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
    
    def getPos(self):
        return self.row, self.col
    
    def isClosed(self):
        return self.colour == RED
    
    def isOpen(self):
        return self.colour == GREEN
    
    def isBarrier(self):
        return self.colour == BLACK
    
    def isStart(self):
        return self.colour == ORANGE
    
    def isEnd(self):
        return self.colour == PURPLE
    
    def reset(self):
        self.colour = WHITE
    
    def makeClosed(self):
        self.colour = RED
    
    def makeOpen(self):
        self.colour = GREEN
    
    def makeBarrier(self):
        self.colour = BLACK
    
    def makeStart(self):
        self.colour = ORANGE
    
    def makeEnd(self):
        self.colour = PURPLE
    
    def makePath(self):
        self.colour = TURQUOISE
    
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))
    
    def updateNeighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier():     # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier():                       # UP
            self.neighbors.append(grid[self.row - 1][self.col])
    
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier():     # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier():                       # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):        # when comparing two cubes together
        return False
    
def heuristic(p1, p2):          # using manhattan distance to calculate distance from p1 to p2
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def changePath(came_from, current, draw):   # the current node starts at the end node
    while current in came_from:             # we're gonna traverse from the end node back to start node
        current = came_from[current]
        current.makePath()                  # make that part of the path
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))      # count variable so we can break ties when we have two elements in the queue that have the same f-score
    came_from = {}                       # keeps track of what nodes come from where to find best path in the end
    g_score = {spot: float("inf") for row in grid for spot in row}      # keeps track of current shortest distance from start node to this node
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}         # keeps track of the predicted of this node to the end node
    f_score[start] = heuristic(start.getPos(), end.getPos())                # set start of f_score at heuristic(whatever our guess is) from start node to end node

    open_set_hash = {start}             # helps us see whats in the open_set

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]     # getting the node associated with the minimum element in the queue
        open_set_hash.remove(current)

        if current == end:                          # if we're at the end/finished, found the path, we're done
            changePath(came_from, end, draw)
            end.makeEnd()
            start.makeEnd()
            return True

        for neighbor in current.neighbors:          # otherwise, consider all neighbors of current node
            temp_g_score = g_score[current] + 1     # calculate their temp g_score

            if temp_g_score < g_score[neighbor]:    # if less then whatever their g_score is on the table
                came_from[neighbor] = current       # then update that, because we found the better path
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.getPos(), end.getPos())
                if neighbor not in open_set_hash:   # then add in the open_set hash if they're not already in there
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.makeOpen()
        
        draw()

        if current != start:
            current.makeClosed()
    
    return False

def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def gridLines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    
    gridLines(win, rows, width)
    pygame.display.update()

def mousePos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    rows = 50
    grid = makeGrid(rows, width)

    start = None
    end = None
    run = True

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():        # events are anything that is clicked/pressed mouse/keyboard or timer went off
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:   # left mouse button
                pos = pygame.mouse.get_pos()
                row, col = mousePos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.makeStart()

                elif not end and node != start:
                    end = node
                    end.makeEnd()

                elif node != end and node != start:
                    node.makeBarrier()

            elif pygame.mouse.get_pressed()[2]: # right mouse button
                pos = pygame.mouse.get_pos()
                row, col = mousePos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_f:
                    start = None
                    end = None
                    grid = makeGrid(rows, width)

    pygame.quit()

main(WIN, WIDTH)