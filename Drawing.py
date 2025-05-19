import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import ImageGrab

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App by Nakul")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.brush_color = "black"
        self.brush_size = 5
        self.eraser_on = False
        self.background_color = "white"

        self.canvas = tk.Canvas(self.root, bg=self.background_color, width=800, height=500)
        self.canvas.pack(pady=20)

        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.last_x, self.last_y = None, None

        self.create_widgets()

    def create_widgets(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        color_btn = tk.Button(control_frame, text="Select Color", command=self.choose_color)
        color_btn.grid(row=0, column=0, padx=5)

        eraser_btn = tk.Button(control_frame, text="Eraser", command=self.use_eraser)
        eraser_btn.grid(row=0, column=1, padx=5)

        brush_btn = tk.Button(control_frame, text="Brush", command=self.use_brush)
        brush_btn.grid(row=0, column=2, padx=5)

        clear_btn = tk.Button(control_frame, text="Clear", command=self.clear_canvas)
        clear_btn.grid(row=0, column=3, padx=5)

        save_btn = tk.Button(control_frame, text="Save", command=self.save_drawing)
        save_btn.grid(row=0, column=4, padx=5)

        size_label = tk.Label(control_frame, text="Brush Size:")
        size_label.grid(row=0, column=5, padx=5)

        self.size_scale = tk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, command=self.change_size)
        self.size_scale.set(self.brush_size)
        self.size_scale.grid(row=0, column=6, padx=5)

    def choose_color(self):
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color
            self.eraser_on = False

    def use_eraser(self):
        self.eraser_on = True

    def use_brush(self):
        self.eraser_on = False

    def change_size(self, new_size):
        self.brush_size = int(new_size)

    def paint(self, event):
        if self.last_x and self.last_y:
            color = self.background_color if self.eraser_on else self.brush_color
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=color,
                                    capstyle=tk.ROUND, smooth=True)
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_drawing(self):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filepath:
            ImageGrab.grab().crop((x, y, x1, y1)).save(filepath)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
