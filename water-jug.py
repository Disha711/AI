import tkinter as tk
from tkinter import messagebox

class Jug:
    def __init__(self, capacity):
        self.capacity = capacity
        self.amount = 0

    def fill(self):
        self.amount = self.capacity

    def empty(self):
        self.amount = 0

    def pour_into(self, other_jug):
        amount_to_pour = min(self.amount, other_jug.capacity - other_jug.amount)
        self.amount -= amount_to_pour
        other_jug.amount += amount_to_pour

    def __str__(self):
        return f"{self.amount}/{self.capacity}"

class WaterJugApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Problem")

        self.num_jugs_label = tk.Label(root, text="Enter number of jugs:")
        self.num_jugs_label.pack()
        self.num_jugs_entry = tk.Entry(root)
        self.num_jugs_entry.pack()

        self.capacities_label = tk.Label(root, text="Enter capacities (comma-separated):")
        self.capacities_label.pack()
        self.capacities_entry = tk.Entry(root)
        self.capacities_entry.pack()

        self.target_label = tk.Label(root, text="Enter target amount:")
        self.target_label.pack()
        self.target_entry = tk.Entry(root)
        self.target_entry.pack()

        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack()

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

    def start(self):
        num_jugs = int(self.num_jugs_entry.get())
        capacities = list(map(int, self.capacities_entry.get().split(',')))
        self.target_amount = int(self.target_entry.get())
        
        self.jugs = [Jug(capacities[i]) for i in range(num_jugs)]
        self.display_jugs()

    def display_jugs(self):
        self.canvas.delete("all")
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        
        jug_width = 60
        jug_height = 200

        for i, jug in enumerate(self.jugs):
            x0 = 100 + i * (jug_width + 50)
            y0 = 50
            x1 = x0 + jug_width
            y1 = y0 + jug_height
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=2)
            fill_height = jug_height * jug.amount // jug.capacity
            self.canvas.create_rectangle(x0, y1 - fill_height, x1, y1, fill="blue")
            self.canvas.create_text((x0 + x1) / 2, y1 + 20, text=f"Jug {i + 1}: {jug.amount}/{jug.capacity}")

            fill_button = tk.Button(self.buttons_frame, text=f"Fill Jug {i + 1}", command=lambda i=i: self.fill_jug(i))
            fill_button.grid(row=i, column=0)

            empty_button = tk.Button(self.buttons_frame, text=f"Empty Jug {i + 1}", command=lambda i=i: self.empty_jug(i))
            empty_button.grid(row=i, column=1)

        row_offset = len(self.jugs)

        for i in range(len(self.jugs)):
            for j in range(len(self.jugs)):
                if i != j:
                    pour_button = tk.Button(self.buttons_frame, text=f"Pour Jug {i + 1} to Jug {j + 1}", command=lambda i=i, j=j: self.pour_jug(i, j))
                    pour_button.grid(row=row_offset + i, column=j)

        restart_button = tk.Button(self.buttons_frame, text="Restart", command=self.restart)
        restart_button.grid(row=row_offset + len(self.jugs), column=0, columnspan=2)

    def fill_jug(self, i):
        self.jugs[i].fill()
        self.display_jugs()
        self.check_target()

    def empty_jug(self, i):
        self.jugs[i].empty()
        self.display_jugs()
        self.check_target()

    def pour_jug(self, i, j):
        self.jugs[i].pour_into(self.jugs[j])
        self.display_jugs()
        self.check_target()

    def restart(self):
        self.start()

    def check_target(self):
        if any(jug.amount == self.target_amount for jug in self.jugs):
            final_amounts = ", ".join([str(jug) for jug in self.jugs])
            self.root.after(100, lambda: messagebox.showinfo("Success", f"Target amount reached! Current water amounts: {final_amounts}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugApp(root)
    root.mainloop()
