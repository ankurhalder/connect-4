class ConnectFour:
    def __init__(self):
        self.board = [[" " for _ in range(7)] for _ in range(6)]
        self.current_player = "X"

    def print_board(self):
        for row in self.board:
            print("|".join(row))
        print("-------------")

    def drop_piece(self, col):
        for row in range(5, -1, -1):
            if self.board[row][col] == " ":
                self.board[row][col] = self.current_player
                return True
        return False

    def is_winner(self, player):
        for row in range(6):
            for col in range(4):
                if (
                    self.board[row][col] == player
                    and self.board[row][col + 1] == player
                    and self.board[row][col + 2] == player
                    and self.board[row][col + 3] == player
                ):
                    return True

        for row in range(3):
            for col in range(7):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col] == player
                    and self.board[row + 2][col] == player
                    and self.board[row + 3][col] == player
                ):
                    return True

        for row in range(3):
            for col in range(4):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col + 1] == player
                    and self.board[row + 2][col + 2] == player
                    and self.board[row + 3][col + 3] == player
                ):
                    return True

                if (
                    self.board[row][col + 3] == player
                    and self.board[row + 1][col + 2] == player
                    and self.board[row + 2][col + 1] == player
                    and self.board[row + 3][col] == player
                ):
                    return True

        return False

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True

    def play(self):
        while True:
            self.print_board()
            col = int(input(f"Player {self.current_player}, enter column (0-6): "))
            if col < 0 or col > 6:
                print("Invalid column! Column must be between 0 and 6.")
                continue
            if self.drop_piece(col):
                if self.is_winner(self.current_player):
                    print(f"Player {self.current_player} wins!")
                    break
                if self.is_full():
                    print("It's a draw!")
                    break
                self.current_player = "O" if self.current_player == "X" else "X"
            else:
                print("Column is full! Please choose another column.")


if __name__ == "__main__":
    game = ConnectFour()
    game.play()
