import pygame

import utils
from Entity.Agent import Agent
from Entity.Arrow import Arrow
from Entity.Breeze import Breeze
from Entity.Cell import Cell
from Entity.Gold import Gold
from Entity.Pit import Pit
from Entity.Stench import Stench
from Entity.Wall import Wall
from Entity.Wumpus import Wumpus
from Run.Action import Action
from Run.Solution import Solution
from constants import *

DDX = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def remove_entity(entity, pos):
    flag = -1
    for idx, e in enumerate(entity):
        if e.getRC() == pos:
            flag = idx
            break
    if flag != -1:
        entity.pop(flag)


class Board(object):
    def __init__(self, filename="map1.txt"):
        self.score = 0
        self.spacing = SPACING_CELL
        self.cell_dimension = CELL_SIZE
        self.matrix_dimension = (NUMBER_CELL, NUMBER_CELL)
        self.width = ((self.cell_dimension * self.matrix_dimension[1]) + (self.spacing * (self.matrix_dimension[1] + 1))
                      + MARGIN["LEFT"])
        self.height = (
                (self.cell_dimension * self.matrix_dimension[0]) + (self.spacing * (self.matrix_dimension[0] + 1))
                + MARGIN['TOP'])
        self.map = None
        # other position entity
        self.Walls = []
        self.Cells = []
        self.Golds = []
        self.Pits = []
        self.Wumpus = []
        self.Agent = None
        self.Breezes = []
        self.Stenches = []
        self.Arrow = None
        self.action_list = Solution('./Assets/Input/map1.txt',
                                    './Assets/Output/result1.txt').solve()

        self.createBoardGame(filename)

    def createBoardGame(self, filename):
        N, _map = utils.Utils.readMapInFile(filename, self.cell_dimension, self.spacing)
        self.matrix_dimension = (N, N)
        self.map = _map

        for row in range(N):
            for col in range(N):
                cell = self.map[row][col]
                # create floor game
                self.Cells.append(Cell(row, col, 1) if GOLD in cell else Cell(row, col))
                self.Walls.append(Wall(row, col))
                if GOLD in cell:
                    self.Golds.append(Gold(row, col))
                if AGENT in cell and self.Agent is None:
                    self.Agent = Agent(row, col, N)
                if PIT in cell:
                    self.Pits.append(Pit(row, col))
                if WUMPUS in cell:
                    self.Wumpus.append(Wumpus(row, col))
                if BREEZE in cell:
                    self.Breezes.append(Breeze(row, col))
                if STENCH in cell:
                    self.Stenches.append(Stench(row, col))

    def draw(self, screen: pygame):
        for cell in self.Cells:
            cell.draw(screen)
        for stench in self.Stenches:
            stench.draw(screen)
        for breeze in self.Breezes:
            breeze.draw(screen)
        for gold in self.Golds:
            gold.draw(screen)
        for pit in self.Pits:
            pit.draw(screen)
        for wum in self.Wumpus:
            wum.draw(screen)
        for wall in self.Walls:
            wall.draw(screen)

        self.Agent.draw(screen)
        if self.Arrow is not None:
            self.Arrow.draw(screen)

        remove_entity(self.Walls, self.Agent.getRC())

    def isDead(self):
        for wum in self.Wumpus:
            if wum.getRC() == self.Agent.getRC():
                return True
        return False

    def get_neighborhood_wumpus(self, row, col):
        result = []
        for (d_r, d_c) in DDX:
            new_row = d_r + row
            new_col = d_c + col
            for stench in self.Stenches:
                if stench.getRC() == [new_row, new_col]:
                    result.append(stench)

        return result

    def get_neighborhood_stench(self, row, col):
        result = []
        for (d_r, d_c) in DDX:
            new_row = d_r + row
            new_col = d_c + col
            for wum in self.Wumpus:
                if wum.getRC() == [new_row, new_col]:
                    result.append(wum)

        return result

    def kill_wumpus(self):
        pos_to = self.Agent.getNextPos()
        pos_from = self.Agent.getRC()
        # remove_entity(self.Walls, pos_to)
        remove_entity(self.Wumpus, pos_to)
        stench_around = self.get_neighborhood_wumpus(pos_to[0], pos_to[1])

        for stench in stench_around:
            pos = stench.getRC()
            if len(self.get_neighborhood_stench(pos[0], pos[1])) == 1:
                remove_entity(self.Stenches, pos)

    def move(self):
        self.Arrow = None

        if len(self.action_list) == 0:
            return False
        action = self.action_list.pop(0)
        print(action)

        if action == Action.TURN_RIGHT:
            self.Agent.turn_to(Action.TURN_RIGHT)
        elif action == Action.TURN_LEFT:
            self.Agent.turn_to(Action.TURN_LEFT)
        elif action == Action.TURN_UP:
            self.Agent.turn_to(Action.TURN_UP)
        elif action == Action.TURN_DOWN:
            self.Agent.turn_to(Action.TURN_DOWN)

        # Move forward action
        elif action == Action.MOVE_FORWARD:
            self.Agent.move_forward()

        # grab gold action
        elif action == Action.GRAB_GOLD:
            pos = self.Agent.getRC()
            remove_entity(self.Golds, pos)

        # infer pit or wumpus
        elif action == Action.DETECT_PIT or action == Action.DETECT_WUMPUS:
            pos = self.Agent.getNextPos()
            remove_entity(self.Walls, pos)

        # shoot
        elif action == Action.SHOOT:
            pos_to = self.Agent.getNextPos()
            pos_from = self.Agent.getRC()
            self.Arrow = Arrow(pos_from, pos_to)

        # kill wumpus
        elif action == Action.KILL_WUMPUS:
            self.kill_wumpus()

        return True
