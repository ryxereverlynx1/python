import tkinter as tk
from tkinter import messagebox

quiz_data = [
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "New Delhi", "Bengaluru", "Chennai"],
        "answer": "New Delhi"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "options": ["William Shakespeare", "Charles Dickens", "Jane Austen", "Mark Twain"],
        "answer": "William Shakespeare"
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["Elephant", "Blue Whale", "Giraffe", "Great White Shark"],
        "answer": "Blue Whale"
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["Gold", "Oxygen", "Silver", "Iron"],
        "answer": "Oxygen"
    },
    {
        "question": "Who is prime minister of India",
        "options": ["Elon Musk", "Narendra Modi", "Mukesh Abani", "Donald Trump"],
        "answer": "Narendra Modi"
    }
]

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Game by Nakul")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f1")

        self.score = 0
        self.question_index = 0

        self.question_label = tk.Label(master, text="", font=("Arial", 16), wraplength=500, bg="#f0f0f0")
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()

        self.options = []
        for i in range(4):
            rb = tk.Radiobutton(master, text="", variable=self.var, value="", font=("Arial", 14), bg="#f0f0f0", anchor="w", justify="left")
            rb.pack(fill="x", padx=50, pady=5)
            self.options.append(rb)

        self.submit_button = tk.Button(master, text="Submit", command=self.check_answer, font=("Arial", 14), bg="#4CAF50", fg="white")
        self.submit_button.pack(pady=20)

        self.load_question()

    def load_question(self):
        if self.question_index < len(quiz_data):
            q = quiz_data[self.question_index]
            self.question_label.config(text=f"Q{self.question_index + 1}: {q['question']}")
            self.var.set(None)
            for i, option in enumerate(q['options']):
                self.options[i].config(text=option, value=option)
        else:
            self.show_result()

    def check_answer(self):
        selected = self.var.get()
        if selected == "":
            messagebox.showwarning("No selection", "Please select an option.")
            return
        correct_answer = quiz_data[self.question_index]['answer']
        if selected == correct_answer:
            self.score += 1
        self.question_index += 1
        self.load_question()

    def show_result(self):
        messagebox.showinfo("Quiz Completed", f"Your score: {self.score} out of {len(quiz_data)}")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
