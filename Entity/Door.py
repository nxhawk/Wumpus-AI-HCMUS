from Entity.Entity import Entity
from constants import DOOR_IMAGE


class Door(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, DOOR_IMAGE)
