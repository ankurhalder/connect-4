import tkinter as tk


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
        self.message_var.set(message)
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Motion>")


root = tk.Tk()
game = ConnectFourGUI(root)
root.mainloop()
