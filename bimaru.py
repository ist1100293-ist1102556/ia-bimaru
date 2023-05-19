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

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

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
        if val != " " and self.set_value(row, col, val):
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

    # TODO: outros metodos da classe


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
    board.display()
