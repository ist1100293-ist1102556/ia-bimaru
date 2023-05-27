from bimaruboats import *


def actions(board):
    """Retorna uma lista de ações que podem ser executadas a
    partir do estado passado como argumento."""
    for k in range(4, 0, -1):
        if board.boats[k - 1] > 0:
            return board.check_positions_boat(k)

    return []


options = []

board, hints = Board.parse_instance()

board.display(advanced=True)
print(actions(board))
for i in range(len(options)):
    board.place_boat(*options[i])
    board.cleanup()
    board.display(advanced=True)
    options(board)
