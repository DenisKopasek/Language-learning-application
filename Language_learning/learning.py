import sqlite3
import random
from tkinter import *

class LanguageLearningApp:
    def __init__(self, master):
        self.master = master
        master.title("Language Learning App")
        master.geometry("800x600")

        self.total_attempts_label = Label(master, text="How many words do you want to guess?")
        self.total_attempts_label.pack()

        self.total_attempts_entry = Entry(master)
        self.total_attempts_entry.pack()

        self.start_button = Button(master, text="Start", command=self.start_guessing)
        self.start_button.pack()

        self.previous_guesses_label = Label(master, text="Previous guesses:")
        self.previous_guesses_label.pack()

        self.previous_guesses_text = Text(master, height=10, width=50)
        self.previous_guesses_text.pack(fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(master, command=self.previous_guesses_text.yview)
        self.previous_guesses_text.config(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.statistics_label = Label(master, text="")
        self.statistics_label.pack()

        self.restart_button = Button(master, text="Restart", command=self.restart)
        self.restart_button.pack()

        self.input_field = Entry(master)
        self.input_field.pack()
        self.input_field.focus_set()

        self.word_label = Label(master, text="")
        self.word_label.pack()

        self.word_pairs = []
        self.current_word_index = 0
        self.correct_guesses = 0
        self.total_attempts = 0

        master.bind('<Return>', self.submit_guess)

        # Define tags for text color
        self.previous_guesses_text.tag_configure("correct", foreground="green")
        self.previous_guesses_text.tag_configure("incorrect", foreground="red")

    def get_word_pairs(self):
        conn = sqlite3.connect('vocabulary.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT Adjectivos_ESP, Adjectives_ENG FROM Adjectives ORDER BY RANDOM()''')
        word_pairs = cursor.fetchall()
        conn.close()
        return word_pairs

    def start_guessing(self):
        self.total_attempts = int(self.total_attempts_entry.get())
        print("Total attempts:", self.total_attempts)
        self.word_pairs.clear()
        self.clear_previous_guesses()
        self.correct_guesses = 0

        all_word_pairs = self.get_word_pairs()
        random.shuffle(all_word_pairs)
        self.word_pairs = all_word_pairs[:self.total_attempts]

        print("Word pairs:", self.word_pairs)
        self.show_next_word()

    def show_next_word(self):
        if self.current_word_index < len(self.word_pairs):
            if self.current_word_index % 2 == 0:
                Adjectives_ENG, _ = self.word_pairs[self.current_word_index]
                self.word_label.config(text=f"Translate: {Adjectives_ENG} (eng)")
            else:
                _, Adjectivos_ESP = self.word_pairs[self.current_word_index]
                self.word_label.config(text=f"Translate: {Adjectivos_ESP} (esp)")

            self.current_word_index += 1
            self.start_button.config(state='disabled')
            self.total_attempts_entry.config(state='disabled')
            self.input_field.delete(0, END)
        else:
            self.show_statistics()

    def submit_guess(self, event=None):
        guess = self.input_field.get().strip()
        if self.current_word_index % 2 == 0:
            Adjectives_ENG, _ = self.word_pairs[self.current_word_index - 1]
            result = "Correct!" if guess.lower() == Adjectives_ENG.lower() else "Incorrect. The correct translation is: " + Adjectives_ENG
        else:
            _, Adjectivos_ESP = self.word_pairs[self.current_word_index - 1]
            result = "Correct!" if guess.lower() == Adjectivos_ESP.lower() else "Incorrect. The correct translation is: " + Adjectivos_ESP

        if result == "Correct!":
            self.correct_guesses += 1

        tag = "correct" if result == "Correct!" else "incorrect"
        self.previous_guesses_text.insert(END, f"Translate: {Adjectives_ENG if self.current_word_index % 2 == 0 else Adjectivos_ESP}\nYour guess: {guess}\nResult: {result}\n\n", tag)
        self.previous_guesses_text.see(END)  # Scroll to the end
        self.show_next_word()

    def clear_previous_guesses(self):
        self.previous_guesses_text.delete('1.0', END)

    def show_statistics(self):
        success_rate = (self.correct_guesses / self.total_attempts) * 100 if self.total_attempts > 0 else 0
        self.statistics_label.config(text=f"You guessed {self.correct_guesses}/{self.total_attempts}. Success rate is {success_rate:.2f}%.")

        self.restart_button.pack()

    def restart(self):
        self.current_word_index = 0
        self.start_guessing()

def main():
    root = Tk()
    app = LanguageLearningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()