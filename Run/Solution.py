from Run.Action import Action
from Run.Base import Base
from Run.Cell import Cell
from Run.CellType import CellType
from Run.KnowledgeBase import KnowledgeBase


class Solution(Base):
    def __init__(self, input_filename, output_filename):
        super().__init__(output_filename)
        self.cave_cell: Cell = Cell(-1, -1, 10, CellType.EMPTY.value)
        self.KB = KnowledgeBase()

        self.read_map(input_filename)

    def read_map(self, filename):
        file = open(filename, 'r')

        self.map_size = int(file.readline())
        raw_map = [line.split('.') for line in file.read().splitlines()]

        self.cell_matrix = [[None for _ in range(self.map_size)] for _ in range(self.map_size)]
        for row in range(self.map_size):
            for col in range(self.map_size):
                self.cell_matrix[row][col] = Cell(row, col, self.map_size, raw_map[row][col])
                if CellType.AGENT.value in raw_map[row][col]:
                    self.agent_cell = self.cell_matrix[row][col]
                    self.agent_cell.update_parent(self.cave_cell)

        file.close()

    def add_KB(self, cell: Cell):
        adj_cell_list: list[Cell] = cell.get_adj_cell(self.cell_matrix)

        # BASE KNOWLEDGE: (P ^ -W) v (-P ^ W)
        # P ^ -W
        sign_pit = '-'
        if cell.exist_Entity(1):
            self.KB.add_clause([cell.get_literal(CellType.WUMPUS, '-')])
            sign_pit = '+'
        self.KB.add_clause([cell.get_literal(CellType.PIT, sign_pit)])
        # -P ^ W
        sign_wumpus = '-'
        if cell.exist_Entity(2):
            self.KB.add_clause([cell.get_literal(CellType.PIT, '-')])
            sign_wumpus = '+'
        self.KB.add_clause([cell.get_literal(CellType.WUMPUS, sign_wumpus)])

        # Check the above constraint.
        if sign_pit == sign_wumpus == '+':
            raise TypeError('Pit and Wumpus can not appear at the same cell.')

        # PL: Breeze?
        sign = '-'
        if cell.exist_Entity(3):
            sign = '+'
        self.KB.add_clause([cell.get_literal(CellType.BREEZE, sign)])

        # PL: Stench?
        sign = '-'
        if cell.exist_Entity(4):
            sign = '+'
        self.KB.add_clause([cell.get_literal(CellType.STENCH, sign)])

        # If this cell have Breeze
        # BASE KNOWLEDGE: B <=> Pa v Pb v Pc v Pd
        if cell.exist_Entity(3):
            # (B => Pa v Pb v Pc v Pd) <=> (-B v Pa v Pb v Pc v Pd)
            clause = [cell.get_literal(CellType.BREEZE, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(CellType.PIT, '+'))
            self.KB.add_clause(clause)

            # (Pa v Pb v Pc v Pd => B) <=> ((-Pa ^ -Pb ^ -Pc ^ -Pd) v B)
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(CellType.BREEZE, '+'), adj_cell.get_literal(CellType.PIT, '-')]
                self.KB.add_clause(clause)

        else:
            # This cell no have Breeze
            # BASE KNOWLEDGE: -Pa ^ -Pb ^ -Pc ^ -Pd
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(CellType.PIT, '-')]
                self.KB.add_clause(clause)

        # If this cell have Stench
        # BASE KNOWLEDGE: S <=> Wa v Wb v Wc v Wd
        if cell.exist_Entity(4):
            # (S => Wa v Wb v Wc v Wd) <=> (-S v Wa v Wb v Wc v Wd)
            clause = [cell.get_literal(CellType.STENCH, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(CellType.WUMPUS, '+'))
            self.KB.add_clause(clause)

            # (Wa v Wb v Wc v Wd => S) <=> ((-Wa ^ -Wb ^ -Wc ^ -Wd) v S)
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(CellType.STENCH, '+'), adj_cell.get_literal(CellType.WUMPUS, '-')]
                self.KB.add_clause(clause)
        else:
            # This cell no have Stench
            # BASE KNOWLEDGE: -Wa ^ -Wb ^ -Wc ^ -Wd
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(CellType.WUMPUS, '-')]
                self.KB.add_clause(clause)

        self.append_event_to_output_file(str(self.KB.KB))

    def backtracking_search(self):
        # if current step of agent have wumpus => game is finish, agent dies
        if self.agent_cell.exist_Entity(2):
            self.add_action(Action.BE_EATEN_BY_WUMPUS)
            return False

        # if current step of agent have pit => game is finish, agent dies
        if self.agent_cell.exist_Entity(1):
            self.add_action(Action.FALL_INTO_PIT)
            return False

        # if current step of agent have gold => agent grab gold
        if self.agent_cell.exist_Entity(0):
            self.add_action(Action.GRAB_GOLD)
            # delete gold
            self.agent_cell.grab_gold()

        # if current step of agent feel Stench => agent perceives Stench
        if self.agent_cell.exist_Entity(4):
            self.add_action(Action.PERCEIVE_STENCH)

        # if current step of agent feel Breeze => agent perceives Breeze
        if self.agent_cell.exist_Entity(3):
            self.add_action(Action.PERCEIVE_BREEZE)

        # mark this cell explored and percepts to the KB
        if not self.agent_cell.is_explored():
            self.agent_cell.explore()
            self.add_KB(self.agent_cell)

        # Initialize valid_adj_cell_list.
        valid_adj_cell_list = self.agent_cell.get_adj_cell(self.cell_matrix)

        temp_adj_cell_list = []
        # Delete node parent in list cell (Because from parent -> this cell => dont move again)
        if self.agent_cell.parent in valid_adj_cell_list:
            valid_adj_cell_list.remove(self.agent_cell.parent)

        # Store previous agent's cell.
        pre_agent_cell = self.agent_cell

        if not self.agent_cell.check():
            # if this cell have breeze or stench
            valid_adj_cell: Cell
            temp_adj_cell_list = []
            # delete cell have pit in next step
            for valid_adj_cell in valid_adj_cell_list:
                if valid_adj_cell.is_explored() and valid_adj_cell.exist_Entity(1):
                    temp_adj_cell_list.append(valid_adj_cell)

            for adj_cell in temp_adj_cell_list:
                valid_adj_cell_list.remove(adj_cell)

            temp_adj_cell_list = []
            if self.agent_cell.exist_Entity(4):
                # this cell is stench => check adj have wumpus or infer this
                for valid_adj_cell in valid_adj_cell_list:
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    # Infer Wumpus
                    self.add_action(Action.INFER_WUMPUS)
                    not_alpha = [[valid_adj_cell.get_literal(CellType.WUMPUS, '-')]]
                    have_wumpus = self.KB.infer(not_alpha)

                    # if this cell have wumpus
                    if have_wumpus:
                        # Detect Wumpus
                        self.add_action(Action.DETECT_WUMPUS)

                        # Shoot this Wumpus
                        self.add_action(Action.SHOOT)
                        self.add_action(Action.KILL_WUMPUS)
                        valid_adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))
                    else:
                        # Dont can detect exact wumpus
                        self.add_action(Action.INFER_NOT_WUMPUS)
                        # Try to detect this cell don't have wumpus
                        not_alpha = [[valid_adj_cell.get_literal(CellType.WUMPUS, '+')]]
                        have_no_wumpus = self.KB.infer(not_alpha)

                        # If we can infer no Wumpus
                        if have_no_wumpus:
                            self.add_action(Action.DETECT_NO_WUMPUS)
                        else:
                            # Don't know exact => don't try move to this cell
                            if valid_adj_cell not in temp_adj_cell_list:
                                temp_adj_cell_list.append(valid_adj_cell)

            # if this cell until have stench => try to shoot all valid cell around this cell
            if self.agent_cell.exist_Entity(4):
                # first step: find all adj_cell don't know what is this
                adj_cell_list = self.agent_cell.get_adj_cell(self.cell_matrix)
                if self.agent_cell.parent in adj_cell_list:
                    adj_cell_list.remove(self.agent_cell.parent)

                explored_cell_list = []
                for adj_cell in adj_cell_list:
                    if adj_cell.is_explored():
                        explored_cell_list.append(adj_cell)
                for explored_cell in explored_cell_list:
                    adj_cell_list.remove(explored_cell)

                # second step: try shoot until don't have stench
                adj_cell: Cell
                for adj_cell in adj_cell_list:
                    self.append_event_to_output_file('Try: ' + str(adj_cell.map_pos))
                    self.turn_to(adj_cell)
                    self.add_action(Action.SHOOT)

                    if adj_cell.exist_Entity(2):
                        # this cell have wumpus
                        self.add_action(Action.KILL_WUMPUS)
                        adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    if not self.agent_cell.exist_Entity(4):
                        # don't have stench
                        self.agent_cell.update_child([adj_cell])
                        break

            # if this cell have Breeze => try to infer Pit
            if self.agent_cell.exist_Entity(3):
                for valid_adj_cell in valid_adj_cell_list:
                    # print("Infer: ", end='')
                    # print(valid_adj_cell.map_pos)
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))
                    self.turn_to(valid_adj_cell)

                    # infer pit
                    self.add_action(Action.INFER_PIT)
                    not_alpha = [[valid_adj_cell.get_literal(CellType.PIT, '-')]]
                    have_pit = self.KB.infer(not_alpha)

                    # if we can infer pit
                    if have_pit:
                        # detect pit
                        self.add_action(Action.DETECT_PIT)
                        valid_adj_cell.explore()
                        self.add_KB(valid_adj_cell)
                        valid_adj_cell.update_parent(valid_adj_cell)
                        temp_adj_cell_list.append(valid_adj_cell)
                    else:
                        # Infer not Pit.
                        self.add_action(Action.INFER_NOT_PIT)
                        not_alpha = [[valid_adj_cell.get_literal(CellType.PIT, '+')]]
                        have_no_pit = self.KB.infer(not_alpha)

                        # If we can infer not Pit.
                        if have_no_pit:
                            # Detect no Pit.
                            self.add_action(Action.DETECT_NO_PIT)

                        # If we can not infer not Pit.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            temp_adj_cell_list.append(valid_adj_cell)

        temp_adj_cell_list = list(set(temp_adj_cell_list))
        # delete all cell not valid
        for adj_cell in temp_adj_cell_list:
            valid_adj_cell_list.remove(adj_cell)

        # try move to all valid cell with backtracking
        self.agent_cell.update_child(valid_adj_cell_list)
        for new_cell in self.agent_cell.child:
            self.move_to(new_cell)
            self.append_event_to_output_file('Move to: ' + str(self.agent_cell.map_pos))

            if not self.backtracking_search():
                return False

            # backtrack
            self.move_to(pre_agent_cell)
            self.append_event_to_output_file('Backtrack: ' + str(pre_agent_cell.map_pos))

        return True

    def solve(self):
        # rest file
        file = open(self.output_filename, 'w')
        file.close()

        self.backtracking_search()

        victory = True
        for row in self.cell_matrix:
            col: Cell
            for col in row:
                # if until have gold or wumpus
                if col.exist_Entity(0) or col.exist_Entity(2):
                    victory = False
                    break

        if victory:
            self.add_action(Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)

        if self.agent_cell.parent == self.cave_cell:
            self.add_action(Action.CLIMB_OUT_OF_THE_CAVE)

        return self.action_list
