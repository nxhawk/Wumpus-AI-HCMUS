from Run.Action import Action


class Base(object):
    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.map_size = 10
        self.cell_matrix = None

        self.agent_cell = None  # initial cell

        self.path = []
        self.action_list = []
        self.score = 0

    def append_event_to_output_file(self, text: str):
        file = open(self.output_filename, 'a')
        file.write(text + '\n')
        file.close()

    def add_action(self, action):
        self.action_list.append(action)
        self.append_event_to_output_file(action.name)

        if action == Action.MOVE_FORWARD:
            self.score -= 10
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.GRAB_GOLD:
            self.score += 100
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.SHOOT:
            self.score -= 100
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.BE_EATEN_BY_WUMPUS:
            self.score -= 10000
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.FALL_INTO_PIT:
            self.score -= 10000
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.CLIMB_OUT_OF_THE_CAVE:
            self.score += 10
            self.append_event_to_output_file('Score: ' + str(self.score))

    def turn_to(self, new_cell):
        if new_cell.map_pos[0] == self.agent_cell.map_pos[0]:
            if new_cell.map_pos[1] - self.agent_cell.map_pos[1] == 1:
                self.add_action(Action.TURN_UP)
            else:
                self.add_action(Action.TURN_DOWN)
        elif new_cell.map_pos[1] == self.agent_cell.map_pos[1]:
            if new_cell.map_pos[0] - self.agent_cell.map_pos[0] == 1:
                self.add_action(Action.TURN_RIGHT)
            else:
                self.add_action(Action.TURN_LEFT)
        else:
            raise TypeError('Error: ' + self.turn_to.__name__)

    def move_to(self, new_cell):
        self.turn_to(new_cell)
        self.add_action(Action.MOVE_FORWARD)
        self.agent_cell = new_cell
