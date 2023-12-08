from Entity.Entity import Entity
from constants import CELL_IMAGE, CELL_GOLD_IMAGE


class Cell(Entity):
    def __init__(self, row, col, state=0):
        image = CELL_IMAGE if state == 0 else CELL_GOLD_IMAGE
        super().__init__(row, col, image)
