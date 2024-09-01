import tkinter as tk
from tkinter import messagebox
import random

class Puzzle:
    def __init__(self):
        self.size = 3
        self.board = self.generate_solved_board()
        self.empty_tile = (2, 2)  # Position of the empty tile
        self.shuffle_board()

    def generate_solved_board(self):
        return [[(i * self.size + j + 1) % (self.size ** 2) for j in range(self.size)] for i in range(self.size)]

    def shuffle_board(self):
        """ Shuffle the board randomly. """
        for _ in range(1000):  # Number of shuffle moves
            self.move_random()

    def move_random(self):
        """ Move a tile randomly. """
        x, y = self.empty_tile
        possible_moves = []
        if x > 0: possible_moves.append((x - 1, y))  # Move tile from above
        if x < self.size - 1: possible_moves.append((x + 1, y))  # Move tile from below
        if y > 0: possible_moves.append((x, y - 1))  # Move tile from the left
        if y < self.size - 1: possible_moves.append((x, y + 1))  # Move tile from the right
        
        move_to = random.choice(possible_moves)
        self.swap_tiles(self.empty_tile, move_to)
        self.empty_tile = move_to

    def swap_tiles(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        self.board[x1][y1], self.board[x2][y2] = self.board[x2][y2], self.board[x1][y1]

    def move_tile(self, tile_position):
        x, y = self.empty_tile
        tx, ty = tile_position
        if abs(x - tx) + abs(y - ty) == 1:
            self.swap_tiles(self.empty_tile, tile_position)
            self.empty_tile = tile_position

    def is_solved(self):
        return self.board == self.generate_solved_board()

    def reset(self):
        self.board = self.generate_solved_board()
        self.empty_tile = (self.size - 1, self.size - 1)
        self.shuffle_board()

class PuzzleGUI:
    def __init__(self, root):
        self.puzzle = Puzzle()
        self.root = root
        self.root.title("Number Puzzle Game")
        self.buttons = [[None for _ in range(self.puzzle.size)] for _ in range(self.puzzle.size)]
        self.create_widgets()
        self.update_buttons()

    def create_widgets(self):
        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):
                button = tk.Button(self.root, text='', font=('Helvetica', 20, 'bold'), width=4, height=2,
                                   command=lambda x=i, y=j: self.on_button_click(x, y),
                                   relief=tk.RAISED, borderwidth=2, bg='lightblue', fg='black')
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button
        
        # Add Reset Button
        reset_button = tk.Button(self.root, text='Reset', font=('Helvetica', 16, 'bold'), command=self.reset_game,
                                 relief=tk.RAISED, borderwidth=2, bg='lightgreen', fg='black')
        reset_button.grid(row=self.puzzle.size, column=0, columnspan=self.puzzle.size, pady=10, sticky='ew')

    def update_buttons(self):
        for i in range(self.puzzle.size):
            for j in range(self.puzzle.size):
                tile = self.puzzle.board[i][j]
                if tile == 0:
                    self.buttons[i][j].config(text='', bg='white')
                else:
                    self.buttons[i][j].config(text=str(tile), bg='lightblue')

    def on_button_click(self, x, y):
        if (abs(x - self.puzzle.empty_tile[0]) + abs(y - self.puzzle.empty_tile[1])) == 1:
            self.puzzle.move_tile((x, y))
            self.update_buttons()
            if self.puzzle.is_solved():
                messagebox.showinfo("Congratulations", "You solved the puzzle!")

    def reset_game(self):
        self.puzzle.reset()
        self.update_buttons()

def main():
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
