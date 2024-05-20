import tkinter as tk
import random

vocabulary = {                      #Vocabulary list
    "bonita": "nice",
    "chaqueta": "jacket",
}
vocabulary["prima"]="cousin"

root = tk.Tk()                  #Opens window
root.title("My Application")    #Name of the window

prompt_text = tk.StringVar()
userInput = tk.StringVar()
feedback_text = tk.StringVar()

def next():
    p = prompt_text.get()
    if p != "":
        o = vocabulary[p]
        if o == userInput.get():                        #Checking if user input equals translation
            feedback_text.set("Correct")
        else:
            feedback_text.set(f"Incorrect : {o}")
    res = random.choice(list(vocabulary.items()))
    prompt_text.set(res[0])
    root.update_idletasks()


def restart():
    prompt_text.set("")         # Resetting prompt text
    userInput.set("")           # Resetting user input
    feedback_text.set("")       # Resetting feedback text









prompt = tk.Label(root,textvariable=prompt_text)
prompt.pack()
feedback = tk.Label(root, textvariable=feedback_text)
feedback.pack()
input = tk.Entry(root,textvariable=userInput)
input.pack()
button = tk.Button(root,text="Next", command=next)
button.pack()
button = tk.Button(root,text="Restart", command=restart)
button.pack()

root.mainloop()


