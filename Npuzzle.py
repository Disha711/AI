import tkinter as tk
from tkinter import simpledialog, messagebox

class NQueenGame:
    def __init__(self, root, n):
        self.root = root
        self.n = n
        self.board = [[0] * n for _ in range(n)]
        self.buttons = [[None] * n for _ in range(n)]
        self.root.title("N-Queen Problem")
        self.root.configure(bg="lightblue")
        self.create_board()
        self.create_controls()
    
    def create_board(self):
        for row in range(self.n):
            for col in range(self.n):
                button = tk.Button(self.root, width=4, height=2, font=("Arial", 16), command=lambda r=row, c=col: self.toggle_queen(r, c))
                button.grid(row=row, column=col, padx=1, pady=1)
                self.buttons[row][col] = button
                if (row + col) % 2 == 0:
                    button.configure(bg="white")
                else:
                    button.configure(bg="gray")
    
    def create_controls(self):
        control_frame = tk.Frame(self.root, bg="lightblue")
        control_frame.grid(row=self.n, column=0, columnspan=self.n, pady=10)
        
        check_button = tk.Button(control_frame, text="Check Answer", command=self.check_solution, font=("Arial", 14), bg="green", fg="white")
        check_button.pack(side=tk.LEFT, padx=5)
        
        restart_button = tk.Button(control_frame, text="Restart", command=self.restart_game, font=("Arial", 14), bg="red", fg="white")
        restart_button.pack(side=tk.LEFT, padx=5)
    
    def toggle_queen(self, row, col):
        if self.board[row][col] == 0:
            self.board[row][col] = 1
            self.buttons[row][col].config(text="Q", bg="yellow", fg="black")
            if not self.is_valid_position(row, col):
                self.board[row][col] = 0
                self.buttons[row][col].config(text="", bg="red")
                self.root.after(500, lambda: self.buttons[row][col].config(bg="white" if (row + col) % 2 == 0 else "gray"))
                messagebox.showerror("Invalid Move", "A queen cannot be placed here. It conflicts with another queen.")
        else:
            self.board[row][col] = 0
            self.buttons[row][col].config(text="", bg="white" if (row + col) % 2 == 0 else "gray")
    
    def is_valid_position(self, row, col):
        for i in range(self.n):
            if i != row and self.board[i][col] == 1:
                return False
        for j in range(self.n):
            if j != col and self.board[row][j] == 1:
                return False
        for i in range(self.n):
            for j in range(self.n):
                if (i != row or j != col) and self.board[i][j] == 1:
                    if abs(i - row) == abs(j - col):
                        return False
        return True
    
    def check_solution(self):
        if self.is_valid_solution():
            messagebox.showinfo("N-Queen Problem", "Congratulations! The solution is correct.")
        else:
            messagebox.showerror("N-Queen Problem", "The solution is incorrect. Try again.")
    
    def is_valid_solution(self):
        queens = sum(sum(row) for row in self.board)
        if queens != self.n:
            return False
        for row in range(self.n):
            for col in range(self.n):
                if self.board[row][col] == 1 and not self.is_valid_position(row, col):
                    return False
        return True
    
    def restart_game(self):
        self.board = [[0] * self.n for _ in range(self.n)]
        for row in range(self.n):
            for col in range(self.n):
                self.buttons[row][col].config(text="", bg="white" if (row + col) % 2 == 0 else "gray")

if __name__ == "__main__":
    root = tk.Tk()
    n = simpledialog.askinteger("N-Queen Problem", "Enter the number of queens:", minvalue=4, maxvalue=20)
    if n:
        game = NQueenGame(root, n)
        root.mainloop()
