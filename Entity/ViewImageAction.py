from Run.Action import Action
from constants import AGENT_IMAGE, WIDTH, HEIGHT, GOLD_IMAGE, BREEZE_IMAGE, STENCH_IMAGE, ARROW_IMAGE, VICTORY_IMAGE, \
    WUMPUS_IMAGE_KILL
from utils import Utils


def action_to_image(action):
    if action == Action.TURN_RIGHT:
        return AGENT_IMAGE[0]
    elif action == Action.TURN_LEFT:
        return AGENT_IMAGE[1]
    elif action == Action.TURN_UP:
        return AGENT_IMAGE[2]
    elif action == Action.TURN_DOWN:
        return AGENT_IMAGE[3]

    # Climb out the cave
    elif action == Action.CLIMB_OUT_OF_THE_CAVE:
        return VICTORY_IMAGE

    # grab gold action
    elif action == Action.GRAB_GOLD:
        return GOLD_IMAGE

    # infer pit or wumpus
    elif action == Action.PERCEIVE_BREEZE:
        return BREEZE_IMAGE

    elif action == action == Action.PERCEIVE_STENCH:
        return STENCH_IMAGE

    # shoot
    elif action == Action.SHOOT:
        return ARROW_IMAGE[0]

    # kill wumpus
    elif action == Action.KILL_WUMPUS:
        return WUMPUS_IMAGE_KILL

    # fall into pit
    elif action == Action.FALL_INTO_PIT:
        pass

    return AGENT_IMAGE[3]


class ImageAction(object):
    def __init__(self, action):
        self.size = 100
        self.change_action = True

        self.image = Utils.load_image_alpha(action_to_image(action), 0, self.size)
        self.rect = self.image.get_rect()
        self.rect.top = HEIGHT - self.size - 150
        self.rect.left = WIDTH - WIDTH // 5 - 50

    def draw(self, screen):
        if self.change_action:
            screen.blit(self.image, self.rect)