# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 42:
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

    def __init__(self, rows, columns) -> None:
        self.board = [[" " for i in range(10)] for j in range(10)]

        self.rows = rows
        self.columns = columns

        self.ships = [4, 3, 2, 1]

        self.remaining_spaces = 100

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row, col]

    def set_value(self, row: int, col: int, val: str) -> None:
        """Escreve na posição escolhida, se ja estiver preenchida, nao faz nada"""
        if self.board[row][col] == " ":
            self.board[row][col] = val
            self.remaining_spaces -= 1

        if val != "W" or val != ".":
            self.rows[row] -= 1
            self.rows[col] -= 1

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
        pass

    def fill_row(self, row: int) -> None:
        """Given a specific row, fills all empty spaces with water."""
        for i in range(10):
            self.set_value(row, i, ".")

    def fill_column(self, col: int) -> None:
        """Given a specific column, fills all empty spaces with water."""
        for i in range(10):
            self.set_value(i, col, ".")

    def clear_rows(self) -> None:
        """Fills all complete rows with water."""
        for i in range(10):
            if self.rows[i] == 0:
                self.fill_row(i)
                self.rows[i] = -1

    def clear_columns(self) -> None:
        """Fills all complete collumns with water."""
        for i in range(10):
            if self.columns[i] == 0:
                self.fill_column(i)
                self.columns[i] = -1

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
            board.set_value(eval(hint[0]), eval(hint[1]), hint[2])

        return board

    def display(self):
        print("\n".join(["".join(x) for x in self.board]))

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
    board = Board.parse_instance()
    board.display()
    board.clear_columns()
    board.clear_rows()
    board.display()
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
