import numpy as np
import tkinter as tk

from pathsolver import PathSolver

window_h = 900
window_w = 1600
margin = 0.01
radius = 3
default_iterations = 100


def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb


def _try_set_int(val, var):
    try:
        var = int(val)
    except ValueError:
        pass


def _try_set_float(val, var):
    try:
        var = float(val)
    except ValueError:
        pass


class Controller:
    def __init__(self, window, canvas):
        self.running = False
        self.n = 30
        self.num_ants = 30
        self.dist_pow = 10
        self.pher_pow = 1
        self.pher_intensity = 10
        self.dissipation = 0.2
        self.solver = None
        self.canvas = canvas
        self.points = None
        self.window = window

        self.points_entry = None
        self._build_gui()
        self._gen_points()
        self._reset_solver()
        self._draw_points() 

        self.show_pher = True
        self.show_best = True

    def _draw_points(self):
        for point in self.points:
            self.canvas.create_oval(point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius,
                                    fill='White')

    def _draw_path(self, indices, color):
        for i in range(len(indices) - 1):
            self.canvas.create_line(self.points[indices[i]][0], self.points[indices[i]][1],
                                    self.points[indices[i + 1]][0], self.points[indices[i + 1]][1], fill=color)
        self.canvas.create_line(self.points[indices[0]][0], self.points[indices[0]][1],
                                self.points[indices[len(indices) - 1]][0], self.points[indices[len(indices) - 1]][1],
                                fill=color)

    def _draw_pheromones(self):
        pheromones = self.solver.get_pheromones()
        max_pheromone = pheromones.max()
        for i in range(len(pheromones)):
            for ii in range(len(pheromones)):
                if pheromones[i][ii] > 0.1:
                    self.canvas.create_line(self.points[i, 0], self.points[i, 1],
                                            self.points[ii, 0], self.points[ii, 1],
                                            fill=_from_rgb((int(256 * pheromones[i, ii] / max_pheromone),) * 3))

    def _gen_points(self):
        x_coord = np.random.randint(low=margin * window_w, high=(1 - margin) * window_w, size=self.n)
        y_coord = np.random.randint(low=margin * window_h, high=(1 - margin) * window_h, size=self.n)
        self.points = np.stack([x_coord, y_coord], axis=1)

    def _reset_solver(self):
        self.solver = PathSolver(self.points)

    def _update_points(self):
        try:
            n = int(self.points_entry.get())
            self.n = n
            self._gen_points()
            self.canvas.delete('all')
            self._reset_solver()
            self._draw_points()
            self.canvas.pack()
        except ValueError:
            print("Invalid input")

    def _build_gui(self):
        bg = 'Gray20'
        fg = 'White'

        root_frame = tk.Frame(self.window, bg=bg)

        # Row 1
        row_1 = tk.Frame(root_frame, bg=bg)
        points_label = tk.Label(row_1, bg=bg, fg=fg, text='Number of Points:')
        points_label.pack(side='left')
        points_entry_str = tk.StringVar(row_1, value=str(self.n))
        points_entry = tk.Entry(row_1, bg=bg, fg=fg, justify='left', width=5, textvariable=points_entry_str, )
        self.points_entry = points_entry
        points_entry.pack(side='left')
        update = tk.Button(row_1, text='Update', bg=bg, fg=fg, command=self._update_points)
        update.pack(side='left')
        row_1.pack(padx=10, pady=10)

        # Row 2
        row_2 = tk.Frame(root_frame, bg=bg)
        ants_label = tk.Label(row_2, bg=bg, fg=fg, text='Ants:')
        ants_label.pack(side='left')
        ants_sv = tk.StringVar(row_2, value=str(self.num_ants))
        ants_entry = tk.Entry(row_2, bg=bg, fg=fg, justify='left', width=5, textvariable=ants_sv)
        ants_entry.pack(side='left')
        ants_update = tk.Button(row_2, text='Update', bg=bg, fg=fg,
                                command=lambda: _try_set_int(ants_entry.get(), self.num_ants))
        ants_update.pack(side='left')
        row_2.pack(padx=10, pady=10)

        # Row 3
        row_3 = tk.Frame(root_frame, bg=bg)
        dist_pow_label = tk.Label(row_3, bg=bg, fg=fg, text='Distance_Pow:')
        dist_pow_label.pack(side='left')
        dist_pow_sv = tk.StringVar(row_3, value=str(self.dist_pow))
        dist_pow_entry = tk.Entry(row_3, bg=bg, fg=fg, justify='left', width=5, textvariable=dist_pow_sv)
        dist_pow_entry.pack(side='left')
        dist_pow_update = tk.Button(row_3, text='Update', bg=bg, fg=fg,
                                    command=lambda: _try_set_float(dist_pow_entry.get(), self.dist_pow))
        dist_pow_update.pack(side='left')
        row_3.pack(padx=10, pady=10)

        # Row 4
        row_4 = tk.Frame(root_frame, bg=bg)
        pher_pow_label = tk.Label(row_4, bg=bg, fg=fg, text='Pheromone_Pow:')
        pher_pow_label.pack(side='left')
        pher_pow_sv = tk.StringVar(row_4, value=str(self.pher_pow))
        pher_pow_entry = tk.Entry(row_4, bg=bg, fg=fg, justify='left', width=5, textvariable=pher_pow_sv)
        pher_pow_entry.pack(side='left')
        pher_pow_update = tk.Button(row_4, text='Update', bg=bg, fg=fg,
                                    command=lambda: _try_set_float(pher_pow_entry.get(), self.pher_pow))
        pher_pow_update.pack(side='left')
        row_4.pack(padx=10, pady=10)

        # Row 5
        row_5 = tk.Frame(root_frame, bg=bg)
        pher_int_label = tk.Label(row_5, bg=bg, fg=fg, text='Pheromone_Intensity:')
        pher_int_label.pack(side='left')
        pher_int_sv = tk.StringVar(row_5, value=str(self.pher_intensity))
        pher_int_entry = tk.Entry(row_5, bg=bg, fg=fg, justify='left', width=5, textvariable=pher_int_sv)
        pher_int_entry.pack(side='left')
        pher_int_update = tk.Button(row_5, text='Update', bg=bg, fg=fg,
                                    command=lambda: _try_set_float(pher_int_entry.get(), self.pher_intensity))
        pher_int_update.pack(side='left')
        row_5.pack(padx=10, pady=10)

        # Row 6
        row_6 = tk.Frame(root_frame, bg=bg)
        dissipation_label = tk.Label(row_6, bg=bg, fg=fg, text='Dissipation:')
        dissipation_label.pack(side='left')
        dissipation_sv = tk.StringVar(row_6, value=str(self.dissipation))
        dissipation_entry = tk.Entry(row_6, bg=bg, fg=fg, justify='left', width=5, textvariable=dissipation_sv)
        dissipation_entry.pack(side='left')
        dissipation_update = tk.Button(row_6, text='Update', bg=bg, fg=fg,
                                       command=lambda: _try_set_float(dissipation_entry.get(), self.dissipation))
        dissipation_update.pack(side='left')
        row_6.pack(padx=10, pady=10)

        # Row_7
        row_7 = tk.Frame(root_frame, bg=bg)
        iterations_label = tk.Label(row_7, bg=bg, fg=fg, text='Iterations:')
        iterations_label.pack(side='left')
        iterations_sv = tk.StringVar(row_7, value=str(default_iterations))
        iterations_entry = tk.Entry(row_7, bg=bg, fg=fg, justify='left', width=5, textvariable=iterations_sv)
        iterations_entry.pack(side='left')
        iterations_update = tk.Button(row_7, text='Run', bg=bg, fg=fg,
                                      command=lambda: self.run_n_interations(iterations_entry.get()))
        iterations_update.pack(side='left')
        row_7.pack(padx=10, pady=10)

        root_frame.pack()

    def run_n_interations(self, n):
        if type(n) is not int:
            try:
                n = int(n)
            except ValueError:
                return
        for i in range(n):
            self.solver.run_1_iteration(self.num_ants, self.dist_pow, self.pher_pow,
                                        self.pher_intensity, self.dissipation)
            self.canvas.delete('all')
            if self.show_pher:
                self._draw_pheromones()
            if self.show_best:
                self._draw_path(self.solver.best_path, 'green')

            self._draw_points()
            self.canvas.pack()
            self.canvas.update()
