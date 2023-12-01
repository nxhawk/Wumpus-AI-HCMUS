import pygame

import utils
from Entity.Agent import Agent
from Entity.Breeze import Breeze
from Entity.Cell import Cell
from Entity.Gold import Gold
from Entity.Pit import Pit
from Entity.Stench import Stench
from Entity.Wumpus import Wumpus
from constants import *


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
        self.Cells = []
        self.Golds = []
        self.Pits = []
        self.Wumpus = []
        self.Agent = None
        self.Breezes = []
        self.Stenches = []

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

        self.Agent.draw(screen)

    def isDead(self):
        for wum in self.Wumpus:
            if wum.getRC() == self.Agent.getRC():
                return True
        return False

    def move(self):
        pass
