import tkinter as tk


class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.canvas = tk.Canvas(master, width=700, height=600, bg="blue")
        self.canvas.pack()
        self.draw_board()
        self.current_player = "red"
        self.board = [[" " for _ in range(7)] for _ in range(6)]
        self.canvas.bind("<Button-1>", self.drop_piece)

    def draw_board(self):
        for row in range(6):
            for col in range(7):
                x1, y1 = col * 100, row * 100
                x2, y2 = x1 + 100, y1 + 100
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")

    def drop_piece(self, event):
        col = event.x // 100
        for row in range(5, -1, -1):
            if self.board[row][col] == " ":
                x, y = col * 100 + 50, row * 100 + 50
                self.canvas.create_oval(
                    x - 45, y - 45, x + 45, y + 45, fill=self.current_player
                )
                self.board[row][col] = self.current_player
                if self.check_winner():
                    self.canvas.unbind("<Button-1>")
                    self.master.title(f"{self.current_player.capitalize()} wins!")
                else:
                    self.current_player = (
                        "yellow" if self.current_player == "red" else "red"
                    )
                break

    def check_winner(self):
        for row in range(6):
            for col in range(4):
                if (
                    self.board[row][col] == self.current_player
                    and self.board[row][col + 1] == self.current_player
                    and self.board[row][col + 2] == self.current_player
                    and self.board[row][col + 3] == self.current_player
                ):
                    return True

        for row in range(3):
            for col in range(7):
                if (
                    self.board[row][col] == self.current_player
                    and self.board[row + 1][col] == self.current_player
                    and self.board[row + 2][col] == self.current_player
                    and self.board[row + 3][col] == self.current_player
                ):
                    return True

        for row in range(3):
            for col in range(4):
                if (
                    self.board[row][col] == self.current_player
                    and self.board[row + 1][col + 1] == self.current_player
                    and self.board[row + 2][col + 2] == self.current_player
                    and self.board[row + 3][col + 3] == self.current_player
                ):
                    return True

                if (
                    self.board[row][col + 3] == self.current_player
                    and self.board[row + 1][col + 2] == self.current_player
                    and self.board[row + 2][col + 1] == self.current_player
                    and self.board[row + 3][col] == self.current_player
                ):
                    return True

        return False


root = tk.Tk()
game = ConnectFourGUI(root)
root.mainloop()
