# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 100293 Carlos Felgueiras
# 102556 Daniel Carvalho

import sys
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


class Board:
    """Representação interna de um tabuleiro de Bimaru:
    "." Água
    "t" Topo
    "b" Fundo
    "l" Esquerda
    "d" Direita
    "m" meio
    "c" barco singular
    " " espaço vazio
    """

    def __init__(self, rows, cols) -> None:
        self.board = [[" " for i in range(10)] for j in range(10)]

        self.rows = rows
        self.cols = cols

        self.row_remaining = [10 for i in range(10)]
        self.col_remaining = [10 for i in range(10)]

        self.remaining_positions = 100

        self.first_empty = (0, 0)

    def get_value(self, row: int, col: int) -> str | None:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row > 9 or col < 0 or col > 9:
            return "."

        return self.board[row][col]

    def set_value(self, row: int, col: int, val: str) -> bool:
        if row < 0 or row > 9 or col < 0 or col > 9:
            return False

        self.board[row][col] = val
        return True

    def place_piece(self, row: int, col: int, val: str) -> None:
        if (
            self.get_value(row, col) == " "
            and val != " "
            and self.set_value(row, col, val)
        ):
            self.row_remaining[row] -= 1
            self.col_remaining[col] -= 1
            self.remaining_positions -= 1

            if val != ".":
                self.rows[row] -= 1
                self.cols[col] -= 1

    def remove_piece(self, row: int, col: int) -> None:
        old_val = self.get_value(row, col)
        if old_val != " " and self.set_value(row, col, " "):
            self.row_remaining[row] += 1
            self.col_remaining[col] += 1
            self.remaining_positions += 1

            if old_val != ".":
                self.rows[row] += 1
                self.cols[col] += 1

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

    def fill_rows_cols_water(self) -> None:
        for i in range(10):
            if self.rows[i] == 0:
                for j in range(10):
                    self.place_piece(i, j, ".")
                self.rows[i] = -1

        for j in range(10):
            if self.cols[j] == 0:
                for i in range(10):
                    self.place_piece(i, j, ".")
                self.cols[j] = -1

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

        if current_simbol == "m":
            """
            if up_value in ["t", "m"] or down_value in ["b", "m"]:
                positions_to_clear.append(left)
                positions_to_clear.append(right)
            elif left_value in ["l", "m"] or right_value in ["r", "m"]:
                positions_to_clear.append(up)
                positions_to_clear.append(down)
            """
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
            if current_simbol != "t":
                positions_to_clear.append(down)
            if current_simbol != "b":
                positions_to_clear.append(up)
            if current_simbol != "l":
                positions_to_clear.append(right)
            if current_simbol != "r":
                positions_to_clear.append(left)

        for pos in positions_to_clear:
            self.place_piece(*pos, ".")

    def complete_rows_and_collumns(self):
        for i in range(10):
            if self.row_remaining[i] == self.rows[i]:
                for j in range(10):
                    self.place_piece(i, j, "?")

        for j in range(10):
            if self.col_remaining[j] == self.cols[j]:
                for i in range(10):
                    self.place_piece(i, j, "?")

    def decide_position(self, row: int, col: int) -> None:
        if self.get_value(row, col) != "?":
            return

        up, down = self.adjacent_vertical_values(row, col)
        left, right = self.adjacent_horizontal_values(row, col)

        if up == " " or down == " " or left == " " or right == " ":
            return

        new = ""
        if up == ".":
            if down == ".":
                if left == ".":
                    if right == ".":
                        new = "c"
                    else:
                        new = "l"
                else:
                    if right == ".":
                        new = "r"
                    else:
                        new = "m"
            else:
                new = "t"
        else:
            if down == ".":
                new = "b"
            else:
                new = "m"

        self.remove_piece(row, col)
        self.place_piece(row, col, new)

    def cleanup(self) -> None:
        current_remaining = -1

        while current_remaining != self.remaining_positions:
            current_remaining = self.remaining_positions

            self.fill_rows_cols_water()

            for i in range(10):
                for j in range(10):
                    self.clear_surroundings(i, j)

            self.complete_rows_and_collumns()

            for i in range(10):
                for j in range(10):
                    self.decide_position(i, j)

            for i in range(10):
                for j in range(10):
                    if self.get_value(i, j) == "?":
                        self.remove_piece(i, j)

    def first_empty_space(self) -> (int, int):
        """Devolve a primeira casa vazia no tabuleiro, a contar da esquerda para a direita, de cima para baixo."""
        i, j = self.first_empty
        while i < 10:
            while j < 10:
                if self.get_value(i, j) == " ":
                    self.first_empty = (i, j)
                    return self.first_empty
                j += 1
            j = 0
            i += 1

        return None

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

        rows = [eval(x) for x in input().split("\t")[1:]]
        columns = [eval(x) for x in input().split("\t")[1:]]

        board = Board(rows, columns)
        hints = []

        n = eval(input())

        for i in range(n):
            x, y, hint = input().split("\t")[1:]

            if hint == "W":
                board.place_piece(eval(x), eval(y), ".")
            else:
                board.place_piece(eval(x), eval(y), hint.lower())

            hints.append((eval(x), eval(y), hint))

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
            print("Remaining positions:", self.remaining_positions)
            print("Remaining boats in rows:\n", str(self.rows))
            print("Remaining empty positions in row:\n", self.row_remaining)
            print("Remaining boats in col:\n", str(self.cols))
            print("Remaining empty positions in col:\n", self.col_remaining)


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board, hints = Board.parse_instance()
    board.cleanup()
    board.display(hints=hints, advanced=False)
