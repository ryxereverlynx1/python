import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic Tac Toe by nakul")

# Current player
current_player = "X"

# Create a 3x3 grid of buttons
buttons = [[None for _ in range(3)] for _ in range(3)]

# Function to check for a win or draw
def check_winner():
    # Check rows
    for row in buttons:
        if row[0]["text"] == row[1]["text"] == row[2]["text"] != "":
            return True
    # Check columns
    for col in range(3):
        if buttons[0][col]["text"] == buttons[1][col]["text"] == buttons[2][col]["text"] != "":
            return True
    # Check diagonals
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True
    return False

# Function to check for a draw
def check_draw():
    for row in buttons:
        for button in row:
            if button["text"] == "":
                return False
    return True

# Function to handle button clicks
def on_click(row, col):
    global current_player
    if buttons[row][col]["text"] == "":
        buttons[row][col]["text"] = current_player
        if check_winner():
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            reset_game()
        elif check_draw():
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
        else:
            current_player = "O" if current_player == "X" else "X"

# Function to reset the game
def reset_game():
    global current_player
    current_player = "X"
    for row in buttons:
        for button in row:
            button["text"] = ""

# Create the buttons and place them in the grid
for i in range(3):
    for j in range(3):
        button = tk.Button(root, text="", font=("Arial", 40), width=5, height=2,
                           command=lambda row=i, col=j: on_click(row, col))
        button.grid(row=i, column=j)
        buttons[i][j] = button

root.mainloop()
