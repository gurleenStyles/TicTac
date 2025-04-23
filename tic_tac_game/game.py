import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
import time

class TicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe - Blue Edition")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg='#cce7ff')

        self.shared_data = {
            "player1": tk.StringVar(),
            "player2": tk.StringVar(),
            "winner": tk.StringVar()
        }

        self.frames = {}
        for F in (StartPage, GamePage, ResultPage):
            frame = F(parent=self, controller=self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#cce7ff')
        self.controller = controller

        tk.Label(self, text="Enter Player Names", font=('Helvetica', 20), bg='#cce7ff').pack(pady=20)

        tk.Label(self, text="Player 1 (X):", bg='#cce7ff').pack(pady=5)
        tk.Entry(self, textvariable=controller.shared_data["player1"]).pack()

        tk.Label(self, text="Player 2 (O):", bg='#cce7ff').pack(pady=5)
        tk.Entry(self, textvariable=controller.shared_data["player2"]).pack()

        tk.Button(self, text="Start Game", font=('Helvetica', 14), bg='#80bfff', command=lambda: controller.show_frame(GamePage)).pack(pady=20)


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#99ccff')
        self.controller = controller

        self.current_player = "X"
        self.move_history = []
        self.move_count = 0
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_widgets()

    def create_widgets(self):
        self.title = tk.Label(self, text="Tic Tac Toe", font=('Helvetica', 18), bg='#99ccff')
        self.title.pack(pady=10)

        self.frame = tk.Frame(self, bg='#99ccff')
        self.frame.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.frame, text="", font=('Helvetica', 24), width=5, height=2,
                                   bg='#b3d9ff', activebackground='#80bfff',
                                   command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def on_click(self, row, col):
        if self.board[row][col] is not None:
            return

        self.animate_button(row, col)
        self.buttons[row][col]["text"] = self.current_player
        self.board[row][col] = self.current_player
        self.move_history.append((row, col))
        self.move_count += 1

        if self.check_winner():
            winner_name = self.controller.shared_data["player1"].get() if self.current_player == "X" else self.controller.shared_data["player2"].get()
            self.controller.shared_data["winner"].set(f"{winner_name} Wins!")
            self.controller.show_frame(ResultPage)
            return

        if self.move_count % 3 == 0:
            erased_row, erased_col = self.move_history.pop(0)
            self.board[erased_row][erased_col] = None
            self.buttons[erased_row][erased_col]["text"] = ""

        self.current_player = "O" if self.current_player == "X" else "X"

    def animate_button(self, row, col):
        for _ in range(3):
            self.buttons[row][col].configure(bg="#80ccff")
            self.update()
            time.sleep(0.1)
            self.buttons[row][col].configure(bg="#b3d9ff")
            self.update()
            time.sleep(0.1)

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] is not None:
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] is not None:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return True

        return False


class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#cce7ff')
        self.controller = controller

        self.result_label = tk.Label(self, text="", font=('Helvetica', 20), bg='#cce7ff')
        self.result_label.pack(pady=40)

        tk.Button(self, text="Play Again", font=('Helvetica', 14), bg='#80bfff', command=self.restart_game).pack(pady=20)

    def tkraise(self, *args, **kwargs):
        self.result_label.config(text=self.controller.shared_data["winner"].get())
        super().tkraise(*args, **kwargs)

    def restart_game(self):
        self.controller.frames[GamePage] = GamePage(self.controller, self.controller)
        self.controller.frames[GamePage].place(relwidth=1, relheight=1)
        self.controller.show_frame(GamePage)


if __name__ == '__main__':
    app = TicTacToeApp()
    app.mainloop()