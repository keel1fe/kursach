#могут ходить в стороны, но теперь не ходят вперед, и ходят назад. Есть регистрация надо доработать

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import hashlib

# Глобальные переменные
k = 100  # Размер клетки
color = "burlywood"
white_shashka = "white"
black_shashka = "black"
vid_kl = "yellow"
queen_wh = "gold"
queen_bl = "red"

def hash_parol(parol): # Хеширование пароля
    return hashlib.sha256(parol.encode('utf-8')).hexdigest()
def registr_user():     # Регистрируем пользователя
    if not login.get() or not parol.get():
        messagebox.showerror("Ошибка", "'Логин' и 'Пароль' должны быть заполнены.")
    elif proverka_logina():
        messagebox.showerror("Ошибка", "Учетная запись уже существует.")
    else:
        with open("users.txt", "a") as file:
            file.write(f"{login.get()}:{hash_parol(parol.get())}\n")
        messagebox.showinfo("Успех","Регистрация успешно завершена.\nВойдите в аккаунт")
def proverka_logina():      # Проверяем наличие логина в файле
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            lines = file.readlines()
            login_vvod = login.get()
            for line in lines:
                if login_vvod in line:
                    return True
        return False
def proverka_users():  # Проверяем наличие данных в файле о пользователе
    if os.path.exists("users.txt"):
        file = open("users.txt", "r+")
        lines = file.readlines()
        login_vvod = login.get()
        parol_vvod = parol.get()
        for line in lines:
            parts = line.strip().split(':')
            if len(parts) == 2:
                sohranenii_login, sohranenii_parol = parts
                if login_vvod == sohranenii_login and hash_parol(parol_vvod) == sohranenii_parol:
                    return True
        return False
def enter_users():  # Атвторизуем пользователя
    if proverka_users():
        messagebox.showinfo("Успех!", "Вы вошли в свой аккаунт")
        root.destroy()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")
def rules():
    rules_file = "Правила игры.docx"
    os.startfile(rules_file)

root = Tk()  # Создаем окно
root.title("Регистрация/вход")
root.geometry("400x250+730+420")
Label_login = Label(text="Логин")
Label_login.pack(padx=6, pady=6)
login = Entry(bd=2)
login.pack(padx=6, pady=6)
Label_parol = Label(text="Пароль")
Label_parol.pack(padx=6, pady=6)
parol = Entry(bd=2)
parol.pack(padx=6, pady=6)
vhod_btn1 = Button(text="Войти",command=enter_users)
vhod_btn1.pack(padx=6, pady=6)
registr_btn2 = Button(text="Зарегистрироваться",command=registr_user)
registr_btn2.pack(padx=6, pady=6)
rules_btn = tk.Button(root, text="Правила игры", command=rules)
rules_btn.place(x=160, y=210)
root.mainloop()


# Начальная позиция на доске
pole = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

selected_piece = None
current_player = 1
must_capture = False
cells = []

def get_cell(x, y):
    return y // k, x // k

def is_valid_move(start_row, start_col, end_row, end_col, player):
    if player == 1 and end_row > start_row:  # Белые не могут двигаться назад или на месте
        return False
    if player == -1 and end_row < start_row:  # Черные не могут двигаться назад или на месте
        return False
    if abs(start_row - end_row) + abs(start_col - end_col) != 1:
        return False
    return True

def is_valid_move_queen(start_row, start_col, end_row, end_col):
    if start_row != end_row and start_col != end_col:
        return False
    step_row = 1 if end_row > start_row else -1 if end_row < start_row else 0
    step_col = 1 if end_col > start_col else -1 if end_col < start_col else 0
    row, col = start_row + step_row, start_col + step_col
    while row != end_row or col != end_col:
        if pole[row][col] != 0:
            return False
        row += step_row
        col += step_col
    return True

def can_capture(start_row, start_col, end_row, end_col, player):
    if abs(start_row - end_row) != 2 and abs(start_col - end_col) != 2:
        return False
    mid_row = (start_row + end_row) // 2
    mid_col = (start_col + end_col) // 2
    if pole[mid_row][mid_col] == -player:
        return True
    return False

def can_capture_queen(start_row, start_col, end_row, end_col, player):
    if start_row == end_row or start_col == end_col:
        step_row = 1 if end_row > start_row else -1 if end_row < start_row else 0
        step_col = 1 if end_col > start_col else -1 if end_col < start_col else 0
        row, col = start_row + step_row, start_col + step_col
        captured = False
        while row != end_row or col != end_col:
            if pole[row][col] != 0:
                if pole[row][col] == -player and not captured:
                    captured = True
                else:
                    return False
            row += step_row
            col += step_col
        return captured and pole[end_row][end_col] == 0
    return False

def on_click(event):
    global selected_piece, current_player, must_capture
    row, col = get_cell(event.x, event.y)
    if 0 <= row < 8 and 0 <= col < 8:
        if event.num == 1 and current_player == 1:  # Левая кнопка мыши для белых
            handle_move(row, col, 1)
        elif event.num == 3 and current_player == -1:  # Правая кнопка мыши для черных
            handle_move(row, col, -1)

def handle_move(row, col, player):
    global selected_piece, current_player, must_capture
    if selected_piece is None:
        if pole[row][col] == player or pole[row][col] == 2 * player:
            selected_piece = (row, col)
            canvas.itemconfig(cells[row][col], fill=vid_kl)
    else:
        start_row, start_col = selected_piece
        if pole[row][col] == 0:
            start_row, start_col = selected_piece
            if is_valid_move(start_row, start_col, row, col, player):
                pole[row][col] = pole[start_row][start_col]
                pole[start_row][start_col] = 0
                redraw_board()
                selected_piece = None
                current_player = -current_player
            elif can_capture(start_row, start_col, row, col, player):
                pole[row][col] = pole[start_row][start_col]
                pole[start_row][start_col] = 0
                mid_row = (start_row + row) // 2
                mid_col = (start_col + col) // 2
                pole[mid_row][mid_col] = 0
                if (player == 1 and row == 0) or (player == -1 and row == 7):
                    pole[row][col] = 2 * player
                redraw_board()
                selected_piece = None
                if not can_capture_again(row, col, player):
                    current_player = -current_player
                if not check_game_over():
                    current_player = -current_player
            else:
                canvas.itemconfig(cells[start_row][start_col], fill=color if (start_row + start_col) % 2 == 1 else color )
                selected_piece = None

def can_capture_again(row, col, player):
    for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if can_capture(row, col, new_row, new_col, player):
                return True
    return False

def redraw_board():
    canvas.delete("all")
    for i in range(8):
        for j in range(8):
            x0, y0 = j * k, i * k
            x1, y1 = x0 + k, y0 + k
            cells[i][j] = canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", width=3)
            if pole[i][j] == 1:
                canvas.create_oval(j * k + 10, i * k + 10, j * k + k - 10, i * k + k - 10, fill=white_shashka, outline="")
            elif pole[i][j] == -1:
                canvas.create_oval(j * k + 10, i * k + 10, j * k + k - 10, i * k + k - 10, fill=black_shashka, outline="")
            elif pole[i][j] == 2:
                canvas.create_oval(j * k + 10, i * k + 10, j * k + k - 10, i * k + k - 10, fill=queen_wh, outline="")
            elif pole[i][j] == -2:
                canvas.create_oval(j * k + 10, i * k + 10, j * k + k - 10, i * k + k - 10, fill=queen_bl, outline="")
            root.state('zoomed')
            
label.config(text=f"Ход игрока {1 if current_player == 1 else 2}")

def check_game_over():
    for row in range(8):
        for col in range(8):
            piece = pole[row][col]
            if piece == 1 or piece == 2:  # Белая шашка или дамка
                white_pieces += 1
                if handle_move(row, col, 1):
                    white_can_move = True
            elif piece == -1 or piece == -2:  # Черная шашка или дамка
                black_pieces += 1
                if handle_move(row, col, -1):
                    black_can_move = True

    # Проверка на ничью (по одной шашке у каждого)
    if white_pieces == 1 and black_pieces == 1:
        end_game("Ничья!")
        return True

    # Если белые отдали все свои шашки или их заперли
    if white_pieces == 0 or not white_can_move:
        end_game("Белые победили!")
        return True

    # Если черные отдали все свои шашки или их заперли
    if black_pieces == 0 or not black_can_move:
        end_game("Черные победили!")
        return True

    return False  # Игра продолжается

def end_game(message):
    global root
    # Очищаем окно и показываем сообщение об окончании игры
    canvas.delete("all")
    canvas.create_text(4 * k, 4 * k, text=message, font=("Arial", 24), fill="red")
    root.update()


# Инициализация окна игры
root = tk.Tk()
root.title("Турецкие шашки-поддавки")
canvas = tk.Canvas(root, width=8 * k, height=8 * k, bg="white")
canvas.pack()
cells = [[None for _ in range(8)] for _ in range(8)]
redraw_board()
canvas.bind("<Button-1>", on_click)
canvas.bind("<Button-3>", on_click)
root.mainloop()
