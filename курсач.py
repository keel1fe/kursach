import tkinter as tk
from tkinter import messagebox
import hashlib
import os

class Game:
    def __init__(self, canvas, turn_label):
        self.canvas = canvas
        self.turn_label = turn_label
        self.reset()

    def reset(self):
        self.selected = None
        self.board = GameBoard(self.canvas)
        self.turn = "white"
        self.valid_moves = {}
        self.turn_label.config(text="Первыми ходят: Белые")
        self.update()

    def update(self):
        self.board.draw_gameboard()
        self.highlight_valid_moves(self.valid_moves)

    def move_piece(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves.get((row, col), [])
            if skipped:
                self.board.remove_pieces(skipped)
            self.switch_turn()
            self.update()
            return True
        return False
    
    def highlight_valid_moves(self, moves):
        for move in moves:
            row, col = move
            x = col * 100 + 100 // 2
            y = row * 100 + 100 // 2
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="pink", outline="pink")

    def select(self, row, col):
        if self.selected:
            if not self.move_piece(row, col):
                self.selected = None
                self.select(row, col)
        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                self.update()
                return True

    def switch_turn(self):
        self.valid_moves = {}
        if self.turn == "white":
            self.turn = "black"
            self.turn_label.config(text="Ход игрока: Черные")
        else:
            self.turn = "white"
            self.turn_label.config(text="Ход игрока: Белые")

        winner = self.board.determine_winner()
        if winner:
            self.show_winner_window(winner)

    def show_winner_window(self, winner):
        self.winner_window = tk.Toplevel(self.canvas.winfo_toplevel())
        self.winner_window.title("Победитель")
        """Центрирует заданное окно на экране."""
        screen_width = self.winner_window.winfo_screenwidth()
        screen_height = self.winner_window.winfo_screenheight()
        x = (screen_width // 2) - 75
        y = (screen_height // 2) - 75
        self.winner_window.geometry(f"{300}x{150}+{x}+{y}")

        tk.Label(self.winner_window, text=winner, font=("Arial", 16)).pack(pady=20)
        tk.Button(self.winner_window, text="Начать заново", command=self.reset_and_close_winner_window).pack(pady=10)

    def reset_and_close_winner_window(self):
        self.winner_window.destroy()
        self.reset()

class Draw:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False
        self.calculate_position()

    def draw(self, canvas):
        canvas.create_oval(
            self.x - 35, self.y - 35,
            self.x + 35, self.y + 35,
            fill=self.color, outline=""
        )

        if self.queen:
            self.draw_crown(canvas)

    def draw_crown(self, canvas):
        crown_points = [
            (self.x - 15, self.y - 10), (self.x - 5, self.y - 20),  
            (self.x, self.y - 25), (self.x + 5, self.y - 20), 
            (self.x + 15, self.y - 10), (self.x + 10, self.y - 5), 
            (self.x + 5, self.y), (self.x - 5, self.y),      
            (self.x - 10, self.y - 5) 
        ]
        canvas.create_polygon(crown_points, fill="gold", outline="black", width=2)

        diamond_points = [
            (self.x, self.y - 20), (self.x + 5, self.y - 15),
            (self.x, self.y - 10), (self.x - 5, self.y - 15)  
        ]
        canvas.create_polygon(diamond_points, fill="red", outline="black", width=1)
    
    def calculate_position(self):
        self.x = 100 * self.col + 50
        self.y = 100 * self.row + 50

    def move(self, row, col):
        self.row, self.col = row, col
        self.calculate_position()

    def make_queen(self):
        self.queen = True

class GameBoard:  
    def __init__(self, canvas):
        self.canvas = canvas
        self.grid = [] 
        self.white_pieces = 16
        self.black_pieces = 16  
        self.white_queens = 0
        self.black_queens = 0  
        self.initialize_gameboard()  
    
    def initialize_gameboard(self): 
        for row in range(8):
            self.grid.append([])
            for col in range(8):
                if 1 <= row <= 2:
                    self.grid[row].append(Draw(row, col, "black"))
                elif 5 <= row <= 6:
                    self.grid[row].append(Draw(row, col, "white"))
                else:
                    self.grid[row].append(0)
    
    def draw_gameboard(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x0, y0 = col * 100, row * 100
                x1, y1 = x0 + 100, y0 + 100
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="burlywood", outline="black", width=3)
                piece = self.grid[row][col]
                if piece:
                    piece.draw(self.canvas)

    def move(self, piece, row, col):  
        self.grid[piece.row][piece.col], self.grid[row][col] = 0, piece
        piece.move(row, col)
        if row in (0, 7):
            piece.make_queen()
            if piece.color == "black":
                self.black_queens += 1
            else:
                self.white_queens += 1

    def remove_pieces(self, pieces):
        for piece in pieces:
            self.grid[piece.row][piece.col] = 0
            if piece.color == "white":
                self.white_pieces -= 1
            else:
                self.black_pieces -= 1

    def get_piece(self, row, col):
        return self.grid[row][col] if 0 <= row < 8 and 0 <= col < 8 else None

    def scan_vertical(self, start, stop, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            current = self.grid[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = skipped + last
                else:
                    moves[(r, col)] = last
                if last:
                    new_skipped = skipped + last
                    moves.update(self.scan_vertical(r + step, stop, step, color, col, skipped=new_skipped))
                    moves.update(self.scan_horizontal(col - 1, -1, -1, color, r, skipped=new_skipped))
                    moves.update(self.scan_horizontal(col + 1, 8, 1, color, r, skipped=new_skipped))
                break
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]
        return moves
    
    def scan_vertical_queen(self, start, stop, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            current = self.grid[r][col]
            if current == 0:
                if skipped:
                    moves[(r, col)] = skipped + last
                else:
                    moves[(r, col)] = last
                if last:
                    new_skipped = skipped + last
                    moves.update(self.scan_vertical(r + step, stop, step, color, col, skipped=new_skipped))
                    moves.update(self.scan_horizontal(col - 1, -1, -1, color, r, skipped=new_skipped))
                    moves.update(self.scan_horizontal(col + 1, 8, 1, color, r, skipped=new_skipped))
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]
        return moves

    def scan_horizontal(self, start, stop, step, color, row, skipped=[]):
        moves = {}
        last = []
        for c in range(start, stop, step):
            current = self.grid[row][c]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, c)] = skipped + last
                else:
                    moves[(row, c)] = last
                if last:
                    new_skipped = skipped + last
                    moves.update(self.scan_horizontal(c + step, stop, step, color, row, skipped=new_skipped))
                    moves.update(self.scan_vertical(row - 1, -1, -1, color, c, skipped=new_skipped))
                    moves.update(self.scan_vertical(row + 1, 8, 1, color, c, skipped=new_skipped))
                break
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]
        return moves

    def scan_horizontal_queen(self, start, stop, step, color, row, skipped=[]):
        moves = {}
        last = []
        for c in range(start, stop, step):
            current = self.grid[row][c]
            if current == 0:
                if skipped:
                    moves[(row, c)] = skipped + last
                else:
                    moves[(row, c)] = last
                if last:
                    new_skipped = skipped + last
                    moves.update(self.scan_horizontal(c + step, stop, step, color, row, skipped=new_skipped))
                    moves.update(self.scan_vertical(row - 1, -1, -1, color, c, skipped=new_skipped))
                    moves.update(self.scan_vertical(row + 1, 8, 1, color, c, skipped=new_skipped))
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]
        return moves
    
    def get_valid_moves(self, piece):
        moves = {}
        row, col = piece.row, piece.col

        if piece.color == "white" and not piece.queen:
            moves.update(self.scan_vertical(row - 1, -1, -1, piece.color, col))  
            moves.update(self.scan_horizontal(col - 1, -1, -1, piece.color, row)) 
            moves.update(self.scan_horizontal(col + 1, 8, 1, piece.color, row))
        elif piece.color == "black" and not piece.queen:
            moves.update(self.scan_vertical(row + 1, 8, 1, piece.color, col))
            moves.update(self.scan_horizontal(col - 1, -1, -1, piece.color, row))
            moves.update(self.scan_horizontal(col + 1, 8, 1, piece.color, row))
        elif piece.queen:
            moves.update(self.scan_vertical_queen(row - 1, -1, -1, piece.color, col))  
            moves.update(self.scan_vertical_queen(row + 1, 8, 1, piece.color, col))
            moves.update(self.scan_horizontal_queen(col - 1, -1, -1, piece.color, row)) 
            moves.update(self.scan_horizontal_queen(col + 1, 8, 1, piece.color, row))

        capture_moves = {pos: skipped for pos, skipped in moves.items() if skipped}
        if capture_moves:
            max_captures = max(len(skipped) for skipped in capture_moves.values())
            return {pos: skipped for pos, skipped in capture_moves.items() if len(skipped) == max_captures}

        return moves
    
    def determine_winner(self):
        if self.black_pieces <= 1:
            return "Победили Белые"
        elif self.white_pieces <= 1:
            return "Победили Черные"
        elif self.white_pieces == 1 and self.black_pieces == 1:
            return "Ничья"
        return None

def get_row_col(event):
    return event.y // 100, event.x // 100

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_user_exists(username):
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[0] == username:
                    return True
    return False

def authenticate(username, password):
    hashed_password = hash_password(password)
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2 and parts[0] == username and parts[1] == hashed_password:
                    return True
    return False

def add_user(username, password):
    if check_user_exists(username):
        return False
    hashed_password = hash_password(password)
    with open("users.txt", "a") as file:
        file.write(f"{username}:{hashed_password}\n")
    return True

class AuthForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Регистрация/вход")
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        tk.Label(self.frame, text="Логин").pack(padx=6, pady=6)
        self.login_entry = tk.Entry(self.frame, bd=2)
        self.login_entry.pack(padx=6, pady=6)

        tk.Label(self.frame, text="Пароль").pack(padx=6, pady=6)
        self.password_entry = tk.Entry(self.frame, bd=2, show='*')
        self.password_entry.pack(padx=6, pady=6)

        tk.Button(self.frame, text="Войти", command=self.login, width=15).pack(padx=6, pady=6)
        tk.Button(self.frame, text="Зарегистрироваться", command=self.register, width=20).pack(padx=6, pady=6)
        tk.Button(self.frame, text="Правила игры", command=self.show_rules, width=15).pack(padx=6, pady=10)

        """Центрирует окно на экране."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 350) // 2
        y = (screen_height - 325) // 2
        self.root.geometry(f"{350}x{290}+{x}+{y}")

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        if authenticate(username, password):
            messagebox.showinfo("Успех!", "Вы вошли в свой аккаунт")
            self.root.destroy()
            start_checkers_game()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль.")

    def register(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Ошибка", "Логин и пароль должны быть заполнены.")
        elif check_user_exists(username):
            messagebox.showerror("Ошибка", "Учетная запись уже существует.")
        else:
            add_user(username, password)
            messagebox.showinfo("Успех", "Регистрация успешно завершена.\nВойдите в аккаунт")

    def show_rules(self):
        rules_file = "правила шашек.pdf"
        if os.path.exists(rules_file):
            os.startfile(rules_file)
        else:
            messagebox.showerror("Ошибка", "Файл с правилами не найден.")

class CheckersGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Турецкие шашки-поддавки")

        self.button_frame = tk.Frame(root).pack(pady=10)

        self.turn_label = tk.Label(text="Первыми ходят: Белые", font=("Arial", 16), bg="lightgray")
        self.turn_label.pack(side=tk.BOTTOM, anchor=tk.NE, padx=10, pady=10)

        self.canvas = tk.Canvas(root, width=800, height=800)
        self.canvas.pack()
        self.game = Game(self.canvas, self.turn_label)

        root.state('zoomed')
        self.canvas.bind("<Button-1>", self.on_click)
        self.update_game()

    def on_click(self, event):
        row, col = get_row_col(event)
        self.game.select(row, col)

def start_checkers_game():
    root = tk.Tk()
    CheckersGame(root)
    root.mainloop()

root = tk.Tk()
AuthForm(root)
root.mainloop()
