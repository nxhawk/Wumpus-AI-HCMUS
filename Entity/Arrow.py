from Entity.Entity import Entity
from constants import ARROW_IMAGE


class Arrow(Entity):
    def __init__(self, row, col, direction='LEFT'):
        image = ARROW_IMAGE[1]
        if direction == 'RIGHT':
            image = ARROW_IMAGE[0]
        elif direction == 'UP':
            image = ARROW_IMAGE[2]
        elif direction == 'DOWN':
            image = ARROW_IMAGE[3]
        super().__init__(row, col, image)
