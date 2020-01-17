#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 07:09:38 2020

@author: vik
"""

import pygame
import random
import copy

pygame.init()
pygame.display.set_caption("Slant Puzzle")
displayScreen = pygame.display.set_mode((600,600))

blue = (0,0,242)
lightblue2 = (110,180,202)
darkblue = (41,26,139)
black = (0,0,0)
yellow = (238,232,67)
green = (52,206,67)
red = (255,0,0)
orange = (255,128,0)
purple = (153,51,255)
lightpurple = (200,185,235)
blue1 = (0,76,153)
blue2 = (51,255,255)
indigo = (75,0,130)
white = (255,255,255)

def in_button(pos, x, y, width, height):
    if pos[0] > x and pos[0] <= x + width and pos[1] > y and pos[1] <= y + height:
        return True
    return False

def get_clicked_node(pos, x, y, spacex, spacey):
    i = int((pos[0] - x)/spacex)
    j = int((pos[1] - y)/spacey)
    return (i, j)

def make_grid(size, diff, cell = None, grid = None):
    # init
    if cell is None:
        cell = (0,0)
        grid = []
        for i in range(size[1]):
            grid.append([0]*size[0])
        
    # make choice and update grid
    orientation = random.choice((1,2))
    new_grid = copy.deepcopy(grid)
    new_grid[cell[1]][cell[0]] = orientation
    
    if no_loops(size, new_grid, cell):
        # base case: made grid with no loops
        if cell == (size[0]-1, size[1]-1):
            return new_grid
        # accross a column
        if cell[1] < size[1] - 1:
            recurse = make_grid(size, diff, (cell[0], cell[1] + 1), new_grid)
            if recurse is not None:
                return recurse
        # down a row
        else:
            recurse = make_grid(size, diff, (cell[0] + 1, 0), new_grid)
            if recurse is not None:
                return recurse

    # try other orientation if found loops
    orientation = list({1,2}.symmetric_difference({orientation}))[0]
    new_grid = copy.deepcopy(grid)
    new_grid[cell[1]][cell[0]] = orientation
    
    if no_loops(size, new_grid, cell):
        # base case: made grid with no loops
        if cell == (size[0]-1, size[1]-1):
            return new_grid
        # accross a column
        if cell[1] < size[1] - 1:
            recurse = make_grid(size, diff, (cell[0], cell[1] + 1), new_grid)
            if recurse is not None:
                return recurse
        # down a row
        else:
            recurse = make_grid(size, diff, (cell[0] + 1, 0), new_grid)
            if recurse is not None:
                return recurse
    else:
        return None
    

def no_loops(size, grid, cell):
    graph = make_graph(size, grid)
    return cycles(graph, cell) is None
    
def cycles(graph, node, path = None):
    # checks for cycles
    for neighb in graph[node]:
        if path is not None and (neighb == path[-2] or neighb in graph[path[-2]]):
            continue
        if path is not None and neighb in path:
            return path
        if path is None:
            new_path = [node, neighb]
        else:
            new_path = path.copy()
            new_path.append(neighb)
        cycle = cycles(graph, neighb, new_path)
        if cycle is not None:
            return cycle
    return None
    
def make_graph(size, grid):
    graph = {}
    for i in range(size[0]):
        for j in range(size[1]):
            (top, bottom, left, right) = False, False, False, False
            if j == size[1] - 1:
                bottom = True
            elif j == 0:
                top = True
            if i == size[0] - 1:
                right = True
            elif i == 0:
                left = True
            if (i, j) not in graph:
                graph[(i, j)] = []
            if grid[j][i] == 1:
                if not top and grid[j-1][i] == 2:
                    graph[(i, j)].append((i, j-1))
                if not top and not right and grid[j-1][i+1] == 1:
                    graph[(i, j)].append((i+1, j-1))
                if not right and grid[j][i+1] == 2:
                    graph[(i, j)].append((i+1, j))
                if not bottom and grid[j+1][i] == 2:
                    graph[(i, j)].append((i, j+1))
                if not bottom and not left and grid[j+1][i-1] == 1:
                    graph[(i, j)].append((i-1, j+1))
                if not left and grid[j][i-1] == 2:
                    graph[(i, j)].append((i-1, j))
            elif grid[j][i] == 2:
                if not top and grid[j-1][i] == 1:
                    graph[(i, j)].append((i, j-1))
                if not top and not left and grid[j-1][i-1] == 2:
                    graph[(i, j)].append((i-1, j-1))
                if not left and grid[j][i-1] == 1:
                    graph[(i, j)].append((i-1, j))
                if not bottom and grid[j+1][i] == 1:
                    graph[(i, j)].append((i, j+1))
                if not bottom and not right and grid[j+1][i+1] == 2:
                    graph[(i, j)].append((i+1, j+1))
                if not right and grid[j][i+1] == 1:
                    graph[(i, j)].append((i+1, j))
    return graph

def make_vertices(size, grid):
    vertices = {}
    for i in range(size[0]+1):
        for j in range(size[1]+1):
            vertices[(i,j)] = 0
            if i > 0 and j > 0 and grid[j-1][i-1] == 2:
                vertices[(i,j)] += 1
            if i < size[0] and j > 0 and grid[j-1][i] == 1:
                vertices[(i,j)] += 1
            if i > 0 and j < size[1] and grid[j][i-1] == 1:
                vertices[(i,j)] += 1
            if i < size[0] and j < size[1] and grid[j][i] == 2:
                vertices[(i,j)] += 1
    return vertices

def remove_vertices(size, vertices, diff):
    # keep a sum hints such that {0:3, 1:2, 2:1, 3:2, 4:3} maps how much each hint is worth
    
    value = {0:3, 1:2, 2:1, 3:2, 4:3}
    
    # make a dict of only the edges
    edges = {}
    for vertex in vertices:
        if 0 in vertex or vertex[0] == size[0] or vertex[1] == size[1]:
            edges[vertex] = vertices[vertex]
            
    # make dict of only the inner vertices
    new_vertices = copy.deepcopy(vertices)
    for vertex in vertices:
        if vertex in edges:
            new_vertices.pop(vertex)
    
    # 36 - 40% remaining out of total (# vertices * 2)
    # 15% - 30% of outside must be filled
    if diff == "hard":
        # remove edge hints first
        percent = random.uniform(0.15, 0.3)
        remaining = int((size[0]*2 + size[1]*2)*percent)
        total = size[0]*2 + size[1]*2
        edge_values = sum(value[x] for x in edges.values())
        
        while not total < remaining:
            to_remove = random.choice(list(edges.keys()))
            edges.pop(to_remove)
            total -= 1
        
        # remove inner hints to reach goal
        percent = random.choice((0.48, 0.5, 0.52, 0.54))
        total_values = sum(value[x] for x in vertices.values()) - edge_values
        total_remaining = int(total_values*percent)
        remaining = total_remaining 
        print(percent)
        print(edges)
        edge_values = sum(value[x] for x in edges.values())
        print(remaining)
        print(edge_values)
        while not total_values <= remaining + edge_values:
            to_remove = random.choice(list(new_vertices.keys()))
            total_values -= value[new_vertices.pop(to_remove)]
            
        new_vertices.update(edges)
            
    elif diff == "easy":
        pass
        
    return new_vertices

def solve():
    pass

def start():
    playing = True
    while playing:
        displayScreen.fill(lightpurple)
        # title
        fontTitle = pygame.font.SysFont('Helvetica', 40)
        textTitle = fontTitle.render("Welcome to the slant game!",False,indigo)
        textleft = 300-(textTitle.get_width()/2)
        texttop = 150-(textTitle.get_height()/2)
        displayScreen.blit(textTitle,(textleft,texttop))
        
        # buttons
        pygame.draw.rect(displayScreen,lightblue2,(150,275,150,75),0)
        pygame.draw.rect(displayScreen,blue1,(300,275,150,75),0)
        pygame.draw.rect(displayScreen,purple,(150,350,150,75),0)
        pygame.draw.rect(displayScreen,indigo,(300,350,150,75),0)
        
        #button texts
        fontTitle = pygame.font.SysFont('Helvetica', 25)
        textTitle = fontTitle.render("8x8 Easy",True,white)
        textleft = 225-(textTitle.get_width()/2)
        texttop = 315-(textTitle.get_height()/2)
        displayScreen.blit(textTitle,(textleft,texttop))
        
        textTitle = fontTitle.render("8x8 Hard",True,white)
        textleft = 375-(textTitle.get_width()/2)
        texttop = 315-(textTitle.get_height()/2)
        displayScreen.blit(textTitle,(textleft,texttop))
        
        textTitle = fontTitle.render("12x10 Easy",True,white)
        textleft = 225-(textTitle.get_width()/2)
        texttop = 385-(textTitle.get_height()/2)
        displayScreen.blit(textTitle,(textleft,texttop))
        
        textTitle = fontTitle.render("12x10 Hard",True,white)
        textleft = 375-(textTitle.get_width()/2)
        texttop = 385-(textTitle.get_height()/2)
        displayScreen.blit(textTitle,(textleft,texttop))
        
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                playing = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if in_button(pos,150,275,150,75):
                    playing = False
                    play((8,8), "easy")
                elif in_button(pos,300,275,150,75):
                    playing = False
                    play((8,8), "hard")
                elif in_button(pos,150,350,150,75):
                    playing = False
                    play((12,10), "easy")
                elif in_button(pos, 300,350,150,75):
                    playing = False
                    play((12,10), "hard")
                
        pygame.display.flip()
        
def play(size, diff):
    
    # update red hints
    def check_hints(cell, orientation):
        (i, j) = cell
        if orientation == 1:
            player_vertices[(i+1, j)] += 1
            player_vertices[(i, j+1)] += 1
        elif orientation == 2:
            player_vertices[(i, j)] += 1
            player_vertices[(i+1, j+1)] += 1
            player_vertices[(i+1, j)] -= 1
            player_vertices[(i, j+1)] -= 1
        else:
            player_vertices[(i, j)] -= 1
            player_vertices[(i+1, j+1)] -= 1
        
        hints_copy = copy.deepcopy(red_hints)
        for m in range(i, i+2):
            for n in range(j, j+2):
                # check if made a mistake
                if player_vertices[(m, n)] > correct_vertices[(m, n)] and (m, n) not in hints_copy and (m, n) in vertices:
                    red_hints.append((m, n))
                # check if fixed a mistake
                if player_vertices[(m, n)] == correct_vertices[(m, n)] and (m, n) in hints_copy and (m, n) in vertices:
                    red_hints.remove((m, n))
        # show updated red hints
        for hint in red_hints:
            pygame.draw.circle(displayScreen,lightpurple,(140 + int(spacex*hint[0]),200 + int(spacey*hint[1])),10,0)
            pygame.draw.circle(displayScreen,red,(140 + int(spacex*hint[0]),200 + int(spacey*hint[1])),10,1)
            fontTitle = pygame.font.SysFont('Arial', 20)
            textTitle = fontTitle.render(str(correct_vertices[hint]),False,red)
            textleft = 141 + int(spacex*hint[0])-(textTitle.get_width()/2)
            texttop = 200 + int(spacey*hint[1])-(textTitle.get_height()/2)
            displayScreen.blit(textTitle,(textleft,texttop))
        # show updated black hints
        for vertex in vertices:
            if vertex not in red_hints:
                pygame.draw.circle(displayScreen,lightpurple,(140 + int(spacex*vertex[0]),200 + int(spacey*vertex[1])),10,0)
                pygame.draw.circle(displayScreen,black,(140 + int(spacex*vertex[0]),200 + int(spacey*vertex[1])),10,1)
                fontTitle = pygame.font.SysFont('Arial', 20)
                textTitle = fontTitle.render(str(vertices[vertex]),False,black)
                textleft = 141 + int(spacex*vertex[0])-(textTitle.get_width()/2)
                texttop = 200 + int(spacey*vertex[1])-(textTitle.get_height()/2)
                displayScreen.blit(textTitle,(textleft,texttop))
    
    # generate a board
    grid = make_grid(size, diff)
    correct_vertices = make_vertices(size, grid)
    vertices = remove_vertices(size, correct_vertices, diff)
    print(grid)
    
    # init game
    player_grid = []
    for i in range(size[1]):
        player_grid.append([0]*size[0])
    player_vertices = {}
    for vertex in correct_vertices:
        player_vertices[vertex] = 0
        
    # init constants 
    spacex = 320/size[0]
    spacey = 320/size[1]
    line_width = spacex - 14
    line_height = spacey - 14
    red_slants = []
    red_hints = []
    
    # draw board
    displayScreen.fill(lightpurple)
    for i in range(size[0]+1):
        x = 140 + i*spacex
        pygame.draw.line(displayScreen,black,(x,200),(x,520),2)
    for i in range(size[1]+1):
        y = 200 + i*spacey
        pygame.draw.line(displayScreen,black,(140,y),(460,y),2)
        
    # func in game 
    def check_cycles(cell, added):
        graph = make_graph(size, player_grid)
        cycle = cycles(graph, cell)
        if cycle is not None:
            for red_cell in cycle:
                (i, j) = red_cell
                x = 147 + i*spacex
                y = 207 + j*spacey
                if player_grid[j][i] == 1:
                    if added:
                        pygame.draw.line(displayScreen,red,(x,y+line_height),(x+line_width,y),2)
                    elif red_cell != cell:
                        pygame.draw.line(displayScreen,black,(x,y+line_height),(x+line_width,y),2)
                else:
                    if added:
                        pygame.draw.line(displayScreen,red,(x,y),(x+line_width,y+line_height),2)
                    elif red_cell != cell:
                        pygame.draw.line(displayScreen,black,(x,y),(x+line_width,y+line_height),2)
                if added:
                    red_slants.append(red_cell)
            if not added:
                for cell in cycle:
                    red_slants.remove(cell)
            
    # show hints
    for vertex in vertices:
        pygame.draw.circle(displayScreen,lightpurple,(140 + int(spacex*vertex[0]),200 + int(spacey*vertex[1])),10,0)
        pygame.draw.circle(displayScreen,black,(140 + int(spacex*vertex[0]),200 + int(spacey*vertex[1])),10,1)
        fontTitle = pygame.font.SysFont('Arial', 20)
        textTitle = fontTitle.render(str(vertices[vertex]),False,black)
        textleft = 141 + int(spacex*vertex[0])-(textTitle.get_width()/2)
        texttop = 200 + int(spacey*vertex[1])-(textTitle.get_height()/2)
        displayScreen.blit(textTitle,(textleft,texttop))

    playing = True
    while playing:
        for event in pygame.event.get():            
            if event.type ==pygame.QUIT:
                playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # check if in grid
                if pos[0] >= 140 and pos[0] <= 459 and pos[1] >= 200 and pos[1] <= 519:
                    # get box that was clicked
                    (i, j) = get_clicked_node(pos, 140, 200, spacex, spacey)
                    if player_grid[j][i] == 0:
                        x = 147 + i*spacex
                        y = 207 + j*spacey
                        pygame.draw.line(displayScreen,black,(x,y+line_height),(x+line_width,y),2)
                        player_grid[j][i] = 1
                        # check for cycles
                        check_cycles((i, j), True)   
                        # check for too many lines
                        check_hints((i, j), 1)                        
                    elif player_grid[j][i] == 1:
                        x = 147 + i*spacex
                        y = 207 + j*spacey
                        pygame.draw.line(displayScreen,lightpurple,(x,y+line_height),(x+line_width,y),3)
                        pygame.draw.line(displayScreen,black,(x,y),(x+line_width,y+line_height),2)
                        # check if cycle was removed
                        check_cycles((i, j), False) 
                        player_grid[j][i] = 2
                        # check for new cycles
                        check_cycles((i, j), True)
                        # check for too many lines or if some hints were fixed
                        check_hints((i, j), 2)
                    elif player_grid[j][i] == 2:
                        x = 147 + i*spacex
                        y = 207 + j*spacey
                        pygame.draw.line(displayScreen,lightpurple,(x,y),(x+line_width,y+line_height),3)
                        # check if cycle was removed
                        check_cycles((i, j), False) 
                        player_grid[j][i] = 0
                        # check if any hints were fixed
                        check_hints((i, j), 0)
                
        pygame.display.flip()
        

start()
pygame.quit()
exit()