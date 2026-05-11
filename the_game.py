"""
The Game (Renju) - determine the winner on a 19x19 board.
Stones: 1 = black, 2 = white, 0 = empty.
A player wins if there are exactly 5 stones of the same color in a row
horizontally, vertically or diagonally.
"""

from pathlib import Path

BOARD_SIZE = 19
INPUT_FILE = Path(__file__).parent / "sample_input.txt"


def read_board(lines):
    """Read 19 rows of 19 numbers from the given lines iterator."""
    board = []
    for _ in range(BOARD_SIZE):
        row = list(map(int, next(lines).split()))
        board.append(row)
    return board


def is_inside(row, col):
    """Return True if (row, col) is within the board."""
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def find_winner(board):
    """
    Look for a winning line on the board.
    Returns (player, row, col) in 1-based coordinates
    or (0, 0, 0) if there is no winner yet.
    """
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            player = board[row][col]
            if player == 0:
                continue

            for d_row, d_col in directions:
                prev_row, prev_col = row - d_row, col - d_col
                if board[prev_row][prev_col] == player:
                    continue

                count = 0
                cur_row, cur_col = row, col
                while is_inside(cur_row, cur_col) and board[cur_row][cur_col] == player:
                    count += 1
                    cur_row += d_row
                    cur_col += d_col

                if count >= 5:
                    return player, row + 1, col + 1

    return 0, 0, 0


def main():
    with open(INPUT_FILE) as f:
        lines = iter(f.read().splitlines())

    num_tests = int(next(lines))
    for _ in range(num_tests):
        board = read_board(lines)
        winner, row, col = find_winner(board)
        print(winner)
        if winner != 0:
            print(row, col)


if __name__ == "__main__":
    main()
