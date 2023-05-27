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
    compare_searchers,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, rows, cols) -> None:
        self.board = [[" " for i in range(10)] for j in range(10)]

        self.rows_hints = rows
        self.cols_hints = cols

        self.rows_boats = copy.deepcopy(rows)
        self.cols_boats = copy.deepcopy(cols)

        self.row_spaces = [10 for i in range(10)]
        self.col_spaces = [10 for i in range(10)]

        self.remaining_positions = 100

        self.boats = [4, 3, 2, 1]

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row > 9 or col < 0 or col > 9:
            return "."

        return self.board[row][col]

    def set_value(self, row: int, col: int, val: str) -> bool:
        if row < 0 or row > 9 or col < 0 or col > 9:
            return False

        self.board[row][col] = val
        return True

    def place_hint(self, row: int, col: int, val: str) -> None:
        if self.get_value(row, col) != " " or val in [".", "W"]:
            return

        if self.set_value(row, col, val):
            self.remaining_positions -= 1

            self.row_spaces[row] -= 1
            self.col_spaces[col] -= 1

            self.rows_hints[row] -= 1
            self.cols_hints[col] -= 1

            self.clear_surroundings(row, col)
            for pos in [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]:
                self.decide_position(*pos)

    def remove_hint(self, row: int, col: int) -> None:
        old_val = self.get_value(row, col)

        if old_val not in ["T", "B", "L", "R", "M", "C", "?"]:
            return

        self.set_value(row, col, " ")
        self.remaining_positions += 1

        self.row_spaces[row] += 1
        self.col_spaces[col] += 1

        self.rows_hints[row] += 1
        self.cols_hints[col] += 1

    def place_boat_piece(self, row: int, col: int, val: int) -> None:
        self.remove_hint(row, col)
        if self.set_value(row, col, val):
            self.row_spaces[row] -= 1
            self.col_spaces[col] -= 1

            self.rows_boats[row] -= 1
            self.cols_boats[col] -= 1

            self.rows_hints[row] -= 1
            self.cols_hints[col] -= 1

            self.remaining_positions -= 1

            self.clear_surroundings(row, col)
            for pos in [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]:
                self.decide_position(*pos)

    def place_water(self, row: int, col: int):
        if self.get_value(row, col) != " ":
            return

        if self.set_value(row, col, "."):
            self.row_spaces[row] -= 1
            self.col_spaces[col] -= 1
            self.remaining_positions -= 1

            for pos in [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]:
                self.decide_position(*pos)

    def place_boat(self, row: int, col: int, size: int, direction: str) -> None:
        self.boats[size - 1] -= 1

        if size == 1:
            self.place_boat_piece(row, col, "c")
            return

        if direction == "H":
            self.place_boat_piece(row, col, "l")

            i = 1
            while i < size - 1:
                self.place_boat_piece(row, col + i, "m")
                i += 1

            self.place_boat_piece(row, col + i, "r")
        elif direction == "V":
            self.place_boat_piece(row, col, "t")

            i = 1
            while i < size - 1:
                self.place_boat_piece(row + i, col, "m")
                i += 1

            self.place_boat_piece(row + i, col, "b")

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return (self.get_value(row - 1, col), self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))

    def adjacent_diagonal_values(self, row: int, col: int) -> (str, str, str, str):
        """Devolve os valores imediatamente acima á esquerda, acima à direita, abaixo à esquerda e abaixo à direita,
        respectivamente."""
        return (
            self.get_value(row - 1, col - 1),
            self.get_value(row - 1, col + 1),
            self.get_value(row + 1, col - 1),
            self.get_value(row + 1, col + 1),
        )

    def clear_surroundings(self, row: int, col: int) -> None:
        current_simbol = self.get_value(row, col)

        if current_simbol in [" ", "."]:
            return

        positions_to_clear = [
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1),
        ]

        up, down = (row - 1, col), (row + 1, col)
        left, right = (row, col - 1), (row, col + 1)

        up_value, down_value = self.adjacent_vertical_values(row, col)
        left_value, right_value = self.adjacent_horizontal_values(row, col)

        if current_simbol in ["m", "M"]:
            if up_value == "." or down_value == ".":
                self.place_hint(*left, "?")
                self.place_hint(*right, "?")

            if left_value == "." or right_value == ".":
                self.place_hint(*up, "?")
                self.place_hint(*down, "?")

            if up_value == ".":
                positions_to_clear.append(down)
            elif down_value == ".":
                positions_to_clear.append(up)
            elif left_value == ".":
                positions_to_clear.append(right)
            elif right_value == ".":
                positions_to_clear.append(left)
        elif current_simbol == "?":
            pass
        else:
            if current_simbol not in ["t", "T"]:
                positions_to_clear.append(down)
            if current_simbol not in ["b", "B"]:
                positions_to_clear.append(up)
            if current_simbol not in ["l", "L"]:
                positions_to_clear.append(right)
            if current_simbol not in ["r", "R"]:
                positions_to_clear.append(left)

            if current_simbol in ["t", "T"]:
                self.place_hint(row + 1, col, "?")
            if current_simbol in ["b", "B"]:
                self.place_hint(row - 1, col, "?")
            if current_simbol in ["l", "L"]:
                self.place_hint(row, col + 1, "?")
            if current_simbol in ["r", "R"]:
                self.place_hint(row, col - 1, "?")

        for pos in positions_to_clear:
            self.place_water(*pos)

    def decide_position(self, row: int, col: int) -> None:
        if self.get_value(row, col) != "?":
            return

        up, down = self.adjacent_vertical_values(row, col)
        left, right = self.adjacent_horizontal_values(row, col)

        if up == " " or down == " " or left == " " or right == " ":
            return

        if up == ".":
            if down == ".":
                if left == ".":
                    if right == ".":
                        new = "C"
                    else:
                        new = "L"
                else:
                    if right == ".":
                        new = "R"
                    else:
                        new = "M"
            else:
                new = "T"
        else:
            if down == ".":
                new = "B"
            else:
                new = "M"

        self.remove_hint(row, col)
        self.place_hint(row, col, new)

    def fill_rows_cols(self) -> None:
        for i in range(10):
            if self.rows_hints[i] == 0:
                for j in range(10):
                    self.place_water(i, j)

        for j in range(10):
            if self.cols_hints[j] == 0:
                for i in range(10):
                    self.place_water(i, j)

    def complete_rows_cols(self) -> None:
        for i in range(10):
            if self.row_spaces[i] == self.rows_hints[i]:
                for j in range(10):
                    self.place_hint(i, j, "?")

        for j in range(10):
            if self.col_spaces[j] == self.cols_hints[j]:
                for i in range(10):
                    self.place_hint(i, j, "?")

    def cleanup(self) -> None:
        current_remaining = -1

        while current_remaining != self.remaining_positions:
            current_remaining = self.remaining_positions

            self.fill_rows_cols()

            for i in range(10):
                for j in range(10):
                    self.clear_surroundings(i, j)

            self.complete_rows_cols()

            for i in range(10):
                for j in range(10):
                    self.decide_position(i, j)

            self.place_guaranteed_boats()

    def check_boat(self, row: int, col: int, size: int, direction: str, hard=False):
        value = self.get_value(row, col)
        up, down = self.adjacent_vertical_values(row, col)
        left, right = self.adjacent_horizontal_values(row, col)

        values_empty = [".", " "]
        values_top = ["T"] if hard else ["T", "?", " "]
        values_bot = ["B"] if hard else ["B", "?", " "]
        values_left = ["L"] if hard else ["L", "?", " "]
        values_right = ["R"] if hard else ["R", "?", " "]
        values_circle = ["C"] if hard else ["C", "?", " "]
        values_mid = ["M"] if hard else ["M", "?", " "]

        if size == 1:
            if (
                (up not in values_empty)
                or (down not in values_empty)
                or (left not in values_empty)
                or (right not in values_empty)
            ):
                return False
            if value not in values_circle:
                return False

        if direction == "H":
            if (
                (up not in values_empty)
                or (down not in values_empty)
                or (left not in values_empty)
            ):
                return False

            if value not in values_left:
                return False

            i = 1
            while i < size - 1:
                up, down = self.adjacent_vertical_values(row, col + i)

                if (up not in values_empty) or (down not in values_empty):
                    return False

                if self.get_value(row, col + i) not in values_mid:
                    return False

                i += 1

            up, down = self.adjacent_vertical_values(row, col + i)
            left, right = self.adjacent_horizontal_values(row, col + i)
            if (
                (up not in values_empty)
                or (down not in values_empty)
                or (right not in values_empty)
            ):
                return False

            if self.get_value(row, col + i) not in values_right:
                return False

        if direction == "V":
            if (
                (up not in values_empty)
                or (left not in values_empty)
                or (right not in values_empty)
            ):
                return False

            if value not in values_top:
                return False

            i = 1
            while i < size - 1:
                left, right = self.adjacent_horizontal_values(row + i, col)

                if (left not in values_empty) or (right not in values_empty):
                    return False

                if self.get_value(row + i, col) not in values_mid:
                    return False

                i += 1

            up, down = self.adjacent_vertical_values(row + i, col)
            left, right = self.adjacent_horizontal_values(row + i, col)
            if (
                (left not in values_empty)
                or (right not in values_empty)
                or (down not in values_empty)
            ):
                return False

            if self.get_value(row + i, col) not in values_bot:
                return False

        return True

    def check_positions_boat(self, size: int):
        # Otimizar meeter >= size
        avail_rows = [i for i in range(10) if self.rows_boats[i] > 0]
        avail_rows.sort(key=(lambda x: self.rows_hints[x]))
        avail_cols = [i for i in range(10) if self.cols_boats[i] > 0]
        avail_cols.sort(key=(lambda x: self.cols_hints[x]))

        positions = []
        if size == 1:
            for i in avail_rows:
                for j in avail_cols:
                    if self.check_boat(i, j, 1, ""):
                        positions.append((i, j, size, ""))

            return positions

        for i in avail_rows:
            for j in avail_cols:
                if self.rows_boats[i] >= size and self.check_boat(i, j, size, "H"):
                    positions.append((i, j, size, "H"))

                if self.cols_boats[j] >= size and self.check_boat(i, j, size, "V"):
                    positions.append((i, j, size, "V"))

        positions.sort(
            key=(
                lambda x: self.cols_hints[x[1]]
                if x[3] == "V"
                else self.rows_hints[x[0]]
            ),
        )
        return positions

    def place_guaranteed_boats(self) -> None:
        for i in range(10):
            for j in range(10):
                value = self.get_value(i, j)

                if value == "C":
                    if self.check_boat(i, j, 1, "", True):
                        self.place_boat(i, j, 1, "")
                elif value == "T":
                    for k in range(2, 5):
                        if self.check_boat(i, j, k, "V", True):
                            self.place_boat(i, j, k, "V")
                            break
                elif value == "L":
                    for k in range(2, 5):
                        if self.check_boat(i, j, k, "H", True):
                            self.place_boat(i, j, k, "H")
                            break

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        rows = [eval(x) for x in input().split("\t")[1:]]
        columns = [eval(x) for x in input().split("\t")[1:]]

        board = Board(rows, columns)
        hints = []

        n = eval(input())

        for i in range(n):
            x, y, hint = input().split("\t")[1:]

            if hint == "W":
                board.place_water(eval(x), eval(y))
            else:
                board.place_hint(eval(x), eval(y), hint)

            hints.append((eval(x), eval(y), hint))

        board.cleanup()

        return board, hints

    def display(self, hints=[], advanced=False) -> None:
        display_board = [[" " for i in range(10)] for j in range(10)]
        for i in range(10):
            for j in range(10):
                display_board[i][j] = self.get_value(i, j)

        for hint in hints:
            i, j, val = hint
            display_board[i][j] = val

        print("\n".join(["".join(x) for x in display_board]))

        if advanced:
            print("rows w/ hints:", self.rows_hints)
            print("rows w/o hints:", self.rows_boats)
            print("rows spaces:", self.row_spaces)

            print("cols w/ hints:", self.cols_hints)
            print("cols w/o hints:", self.cols_boats)
            print("cols spaces:", self.col_spaces)

            print("rem. positions:", self.remaining_positions)
            print("rem. boats:", self.boats)


class Bimaru(Problem):
    def __init__(self, board: Board):
        super().__init__(BimaruState(board))

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        for k in range(4, 0, -1):
            if state.board.boats[k - 1] > 0:
                return state.board.check_positions_boat(k)

        return []

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        old_board = copy.deepcopy(state.board)
        new_state = BimaruState(old_board)

        new_state.board.place_boat(*action)
        new_state.board.cleanup()

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.board.remaining_positions != 0:
            return False

        for x in state.board.rows_boats:
            if x != 0:
                return False

        for x in state.board.cols_boats:
            if x != 0:
                return False

        for i in range(4):
            if state.board.boats[i] != 0:
                return False

        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return 20 - (
            node.state.board.boats[0]
            + node.state.board.boats[1] * 2
            + node.state.board.boats[2] * 3
            + node.state.board.boats[3] * 4
        )

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board, hints = Board.parse_instance()
    problem = Bimaru(board)
    """
    compare_searchers(
        [problem],
        ["Searcher", "Successors | Goal_Tests | States | Found"],
        searchers=[depth_first_tree_search],
    )
    """
    res = depth_first_tree_search(problem)
    res.state.board.display(hints=hints)
