import pygame

import utils
from Entity.Agent import Agent
from Entity.Cell import Cell
from Entity.Gold import Gold
from constants import SPACING_CELL, CELL_SIZE, NUMBER_CELL, MARGIN, GOLD, AGENT


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
        self.Agent = None

        self.createBoardGame(filename)

    def createBoardGame(self, filename):
        N, _map = utils.Utils.readMapInFile(filename, self.cell_dimension, self.spacing)
        self.matrix_dimension = (N, N)
        self.map = _map

        for row in range(N):
            for col in range(N):
                cell = self.map[row][col]
                # create floor game
                self.Cells.append(Cell(row, col))
                if GOLD in cell:
                    self.Golds.append(Gold(row, col))
                if AGENT in cell and self.Agent is None:
                    self.Agent = Agent(row, col)

    def draw(self, screen: pygame):
        for cell in self.Cells:
            cell.draw(screen)
        for gold in self.Golds:
            gold.draw(screen)
        self.Agent.draw(screen)
