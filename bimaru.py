# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 42:
# 100293 Carlos Felgueiras
# 102556 Daniel Carvalho

import sys
import copy
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows, columns) -> None:
        self.board = [[" " for i in range(10)] for j in range(10)]

        self.rows = rows
        self.columns = columns

        self.remaining_spaces = 100
        self.question_marks = 0

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]

    def set_value(self, row: int, col: int, val: str, cleanup=True) -> None:
        """Escreve na posição escolhida, se ja estiver preenchida, nao faz nada"""
        if self.board[row][col] == " ":
            self.board[row][col] = val
            if val != "?":
                self.remaining_spaces -= 1
            else:
                self.question_marks += 1

            if val != "W" and val != ".":
                self.rows[row] -= 1
                self.columns[col] -= 1
                if cleanup:
                    self.clear_surroundings(row, col)

        if self.board[row][col] == "?" and val != "." and val != "W" and val != "?":
            self.board[row][col] = val
            self.question_marks -= 1
            if val == " ":
                self.rows[row] += 1
                self.columns[col] += 1
            else:
                self.remaining_spaces -= 1

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (
            self.board[row - 1][col] if row - 1 >= 0 else None,
            self.board[row + 1][col] if row + 1 <= 9 else None,
        )

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (
            self.board[row][col - 1] if col - 1 >= 0 else None,
            self.board[row][col + 1] if col + 1 <= 9 else None,
        )

    def adjacent_diagonal_values(self, row: int, col: int) -> (str, str, str, str):
        """Devolve os valores nas diagonais imediatas do quadrado escolhido.
        Order: LU, RU, LD, RD"""
        return (
            self.board[row - 1][col - 1] if row - 1 >= 0 and col - 1 >= 0 else None,
            self.board[row - 1][col + 1] if row - 1 >= 0 and col + 1 <= 9 else None,
            self.board[row + 1][col - 1] if row + 1 <= 9 and col - 1 >= 0 else None,
            self.board[row + 1][col + 1] if row + 1 <= 9 and col + 1 <= 9 else None,
        )

    def adjacent_vertical_coords(self, row: int, col: int) -> (tuple, tuple):
        """Devolve as coordenadas imediatamente acima e abaixo,
        respectivamente."""
        return (
            (row - 1, col) if row - 1 >= 0 else None,
            (row + 1, col) if row + 1 <= 9 else None,
        )

    def adjacent_horizontal_coords(self, row: int, col: int) -> (tuple, tuple):
        """Devolve as coordenadas imediatamente à esquerda e à direita,
        respectivamente."""
        return (
            (row, col - 1) if col - 1 >= 0 else None,
            (row, col + 1) if col + 1 <= 9 else None,
        )

    def adjacent_diagonal_coords(
        self, row: int, col: int
    ) -> (tuple, tuple, tuple, tuple):
        """Devolve as coordenadas nas diagonais imediatas do quadrado escolhido.
        Order: LU, RU, LD, RD"""
        return (
            (row - 1, col - 1) if row - 1 >= 0 and col - 1 >= 0 else None,
            (row - 1, col + 1) if row - 1 >= 0 and col + 1 <= 9 else None,
            (row + 1, col - 1) if row + 1 <= 9 and col - 1 >= 0 else None,
            (row + 1, col + 1) if row + 1 <= 9 and col + 1 <= 9 else None,
        )

    def fill_row(self, row: int) -> None:
        """Given a specific row, fills all empty spaces with water."""
        for i in range(10):
            self.set_value(row, i, ".")

    def fill_column(self, col: int) -> None:
        """Given a specific column, fills all empty spaces with water."""
        for i in range(10):
            self.set_value(i, col, ".")

    def fill_rows(self) -> None:
        """Fills all complete rows with water."""
        for i in range(10):
            if self.rows[i] == 0:
                self.fill_row(i)
                self.rows[i] = -1

    def fill_columns(self) -> None:
        """Fills all complete collumns with water."""
        for i in range(10):
            if self.columns[i] == 0:
                self.fill_column(i)
                self.columns[i] = -1

    def row_empty_spaces(self, row: int) -> int:
        count = 0
        for i in range(10):
            if self.get_value(row, i) == " ":
                count += 1

        return count

    def column_empty_spaces(self, col: int) -> int:
        count = 0
        for i in range(10):
            if self.get_value(i, col) == " ":
                count += 1

        return count

    def complete_row(self, row: int) -> None:
        """Completes the row with boats (in case that the number of empty spaces is the same as the remaining boats)"""
        for i in range(10):
            self.set_value(row, i, "?")

    def complete_column(self, col: int) -> None:
        """Completes the collumn with boats (in case that the number of empty spaces is the same as the remaining boats)"""
        for i in range(10):
            self.set_value(i, col, "?")

    def complete_rows(self) -> None:
        """Completes all rows that are valid"""
        for i in range(10):
            if self.rows[i] >= 1 and self.row_empty_spaces(i) == self.rows[i]:
                self.complete_row(i)

    def complete_columns(self) -> None:
        """Completes all rows that are valid"""
        for i in range(10):
            if self.columns[i] >= 1 and self.column_empty_spaces(i) == self.columns[i]:
                self.complete_column(i)

    def set_value_bulk(self, lst: list, val: str) -> None:
        """Given a list of tuples (or None), sets the values on the positions represented by the tuples to the value given."""
        for pos in lst:
            if pos:
                self.set_value(pos[0], pos[1], val)

    def clear_surroundings(self, row: int, col: int) -> None:
        """Clears the surroundings of a specific position, depending on what is there."""
        current_simbol = self.get_value(row, col)

        if current_simbol == " " or current_simbol == "W" or current_simbol == ".":
            return

        positions_to_clean = []

        for coord in self.adjacent_diagonal_coords(row, col):
            positions_to_clean.append(coord)

        adjacent_horizontal = self.adjacent_horizontal_coords(row, col)
        adjacent_vertical = self.adjacent_vertical_coords(row, col)

        if current_simbol in ["T", "t"]:
            positions_to_clean.append(adjacent_horizontal[0])
            positions_to_clean.append(adjacent_horizontal[1])
            positions_to_clean.append(adjacent_vertical[0])
        elif current_simbol in ["B", "b"]:
            positions_to_clean.append(adjacent_horizontal[0])
            positions_to_clean.append(adjacent_horizontal[1])
            positions_to_clean.append(adjacent_vertical[1])
        elif current_simbol in ["L", "l"]:
            positions_to_clean.append(adjacent_vertical[0])
            positions_to_clean.append(adjacent_vertical[1])
            positions_to_clean.append(adjacent_horizontal[0])
        elif current_simbol in ["R", "r"]:
            positions_to_clean.append(adjacent_vertical[0])
            positions_to_clean.append(adjacent_vertical[1])
            positions_to_clean.append(adjacent_horizontal[1])
        elif current_simbol in ["C", "c"]:
            positions_to_clean.append(adjacent_vertical[0])
            positions_to_clean.append(adjacent_vertical[1])
            positions_to_clean.append(adjacent_horizontal[0])
            positions_to_clean.append(adjacent_horizontal[1])
        elif current_simbol in ["M", "m"]:
            if self.adjacent_vertical_values(row, col)[0] in [
                "T",
                "t",
                "M",
                "m",
            ] or self.adjacent_vertical_values(row, col)[1] in ["B", "b", "M", "m"]:
                positions_to_clean.append(adjacent_horizontal[0])
                positions_to_clean.append(adjacent_horizontal[1])
            elif self.adjacent_horizontal_values(row, col)[0] in [
                "L",
                "l",
                "M",
                "m",
            ] or self.adjacent_horizontal_values(row, col)[1] in ["R", "r", "M", "m"]:
                positions_to_clean.append(adjacent_vertical[0])
                positions_to_clean.append(adjacent_vertical[1])

        self.set_value_bulk(positions_to_clean, ".")

    def clear_positions(self):
        """Clears all surroundings of all positions."""
        for i in range(10):
            for j in range(10):
                self.clear_surroundings(i, j)

    def decide_square(self, row: int, col: int) -> None:
        # Up, Down, Left, Right
        adjacents = [
            self.adjacent_vertical_values(row, col)[0],
            self.adjacent_vertical_values(row, col)[1],
            self.adjacent_horizontal_values(row, col)[0],
            self.adjacent_horizontal_values(row, col)[1],
        ]

        for i in range(4):
            if adjacents[i] == " ":
                return

            if adjacents[i] is None or adjacents[i] == "." or adjacents[i] == "W":
                adjacents[i] = "W"
            else:
                adjacents[i] = "B"

        up, down, left, right = adjacents
        new_value = ""
        if up == "W":
            if down == "W":
                if left == "W":
                    if right == "W":
                        new_value = "c"
                    else:
                        new_value = "l"
                else:
                    if right == "W":
                        new_value = "r"
                    else:
                        new_value = "m"
            else:
                new_value = "t"
        else:
            if down == "W":
                new_value = "b"
            else:
                new_value = "m"

        self.set_value(row, col, new_value)

    def square_possibilities(self, row, col) -> list:
        up, down = self.adjacent_vertical_values(row, col)
        left, right = self.adjacent_horizontal_values(row, col)
        lu, ru, ld, rd = self.adjacent_diagonal_values(row, col)

        eq_water = [None, ".", "W"]
        eq_top = ["T", "t"]
        eq_bottom = ["B", "b"]
        eq_left = ["L", "l"]
        eq_right = ["R", "r"]
        eq_middle = ["M", "m"]
        eq_circle = ["C", "c"]

        possible_values = [".", "t", "b", "l", "r", "c", "m"]

        if up in eq_top:
            possible_values = [
                x for x in possible_values if x not in [".", "t", "l", "r", "c"]
            ]
        if down in eq_bottom:
            possible_values = [
                x for x in possible_values if x not in [".", "b", "l", "r", "c"]
            ]
        if left in eq_left:
            possible_values = [
                x for x in possible_values if x not in [".", "t", "b", "l", "c"]
            ]
        if right in eq_right:
            possible_values = [
                x for x in possible_values if x not in [".", "t", "b", "r", "c"]
            ]

        if up in eq_middle:
            possible_values = [
                x for x in possible_values if x not in ["t", "l", "r", "c"]
            ]
            if lu in eq_water or ru in eq_water:
                possible_values = [x for x in possible_values if x not in ["."]]

        if down in eq_middle:
            possible_values = [
                x for x in possible_values if x not in ["b", "l", "r", "c"]
            ]
            if ld in eq_water or rd in eq_water:
                possible_values = [x for x in possible_values if x not in ["."]]

        if left in eq_middle:
            possible_values = [
                x for x in possible_values if x not in ["t", "b", "l", "c"]
            ]
            if lu in eq_water or ld in eq_water:
                possible_values = [x for x in possible_values if x not in ["."]]

        if right in eq_middle:
            possible_values = [
                x for x in possible_values if x not in ["t", "b", "r", "c"]
            ]
            if ru in eq_water or rd in eq_water:
                possible_values = [x for x in possible_values if x not in ["."]]

        if up in eq_water:
            possible_values = [x for x in possible_values if x not in ["b"]]
        if down in eq_water:
            possible_values = [x for x in possible_values if x not in ["t"]]
        if left in eq_water:
            possible_values = [x for x in possible_values if x not in ["r"]]
        if right in eq_water:
            possible_values = [x for x in possible_values if x not in ["l"]]

        if (
            (up in eq_water and left in eq_water)
            or (down in eq_water and left in eq_water)
            or (up in eq_water and right in eq_water)
            or (down in eq_water and right in eq_water)
        ):
            possible_values = [x for x in possible_values if x not in ["m"]]

        if self.rows[row] == 1 and right not in ["R", "r", "M", "m"]:
            possible_values = [x for x in possible_values if x not in ["l"]]

        if self.columns[col] == 1 and down not in ["B", "b", "M", "m"]:
            possible_values = [x for x in possible_values if x not in ["t"]]

        return possible_values

    def first_empty(self):
        for i in range(10):
            for j in range(10):
                if self.get_value(i, j) == " ":
                    return (i, j)

    def decide_squares(self, hard: bool) -> None:
        if hard:
            for i in range(10):
                for j in range(10):
                    if self.get_value(i, j) == "?":
                        self.set_value(i, j, " ")
        else:
            for i in range(10):
                for j in range(10):
                    if self.get_value(i, j) == "?":
                        self.decide_square(i, j)

    def cleanup(self):
        current_spaces = -1
        current_question_marks = -1

        while (
            self.remaining_spaces != current_spaces
            or self.question_marks != current_question_marks
        ):
            current_spaces = self.remaining_spaces
            current_question_marks = self.question_marks
            self.fill_columns()
            self.fill_rows()
            self.clear_positions()
            self.complete_columns()
            self.complete_rows()
            self.decide_squares(False)
            self.decide_squares(True)

    def check_boats(self):
        boats = [4, 3, 2, 1]

        for i in range(10):
            for j in range(10):
                if self.get_value(i, j) in ["C", "c"]:
                    boats[0] -= 1
                elif self.get_value(i, j) in ["T", "t"]:
                    k = 1

                    while self.get_value(i + k, j) in ["M", "m"]:
                        k += 1

                    if self.get_value(i + k, j) in ["B", "b"]:
                        if k <= 3:
                            boats[k] -= 1
                        else:
                            return -1
                    elif self.get_value(i + k, j) == " ":
                        pass
                    else:
                        return -1
                elif self.get_value(i, j) in ["L", "l"]:
                    k = 1

                    while self.get_value(i, j + k) in ["M", "m"]:
                        k += 1

                    if self.get_value(i, j + k) in ["R", "r"]:
                        if k <= 3:
                            boats[k] -= 1
                        else:
                            return -1
                    elif self.get_value(i, j + k) == " ":
                        pass
                    else:
                        return -1

        for x in boats:
            if x < 0:
                return -1

        for x in boats:
            if x > 0:
                return 1

        return 0

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        rows = [eval(x) for x in input().split("\t")[1:]]
        columns = [eval(x) for x in input().split("\t")[1:]]

        board = Board(rows, columns)

        hints = eval(input())

        for i in range(hints):
            hint = input().split("\t")[1:]
            board.set_value(eval(hint[0]), eval(hint[1]), hint[2], cleanup=False)

        board.cleanup()
        return board

    def display(self):
        print("--------------")
        print("Remaining positions: " + str(self.remaining_spaces))
        print("\n".join(["".join(x) for x in self.board]))
        print(str(self.rows))
        print(str(self.columns))
        print("--------------")

    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        super().__init__(BimaruState(board))

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.board.first_empty() is None:
            return []

        actions = []
        x, y = state.board.first_empty()
        for pos in state.board.square_possibilities(x, y):
            actions.append((x, y, pos))

        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        x, y, val = action
        old_board = copy.deepcopy(state.board)
        new_state = BimaruState(old_board)
        new_state.board.set_value(x, y, val)
        new_state.board.cleanup()

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        for x in state.board.rows:
            if x != -1:
                return False

        for x in state.board.columns:
            if x != -1:
                return False

        return state.board.remaining_spaces == 0 and (state.board.check_boats() == 0)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        return 0

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()

    problem = Bimaru(board)
    dfs = depth_first_tree_search(problem)
    dfs.state.board.display()

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
