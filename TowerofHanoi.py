import tkinter as tk
from tkinter import simpledialog, messagebox

class TowerOfHanoi:
    def __init__(self, master):
        self.master = master
        self.master.title("Tower of Hanoi")
        self.master.configure(bg="cyan")

        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="cyan")
        self.canvas.pack()

        self.message_label = tk.Label(self.master, text="", fg="red", bg="cyan")
        self.message_label.pack()

        self.num_disks = self.get_number_of_disks()
        if self.num_disks is None:
            self.master.destroy()
            return

        self.max_moves = 2 ** self.num_disks - 1
        self.towers = [[], [], []]
        self.selected_tower = None
        self.move_count = 0

        self.create_towers()
        self.draw_disks()
        self.create_info_label()
        self.create_move_counter()
        self.create_play_again_button()
        self.canvas.bind("<Button-1>", self.on_click)

    def get_number_of_disks(self):
        while True:
            try:
                num_disks = simpledialog.askinteger("Input", "Enter number of disks (3-8):", minvalue=3, maxvalue=8)
                if num_disks is None:
                    return None
                return num_disks
            except ValueError:
                self.message_label.config(text="Invalid input, please enter a number between 3 and 8")

    def create_towers(self):
        for i in range(3):
            x = 100 + i * 200
            self.canvas.create_line(x, 100, x, 300, width=5)
            self.canvas.create_line(x-50, 300, x+50, 300, width=5)

    def draw_disks(self):
        for i in range(self.num_disks, 0, -1):
            self.towers[0].append(i)
        self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("disk")
        for i in range(3):
            x = 100 + i * 200
            for j, disk in enumerate(self.towers[i]):
                width = disk * 20
                self.canvas.create_rectangle(x-width/2, 280-j*20, x+width/2, 300-j*20, fill="blue", tags="disk")

    def create_info_label(self):
        self.info_label = tk.Label(self.master, text=f"Maximum moves required: {self.max_moves}", bg="cyan")
        self.info_label.pack()

    def create_move_counter(self):
        self.move_counter_label = tk.Label(self.master, text=f"Moves: {self.move_count}", bg="cyan")
        self.move_counter_label.pack()

    def create_play_again_button(self):
        self.play_again_button = tk.Button(self.master, text="Play Again", command=self.reset_game, bg="cyan")
        self.play_again_button.pack()

    def on_click(self, event):
        clicked_tower = event.x // 200
        if self.selected_tower is None:
            if self.towers[clicked_tower]:
                self.selected_tower = clicked_tower
        else:
            if self.selected_tower != clicked_tower:
                if not self.towers[clicked_tower] or self.towers[self.selected_tower][-1] < self.towers[clicked_tower][-1]:
                    self.towers[clicked_tower].append(self.towers[self.selected_tower].pop())
                    self.move_count += 1
                    self.update_canvas()
                    self.update_move_counter()
                    self.message_label.config(text="")  # Clear any previous error message
                    if self.check_win():
                        self.message_label.config(text="Congratulations! You Won!", fg="green")
                else:
                    self.message_label.config(text="Invalid Move: Cannot place a larger disk on a smaller disk", fg="red")
            self.selected_tower = None

    def update_move_counter(self):
        self.move_counter_label.config(text=f"Moves: {self.move_count}")

    def check_win(self):
        return len(self.towers[2]) == self.num_disks and self.towers[2] == list(range(self.num_disks, 0, -1))

    def reset_game(self):
        self.num_disks = self.get_number_of_disks()
        if self.num_disks is None:
            self.master.destroy()
            return
        self.max_moves = 2 ** self.num_disks - 1
        self.towers = [[], [], []]
        self.selected_tower = None
        self.move_count = 0
        self.message_label.config(text="", fg="red")
        self.create_towers()
        self.draw_disks()
        self.info_label.config(text=f"Maximum moves required: {self.max_moves}")
        self.update_move_counter()

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()
