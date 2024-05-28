import tkinter as tk
import random
import sqlite3

class LanguageLearningApp:
    def __init__(self, master):
        self.master = master
        master.title("Language Learning App")
        master.geometry("400x300")

        self.vocabulary = self.load_vocabulary()

        self.prompt_text = tk.StringVar()
        self.user_input = tk.StringVar()
        self.feedback_text = tk.StringVar()

        self.create_widgets()
        self.next_word()  # Load the first word when the app starts

    def load_vocabulary(self):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT Adjectivos_ESP, Adjectives_ENG FROM Adjectives')
            data = cursor.fetchall()
            conn.close()
            # Convert the fetched data into a dictionary
            vocabulary = {esp: eng for esp, eng in data}
            return vocabulary
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return {}

    def create_widgets(self):
        prompt_label = tk.Label(self.master, textvariable=self.prompt_text)
        prompt_label.pack()

        feedback = tk.Label(self.master, textvariable=self.feedback_text)
        feedback.pack()

        input_entry = tk.Entry(self.master, textvariable=self.user_input)
        input_entry.pack()

        submit_button = tk.Button(self.master, text="Submit", command=self.submit_guess)
        submit_button.pack()

        next_button = tk.Button(self.master, text="Next", command=self.next_word)
        next_button.pack()

        restart_button = tk.Button(self.master, text="Restart", command=self.restart)
        restart_button.pack()

    def next_word(self):
        if self.vocabulary:
            current_word = random.choice(list(self.vocabulary.keys()))
            self.prompt_text.set(current_word)
            self.user_input.set("")  # Clear the user input field
            self.feedback_text.set("")  # Clear any previous feedback
            self.master.unbind('<Return>')  # Unbind any previous bindings of the 'Return' key
            self.master.bind('<Return>', self.submit_guess)  # Bind the 'submit_guess' method to the 'Return' key press event
        else:
            self.prompt_text.set("No words available")

    def submit_guess(self, event=None):
        guess = self.user_input.get().strip()
        current_word = self.prompt_text.get()
        
        if current_word in self.vocabulary:
            correct_translation = self.vocabulary[current_word]
            
            if guess.lower() == correct_translation.lower():
                self.feedback_text.set("Correct!")
            else:
                self.feedback_text.set(f"Incorrect. The correct translation is: {correct_translation}")
        else:
            self.feedback_text.set("No word available for translation")

    def restart(self):
        self.prompt_text.set("")  # Resetting prompt text
        self.user_input.set("")  # Resetting user input
        self.feedback_text.set("")  # Resetting feedback text
        self.vocabulary = self.load_vocabulary()  # Reload vocabulary from database
        self.next_word()  # Load the first word

def main():
    root = tk.Tk()
    app = LanguageLearningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
