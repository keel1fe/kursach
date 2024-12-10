import tkinter as tk
from tkinter import *
import os

def regis():  # регистрация пользователя
    global txt, txtl, txtp, login, password, lab

    def dismiss(win_t):
        win_t.grab_release()
        win_t.destroy()

    s_l = login.get()
    s_p = password.get()
    if len(s_l) == 0 or len(s_p) == 0:
        win = Toplevel(root, relief=SUNKEN)
        win.geometry("400x100+730+420")
        win.title("Регистрация / Авторизация")
        win.minsize(width=400, height=100)
        win.maxsize(width=400, height=100)
        win.protocol("WM_DELETE_WINDOW", lambda: dismiss(win))  # перехватываем нажатие на крестик
        Label(win, text='Пуcтое поле "Логин" или "Пароль"', font=("Arial", 14, 'bold')).place(x=30, y=10)
        close_button = tk.Button(win, text="Повторить ввод", command=lambda: dismiss(win))
        close_button.place(x=150, y=50)
        win.grab_set()  # захватываем пользовательский ввод
    else:
        f_reg = False
        file = open("l_p.txt", "r+")  # открываем файл
        a = file.read().split()  # читаем файл
        for j in range(len(a)):  # ищем совпадение логин и пароль
            if a[j] == s_l and a[j + 1] == s_p:
                f_reg = True
                break
        if not f_reg:  # совпадения нет
            file.seek(0, os.SEEK_END)
            file.write(s_l + ' ' + s_p + ' ')  # записываем новые логин и пароль
        file.close()
        win_r = Toplevel(root, relief=SUNKEN)
        win_r.geometry("400x100+730+420")
        win_r.title("Регистрация / Авторизация")
        win_r.minsize(width=400, height=100)
        win_r.maxsize(width=400, height=100)
        win_r.protocol("WM_DELETE_WINDOW", lambda: dismiss(win_r))  # перехватываем нажатие на крестик
        Label(win_r, text="Уважаемый(-ая) " + s_l + ", вы успешно" + "\n зарегистрировались /авторизовались",
              font=("Arial", 14, 'bold')).place(x=5, y=10)
        close_button = tk.Button(win_r, text="Начать игру", command=lambda: [dismiss(win_r), start_game()])
        close_button.place(x=150, y=65)
        win_r.grab_set()  # захватываем пользовательский ввод
        txt.place_forget()  # стираем виджеты регистрации
        txtl.place_forget()
        txtp.place_forget()
        login.place_forget()
        password.place_forget()
        close_but.place_forget()

def start_game():
    global canvas

    # Цвета клеток
    light_color = "white"  # Цвет светлых клеток
    dark_color = "gray"    # Цвет темных клеток

    # Цвета фигур
    white_piece_color = "white"  # Цвет белых фигур
    black_piece_color = "black"  # Цвет черных фигур

    # Размер клетки
    global k
    k = 100

    # Создание игрового поля
    canvas = Canvas(root, width=8 * k, height=8 * k, bg="white")
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Центрируем холст

    # Рисуем игровое поле
    for i in range(8):
        for j in range(8):
            x0, y0 = j * k, i * k
            x1, y1 = x0 + k, y0 + k
            if (i + j) % 2 == 0:
                canvas.create_rectangle(x0, y0, x1, y1, fill=light_color, outline="")  # Светлая клетка
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill=dark_color, outline="")  # Темная клетка
    root.state('zoomed')
    # Размещаем фигуры на поле
    for i in range(8):
        for j in range(8):
            if pole[i][j] == 1:
                canvas.create_oval(j * k + 10, i * k + 10, j * k + k - 10, i * k + k - 10, fill=white_piece_color, outline="")  # Белая фигура
            elif pole[i][j] == -1:
                canvas.create_oval(j * k + 10, i * k + 10, j * k + k - 10, i * k + k - 10, fill=black_piece_color, outline="")  # Черная фигура

# Создание главного окна
root = Tk()
root.title('Курсовая Работа: Турецкий шашки-поддавки')  # заголовок окна
root.geometry("530x300+550+350")  # Устанавливаем начальный размер окна для регистрации

# Игровое поле
pole = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# Регистрация и авторизация
txt = Label(root, text="Для игры введите Ваш логин и пароль\nДля регистрации введите новый логин и пароль",
            font=("Arial", 14, 'bold'))
txt.place(x=40, y=20)
txtl = Label(root, text='Логин', font=("Arial", 14, 'bold'))
txtl.place(x=70, y=90)
login = tk.Entry(root, width=10, bd=3)
login.place(x=170, y=94)
txtp = Label(root, text='Пароль', font=("Arial", 14, 'bold'))
txtp.place(x=70, y=130)
password = tk.Entry(root, width=10, bd=3)
password.place(x=170, y=130)
close_but = tk.Button(root, text="Зарегистрироваться / начать игру", command=regis)
close_but.place(x=70, y=180)

mainloop()