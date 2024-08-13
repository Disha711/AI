import tkinter as tk
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.configure(bg="cyan")

        self.mode = "player_vs_bot"  # Default mode
        self.current_player = "X"

        self.create_ui()
        self.window.mainloop()

    def create_ui(self):
        # Mode selection
        mode_frame = tk.Frame(self.window, bg="cyan")
        mode_frame.pack()

        tk.Label(mode_frame, text="Choose game mode:", bg="cyan").pack()

        self.player_vs_bot_button = tk.Button(mode_frame, text="Player vs Bot", command=self.set_mode_player_vs_bot)
        self.player_vs_bot_button.pack(side=tk.LEFT)

        self.player_vs_player_button = tk.Button(mode_frame, text="Player vs Player", command=self.set_mode_player_vs_player)
        self.player_vs_player_button.pack(side=tk.RIGHT)

        # Game buttons
        self.buttons_frame = tk.Frame(self.window, bg="cyan")
        self.buttons_frame.pack()

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.buttons_frame, text="", font=('normal', 40), width=5, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        # Status label
        self.status_label = tk.Label(self.window, text="", font=('normal', 20), bg="cyan")
        self.status_label.pack()

        # Play Again button
        self.play_again_button = tk.Button(self.window, text="Play Again", command=self.reset_game)
        self.play_again_button.pack()

    def set_mode_player_vs_bot(self):
        self.mode = "player_vs_bot"

    def set_mode_player_vs_player(self):
        self.mode = "player_vs_player"

    def on_button_click(self, row, col):
        if self.buttons[row][col]["text"] == "" and self.status_label["text"] == "":
            self.buttons[row][col]["text"] = self.current_player
            if self.check_winner(self.current_player):
                self.status_label.config(text=f"Player {self.current_player} wins!")
            elif self.is_draw():
                self.status_label.config(text="It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.mode == "player_vs_bot" and self.current_player == "O":
                    self.bot_move()

    def bot_move(self):
        _, move = self.minimax(self.current_player, -float('inf'), float('inf'))
        row, col = move
        self.buttons[row][col]["text"] = "O"
        if self.check_winner("O"):
            self.status_label.config(text="Player O wins!")
        elif self.is_draw():
            self.status_label.config(text="It's a draw!")
        else:
            self.current_player = "X"

    def minimax(self, player, alpha, beta):
        opponent = "O" if player == "X" else "X"
        if self.check_winner("O"):
            return 1, None
        if self.check_winner("X"):
            return -1, None
        if self.is_draw():
            return 0, None

        best_move = None
        if player == "O":
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = player
                        score, _ = self.minimax(opponent, alpha, beta)
                        self.buttons[i][j]["text"] = ""
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            break
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]["text"] == "":
                        self.buttons[i][j]["text"] = player
                        score, _ = self.minimax(opponent, alpha, beta)
                        self.buttons[i][j]["text"] = ""
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
                        beta = min(beta, score)
                        if beta <= alpha:
                            break
        return best_score, best_move

    def check_winner(self, player):
        for i in range(3):
            if all(self.buttons[i][j]["text"] == player for j in range(3)) or \
               all(self.buttons[j][i]["text"] == player for j in range(3)):
                return True
        if all(self.buttons[i][i]["text"] == player for i in range(3)) or \
           all(self.buttons[i][2 - i]["text"] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def reset_game(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]["text"] = ""
        self.current_player = "X"
        self.status_label.config(text="")

if __name__ == "__main__":
    TicTacToe()
