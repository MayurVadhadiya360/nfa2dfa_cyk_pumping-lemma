from tkinter import *
import nfa2dfa_gui
import cyk
import lemma

gui = Tk()
gui.title("Exploring Formal Language Theory")
gui.geometry("500x500")
btn1 = Button(
    gui,
    text="NFA2DFA",
    command=nfa2dfa_gui.run,
    width=25, bg="blue",
    activebackground='black',
    foreground='white'
)
btn2 = Button(
    gui,
    text="CYK",
    command=cyk.run,
    width=25,
    bg='blue',
    activebackground='black',
    foreground='white'
)
btn1.pack(padx=5, pady=5)

btn2.pack(padx=5, pady=5)

btn3 = Button(
    gui,
    text="Pumping Lemma",
    command=lemma.run,
    width=25,
    bg='blue',
    activebackground='black',
    foreground='white'
)
btn3.pack(padx=5, pady=5)

gui.mainloop()
