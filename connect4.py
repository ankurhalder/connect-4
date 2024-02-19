import tkinter as tk
from tkinter import messagebox
import random


class HomePage:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.master.geometry("500x400")

        # Heading
        self.heading_label = tk.Label(
            master, text="Connect Four Game", font=("Helvetica", 24)
        )
        self.heading_label.pack(pady=20)

        # Subheading
        self.subheading_label = tk.Label(
            master, text="Created by Ankur Halder", font=("Helvetica", 12)
        )
        self.subheading_label.pack()

        # Buttons
        self.start_button = tk.Button(
            master, text="Start Game", command=self.start_game
        )
        self.start_button.pack(pady=20)

        self.exit_button = tk.Button(master, text="Exit Game", command=self.exit_game)
        self.exit_button.pack(pady=10)

        # Footer
        self.footer_label = tk.Label(
            master,
            text="Explore more projects like this visit ankurhalder.in",
            font=("Helvetica", 10),
            fg="blue",
            cursor="hand2",
        )
        self.footer_label.pack(pady=20)
        self.footer_label.bind(
            "<Button-1>", lambda e: self.open_website("https://ankurhalder.in")
        )

    def start_game(self):
        self.master.destroy()
        game_window = tk.Tk()
        game = ConnectFourGUI(game_window)
        game_window.mainloop()

    def exit_game(self):
        self.master.destroy()

    def open_website(self, url):
        import webbrowser

        webbrowser.open(url)


class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")

        self.canvas = tk.Canvas(master, width=700, height=600, bg="blue")
        self.canvas.pack()

        self.board = [[" " for _ in range(7)] for _ in range(6)]
        self.current_player = "red"
        self.create_board()
        self.message_var = tk.StringVar()
        self.message_var.set("Player Red's Turn")
        self.message_label = tk.Label(
            master,
            textvariable=self.message_var,
            font=("Helvetica", 18),
            bg="blue",
            fg="white",
        )
        self.message_label.pack(pady=10)

        self.canvas.bind("<Motion>", self.highlight_column)
        self.canvas.bind("<Button-1>", self.drop_piece)

    def create_board(self):
        self.rectangles = []
        for row in range(6):
            row_rects = []
            for col in range(7):
                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill="yellow", outline="black", width=2
                )
                row_rects.append(rect_id)
            self.rectangles.append(row_rects)

    def highlight_column(self, event):
        col = event.x // 100
        self.canvas.delete("highlight")
        if 0 <= col <= 6:
            x1, y1 = col * 100, 0
            x2, y2 = x1 + 100, 600
            self.canvas.create_rectangle(
                x1, y1, x2, y2, fill="", outline="white", width=3, tags="highlight"
            )

    def drop_piece(self, event):
        col = event.x // 100
        for row in range(5, -1, -1):
            if self.board[row][col] == " ":
                x, y = col * 100 + 50, row * 100 + 50
                self.canvas.create_oval(
                    x - 45, y - 45, x + 45, y + 45, fill=self.current_player
                )
                self.board[row][col] = self.current_player
                if self.check_winner(row, col):
                    self.end_game(f"Player {self.current_player.capitalize()} Wins!")
                elif self.is_board_full():
                    self.end_game("It's a Draw!")
                else:
                    self.current_player = (
                        "yellow" if self.current_player == "red" else "red"
                    )
                    self.message_var.set(
                        f"Player {self.current_player.capitalize()}'s Turn"
                    )
                    if self.current_player == "yellow":
                        self.ai_move()
                break

    def check_winner(self, row, col):
        # Check horizontally
        for c in range(col - 3, col + 1):
            if (
                0 <= c <= 3
                and self.board[row][c] == self.current_player
                and self.board[row][c + 1] == self.current_player
                and self.board[row][c + 2] == self.current_player
                and self.board[row][c + 3] == self.current_player
            ):
                return True

        # Check vertically
        for r in range(row - 3, row + 1):
            if (
                0 <= r <= 2
                and self.board[r][col] == self.current_player
                and self.board[r + 1][col] == self.current_player
                and self.board[r + 2][col] == self.current_player
                and self.board[r + 3][col] == self.current_player
            ):
                return True

        # Check diagonally (positive slope)
        for r, c in zip(range(row - 3, row + 1), range(col - 3, col + 1)):
            if (
                0 <= r <= 2
                and 0 <= c <= 3
                and self.board[r][c] == self.current_player
                and self.board[r + 1][c + 1] == self.current_player
                and self.board[r + 2][c + 2] == self.current_player
                and self.board[r + 3][c + 3] == self.current_player
            ):
                return True

        # Check diagonally (negative slope)
        for r, c in zip(range(row + 3, row - 1, -1), range(col - 3, col + 1)):
            if (
                3 <= r <= 5
                and 0 <= c <= 3
                and self.board[r][c] == self.current_player
                and self.board[r - 1][c + 1] == self.current_player
                and self.board[r - 2][c + 2] == self.current_player
                and self.board[r - 3][c + 3] == self.current_player
            ):
                return True

        return False

    def is_board_full(self):
        for row in self.board:
            if " " in row:
                return False
        return True

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.master.destroy()
        closing_window = tk.Tk()
        closing_page = ClosingPage(closing_window)
        closing_window.mainloop()

    def ai_move(self):
        if self.current_player == "yellow":
            col = self.get_ai_move()
            if col is not None:
                self.drop_piece_ai(col)

    def get_ai_move(self):
        best_score = -float("inf")
        best_col = None

        for col in range(7):
            row = self.get_next_open_row(col)
            if row is not None:
                score = self.evaluate_move(row, col)
                if score > best_score:
                    best_score = score
                    best_col = col

        return best_col

    def get_next_open_row(self, col):
        for row in range(5, -1, -1):
            if self.board[row][col] == " ":
                return row
        return None

    def evaluate_move(self, row, col):
        score = 0

        # Check for potential horizontal wins
        for i in range(col - 3, col + 1):
            if 0 <= i <= 6:
                pieces = self.board[row][i : i + 4]
                score += self.score_pieces(pieces)

        # Check for potential vertical wins
        for i in range(row - 3, row + 1):
            if 0 <= i <= 5:
                pieces = [self.board[i][col]] * 4
                score += self.score_pieces(pieces)

        # Check for potential diagonal wins
        for i in range(-3, 4):
            if 0 <= row + i <= 5 and 0 <= col + i <= 6:
                pieces = [self.board[row + i][col + i]] * 4
                score += self.score_pieces(pieces)
            if 0 <= row - i <= 5 and 0 <= col + i <= 6:
                pieces = [self.board[row - i][col + i]] * 4
                score += self.score_pieces(pieces)

        return score

    def score_pieces(self, pieces):
        score = 0
        num_empty = pieces.count(" ")
        if num_empty == 4:
            return 0
        if num_empty == 3:
            score += 5  # Prioritize moves that create immediate winning opportunities
        elif num_empty == 2:
            score += 2  # Favor moves closer to winning
        elif num_empty == 1:
            score += 1  # Consider moves that block opponent's progress

        if pieces.count("red") == 4:
            score = -100  # Avoid moves that lead to opponent's win
        elif pieces.count("yellow") == 4:
            score += 100  # Prioritize moves that create immediate winning opportunities for AI

        return score


class ClosingPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.master.geometry("500x400")

        # Heading
        self.heading_label = tk.Label(
            master, text="Connect Four Game", font=("Helvetica", 24)
        )
        self.heading_label.pack(pady=20)

        # Subheading
        self.subheading_label = tk.Label(
            master, text="Created by Ankur Halder", font=("Helvetica", 12)
        )
        self.subheading_label.pack()

        # Buttons
        self.play_again_button = tk.Button(
            master, text="Play Again", command=self.play_again
        )
        self.play_again_button.pack(pady=20)

        self.exit_button = tk.Button(master, text="Exit Game", command=self.exit_game)
        self.exit_button.pack(pady=10)

        # Footer
        self.footer_label = tk.Label(
            master,
            text="Explore more projects like this visit ankurhalder.in",
            font=("Helvetica", 10),
            fg="blue",
            cursor="hand2",
        )
        self.footer_label.pack(pady=20)
        self.footer_label.bind(
            "<Button-1>", lambda e: self.open_website("https://ankurhalder.in")
        )

    def play_again(self):
        self.master.destroy()
        root = tk.Tk()
        home_page = HomePage(root)
        root.mainloop()

    def exit_game(self):
        self.master.destroy()

    def open_website(self, url):
        import webbrowser

        webbrowser.open(url)


root = tk.Tk()
home_page = HomePage(root)
root.mainloop()
