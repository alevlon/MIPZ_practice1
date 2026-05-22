"""
The Game (Renju) - determine the winner on a 19x19 board.
Stones: 1 = black, 2 = white, 0 = empty.
A player wins if there are exactly 5 stones of the same color in a row
horizontally, vertically or diagonally.
"""

import sys

BOARD_SIZE = 19
# enhancement: магічне число «5» (довжина виграшної лінії) винесене
# в іменовану константу. Раніше воно зустрічалось у коді «як є»,
# що ускладнювало читання та підтримку.
WIN_LENGTH = 5
# enhancement (#4): напрямки сканування винесені у модульну константу
# поряд із BOARD_SIZE/WIN_LENGTH. Раніше цей список перестворювався
# при кожному виклику find_winner; тепер це чиста константа, плюс
# усі «магічні» параметри гри тепер згруповані в одному місці.
DIRECTIONS = ((0, 1), (1, 0), (1, 1), (-1, 1))


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
    Returns (player, row, col) in 1-based coordinates if there is a winner,
    or None otherwise.

    enhancement: раніше функція повертала (0, 0, 0) у разі відсутності
    переможця. Координати (0, 0) фігурували в сигнатурі, але ніколи не
    використовувались викликачем — це збивало з пантелику читача
    («що означає row=0, col=0?»). Тепер сигнатура чесна: або є
    переможець з координатами, або None.
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            player = board[row][col]
            if player == 0:
                continue

            for d_row, d_col in DIRECTIONS:
                prev_row, prev_col = row - d_row, col - d_col
                # bug fix: раніше було просто board[prev_row][prev_col],
                # але при row == 0, d_row == 1 отримуємо prev_row == -1,
                # а у Python board[-1] — це останній рядок списку
                # (negative indexing), а не «поза межами». Через це
                # камінь того ж кольору на протилежному краю дошки міг
                # хибно вважатися продовженням ланцюжка, і ми пропускали
                # валідний початок. Тому спочатку перевіряємо, що
                # попередня клітинка дійсно лежить у межах дошки.
                if is_inside(prev_row, prev_col) and board[prev_row][prev_col] == player:
                    continue

                count = 0
                cur_row, cur_col = row, col
                while is_inside(cur_row, cur_col) and board[cur_row][cur_col] == player:
                    count += 1
                    cur_row += d_row
                    cur_col += d_col

                # bug fix: за специфікацією гравець НЕ виграє, якщо
                # підряд стоїть більше п'яти каменів одного кольору.
                # З оператором >= ланцюжок із 6, 7, 8 каменів помилково
                # давав перемогу (напр., 6 чорних у рядку поверталися
                # як виграш замість 0). Перевіряємо суворо рівність.
                if count == WIN_LENGTH:
                    return player, row + 1, col + 1

    return None


PLAYER_NAMES = {1: "чорні (1)", 2: "білі (2) "}
SEPARATOR = "═" * 60


def format_result(index, result):
    """Return a human-readable line describing the outcome of board #index."""
    label = f"  Дошка #{index}:".ljust(14)
    if result is None:
        return f"{label} переможця немає"
    winner, row, col = result
    return f"{label} виграли {PLAYER_NAMES[winner]} — рядок {row}, стовпець {col}"


def main():
    # bug fix (#1): раніше main() жорстко відкривав sample_input.txt
    # поряд зі скриптом, ігноруючи stdin. Це суперечило README, яке
    # обіцяло запуск через `python the_game.py < sample_input.txt`,
    # і не давало прогнати програму на іншому вхідному файлі без
    # правки коду. Тепер читаємо саме зі stdin, як і задокументовано.
    #
    # bug fix (#2): явно реконфігуруємо stdin/stdout на UTF-8. На
    # Windows системна локаль за замовчуванням — cp1251, тож вхідний
    # файл із UTF-8 BOM/нелатинськими символами міг впасти з
    # UnicodeDecodeError, а pretty-вивід з кириличними рамками — з
    # UnicodeEncodeError. reconfigure() безпечно доступний у Python 3.7+.
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    # enhancement: дозволяємо людині візуально розділяти дошки порожніми
    # рядками («абзацами») у вхідному файлі. Парсер тепер ігнорує
    # порожні рядки та рядки з самих лише пробілів, тож формат лишається
    # сумісним зі строгою специфікацією, але стає набагато читабельнішим
    # для ручного редагування sample_input.txt.
    lines = iter(line for line in sys.stdin.read().splitlines() if line.strip())

    num_tests = int(next(lines))
    results = []
    for _ in range(num_tests):
        board = read_board(lines)
        # Узгоджено з новою сигнатурою find_winner: None == немає переможця,
        # інакше — кортеж (player, row, col).
        results.append(find_winner(board))

    # enhancement: замість сухого виводу за специфікацією (число + пара
    # координат) друкуємо людино-читабельний звіт з шапкою, переліком
    # дощок і підсумком. Так результат набагато простіше переглядати
    # очима під час лабораторної роботи. Якщо колись знадобиться суворий
    # формат для автоматичної перевірки — достатньо додати CLI-прапор.
    wins = sum(1 for r in results if r is not None)
    draws = len(results) - wins

    print(SEPARATOR)
    print("  THE GAME (Renju) — результати")
    print(SEPARATOR)
    print()
    for i, result in enumerate(results, start=1):
        print(format_result(i, result))
    print()
    print(SEPARATOR)
    print(f"  Підсумок: переможців {wins}, нічиїх {draws}")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
