import tkinter as tk
import random


vocabulary = {
    "bonita": "nice",
    "chaqueta": "jacket",
}
vocabulary["prima"]="cousin"

root = tk.Tk()

prompt_text = tk.StringVar()

userInput = tk.StringVar()

feedback_text = tk.StringVar()

def next():
    p = prompt_text.get()
    if p != "":
        o = vocabulary[p]
        print(p)
        if o == userInput.get():
            feedback_text.set("Correct")
        else:
            feedback_text.set(f"Incorrect : {o}")
    res = random.choice(list(vocabulary.items()))
    prompt_text.set(res[0])
    root.update_idletasks()

# def restart():
#     p = 


prompt = tk.Label(root,textvariable=prompt_text)
prompt.pack()
feedback = tk.Label(root, textvariable=feedback_text)
feedback.pack()
input = tk.Entry(root,textvariable=userInput)
input.pack()
button = tk.Button(root,text="Next", command=next)
button.pack()
button = tk.Button(root,text="Restart", command=next)
button.pack()
root.mainloop()


