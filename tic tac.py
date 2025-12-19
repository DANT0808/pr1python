#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Консольная игра крестики-нолики (обобщённая) с режимами:
- игра друг против друга
- игра против робота
Поддерживается произвольный размер квадратного поля (N x N, N >= 3).
Побеждает тот, кто соберёт N одинаковых символов по горизонтали,
вертикали или на одной из диагоналей.

Дополнительно:
- Создаётся директория со статистикой и текстовый файл, куда
  записываются данные по каждой сыгранной партии.
- Перед каждой игрой случайным образом выбирается,
  кто ходит первым (символ X или O).
- После окончания партии можно сыграть ещё, не выходя из приложения.
- Обрабатываются ошибки ввода пользователя.
"""

import os
import random
import datetime

STATS_DIR = "stats"
STATS_FILE = "game_stats.txt"


def ensure_stats_storage():
    """
    Создаёт директорию и файл для статистики, если их ещё нет.
    """
    try:
        if not os.path.exists(STATS_DIR):
            os.makedirs(STATS_DIR, exist_ok=True)

        stats_path = os.path.join(STATS_DIR, STATS_FILE)
        if not os.path.exists(stats_path):
            with open(stats_path, "w", encoding="utf-8") as f:
                f.write("date_time;mode;board_size;first_symbol;winner;moves\n")
    except OSError as e:
        print(f"Предупреждение: не удалось создать файл статистики: {e}")


def save_stats(mode, board_size, first_symbol, winner, moves):
    """
    Сохраняет статистику одной игры в файл.
    """
    stats_path = os.path.join(STATS_DIR, STATS_FILE)
    try:
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{dt};{mode};{board_size};{first_symbol};{winner};{moves}\n"
        with open(stats_path, "a", encoding="utf-8") as f:
            f.write(line)
    except OSError as e:
        print(f"Предупреждение: не удалось записать статистику: {e}")


def read_int(prompt, min_value=None):
    """
    Безопасное чтение целого числа с проверкой минимального значения.
    """
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")
            continue

        if min_value is not None and value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}.")
            continue

        return value


def draw_board(board):
    """
    Отрисовка игрового поля.
    """
    size = len(board)
    print()
    # Нумерация столбцов
    header = "   " + " ".join(f"{i+1:2}" for i in range(size))
    print(header)
    print("   " + "---" * size)
    for i, row in enumerate(board):
        row_str = " ".join(f"{cell or ' ' :2}" for cell in row)
        print(f"{i+1:2}| {row_str}")
    print()


def get_human_move(board):
    """
    Считывание хода человека с обработкой ошибок.
    """
    size = len(board)
    while True:
        move_str = input(
            f"Введите ход (строка и столбец через пробел, от 1 до {size}): "
        ).strip()
        parts = move_str.split()
        if len(parts) != 2:
            print("Ошибка: нужно ввести два числа через пробел, например: 1 1")
            continue

        try:
            row = int(parts[0])
            col = int(parts[1])
        except ValueError:
            print("Ошибка: координаты должны быть целыми числами.")
            continue

        if not (1 <= row <= size and 1 <= col <= size):
            print(f"Ошибка: координаты должны быть в диапазоне от 1 до {size}.")
            continue

        r, c = row - 1, col - 1
        if board[r][c] != " ":
            print("Ошибка: выбранная клетка уже занята.")
            continue

        return r, c


def check_winner(board, symbol):
    """
    Проверяет, есть ли победа для указанного символа.
    Победа считается, если вся строка, столбец или диагональ заполнены символом.
    """
    size = len(board)

    # Проверка строк
    for r in range(size):
        if all(board[r][c] == symbol for c in range(size)):
            return True

    # Проверка столбцов
    for c in range(size):
        if all(board[r][c] == symbol for r in range(size)):
            return True

    # Главная диагональ
    if all(board[i][i] == symbol for i in range(size)):
        return True

    # Побочная диагональ
    if all(board[i][size - 1 - i] == symbol for i in range(size)):
        return True

    return False


def is_board_full(board):
    """
    Проверка, заполнено ли поле полностью.
    """
    return all(board[r][c] != " " for r in range(len(board)) for c in range(len(board)))


def get_available_moves(board):
    """
    Возвращает список доступных (пустых) клеток.
    """
    moves = []
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == " ":
                moves.append((r, c))
    return moves


def find_winning_move(board, symbol):
    """
    Ищет ход, который приводит к немедленной победе для symbol.
    Возвращает координаты хода или None, если такого хода нет.
    """
    moves = get_available_moves(board)
    for r, c in moves:
        board[r][c] = symbol
        if check_winner(board, symbol):
            board[r][c] = " "
            return r, c
        board[r][c] = " "
    return None


def get_robot_move(board, robot_symbol, human_symbol):
    """
    Логика хода робота:
    1. Попробовать выиграть одним ходом.
    2. Если не получается — заблокировать возможную победу человека.
    3. Занять центр, если свободен.
    4. Сделать случайный ход.
    """
    # 1. Попытка выиграть
    move = find_winning_move(board, robot_symbol)
    if move is not None:
        return move

    # 2. Блокировка победы человека
    move = find_winning_move(board, human_symbol)
    if move is not None:
        return move

    # 3. Центр, если свободен
    size = len(board)
    center = size // 2
    if board[center][center] == " ":
        return center, center

    # 4. Случайный ход
    moves = get_available_moves(board)
    return random.choice(moves)


def play_game(board_size, mode):
    """
    Одна игра.

    mode:
        "pvp"   — игрок против игрока
        "robot" — игрок против робота

    Возвращает кортеж (winner, moves_count, first_symbol).
        winner:
            для режима pvp: "X", "O" или "draw"
            для режима robot: "human", "robot" или "draw"
    """
    board = [[" " for _ in range(board_size)] for _ in range(board_size)]
    moves = 0

    # Случайно выбираем, кто ходит первым: X или O
    first_symbol = random.choice(["X", "O"])
    current_symbol = first_symbol

    if mode == "robot":
        # Человек всегда играет X, робот — O, но первым может ходить кто угодно
        human_symbol = "X"
        robot_symbol = "O"

        print()
        print("Режим игры: человек против робота.")
        print(f"Человек играет за '{human_symbol}', робот играет за '{robot_symbol}'.")
        if first_symbol == human_symbol:
            print("Первым ходит человек (X).")
        else:
            print("Первым ходит робот (O).")
    else:
        print()
        print("Режим игры: два игрока друг против друга.")
        print(f"Игрок с символом '{first_symbol}' ходит первым.")

    while True:
        draw_board(board)

        if mode == "robot" and current_symbol == "O":
            # Ход робота
            print("Ход робота...")
            r, c = get_robot_move(board, robot_symbol="O", human_symbol="X")
        else:
            # Ход человека (или любого из двух людей в pvp)
            print(f"Ход игрока с символом '{current_symbol}'.")
            r, c = get_human_move(board)

        board[r][c] = current_symbol
        moves += 1

        if check_winner(board, current_symbol):
            draw_board(board)
            if mode == "robot":
                if current_symbol == "X":
                    print("Поздравляем! Вы победили робота!")
                    winner = "human"
                else:
                    print("Робот победил. Попробуйте ещё раз!")
                    winner = "robot"
            else:
                print(f"Победил игрок с символом '{current_symbol}'. Поздравляем!")
                winner = current_symbol

            return winner, moves, first_symbol

        if is_board_full(board):
            draw_board(board)
            print("Ничья! Свободных клеток не осталось.")
            return "draw", moves, first_symbol

        # Передаём ход другому символу
        current_symbol = "O" if current_symbol == "X" else "X"


def main_menu():
    """
    Главное меню приложения.
    """
    print("Добро пожаловать в игру 'Крестики-нолики' (расширенный вариант)!")
    ensure_stats_storage()

    while True:
        print()
        print("Главное меню:")
        print("  1 - игра вдвоём (игрок против игрока)")
        print("  2 - игра против робота")
        print("  0 - выход")
        choice = input("Сделайте выбор: ").strip()

        if choice == "0":
            print("Спасибо за игру! До свидания.")
            break
        elif choice not in ("1", "2"):
            print("Ошибка: введите 0, 1 или 2.")
            continue

        mode = "pvp" if choice == "1" else "robot"

        # Цикл игр в выбранном режиме
        while True:
            board_size = read_int(
                "Введите размер игрового поля (целое число не меньше 3): ", min_value=3
            )

            winner, moves, first_symbol = play_game(board_size, mode)
            save_stats(mode, board_size, first_symbol, winner, moves)

            again = input(
                "Сыграть ещё раз в этом режиме? (y/n или д/н): "
            ).strip().lower()
            if again not in ("y", "д", "да"):
                # Возвращаемся в главное меню
                break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nИгра прервана пользователем. До свидания!")
