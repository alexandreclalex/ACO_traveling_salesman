import tkinter as tk
from tkinter import font
from Controller import Controller
from pathsolver import PathSolver

window_h = 900
window_w = 1600

window = tk.Tk()
window.title('Traveling Salesman')
canvas = tk.Canvas(window, bg='grey20', height=window_h, width=window_w)
canvas.pack()

controls_window = tk.Tk()
controls_window.title('Config')
controls_window.option_add('*Font', 'Monoid')
controller = Controller(controls_window, canvas)
controls_window.lift()
controls_window.mainloop()
