import tkinter as tk
import re
from tkinter import messagebox

global regex_entry, string_entry, result_label


def check_pumping_lemma():
    global regex_entry, string_entry, result_label
    # Get the regular expression and string input by the user
    regex_str = regex_entry.get().strip()
    string = string_entry.get().strip()

    # Check if the input fields are empty
    if not regex_str or not string:
        messagebox.showerror("Error", "Please enter a regular expression and a string")
        return

    # Compile the regular expression
    try:
        regex = re.compile(regex_str)
    except re.error:
        messagebox.showerror("Error", "Invalid regular expression")
        return

    # Implement the pumping lemma
    p = len(regex_str) + 1
    for i in range(p):
        # Split the string into three parts
        prefix = string[:i]
        suffix = string[i:]
        middle = suffix[:p - i - 1]
        remainder = suffix[p - i - 1:]

        # Check if the middle part can be repeated any number of times
        if regex.match(prefix + middle * 2 + remainder):
            messagebox.showinfo("Result", "The string is in the language")
            return

    messagebox.showinfo("Result", "The string is not in the language")


def clear_result():
    global regex_entry, string_entry, result_label
    regex_entry.delete(0, 'end')
    string_entry.delete(0, 'end')


def run():
    # Create the GUI
    global regex_entry, string_entry, result_label
    root = tk.Tk()
    root.title("Pumping Lemma Checker")
    root.geometry("800x500")

    # Background color
    root.configure(bg='#e6f2ff')

    # Regular expression input
    regex_frame = tk.Frame(root, bg="#E0E0E0")
    regex_frame.pack(pady=10)

    regex_label = tk.Label(regex_frame, text="Regular Expression:", bg="blue", fg="white", width=25)
    regex_label.pack(side=tk.LEFT)

    regex_entry = tk.Entry(regex_frame, width=50)
    regex_entry.pack(side=tk.LEFT)

    # String input
    string_frame = tk.Frame(root, bg="#E0E0E0")
    string_frame.pack(pady=10)

    string_label = tk.Label(string_frame, text="String:", bg="blue", fg="white", width=25)
    string_label.pack(side=tk.LEFT)

    string_entry = tk.Entry(string_frame, width=50)
    string_entry.pack(side=tk.LEFT)

    # Check button
    check_button = tk.Button(root, text="Check", command=check_pumping_lemma, bg="#4CAF50", fg="white", width=15)
    check_button.pack(pady=10)

    # Clear button
    clear_button = tk.Button(root, text="Clear", command=clear_result, bg="#f44336", fg="white", width=15)
    clear_button.pack(pady=10)

    # Result label
    # result_label = tk.Label(root, text="", bg="blue", fg="white", font=("Helvetica", 16), width=50, )
    # result_label.pack(pady=10)

    root.mainloop()