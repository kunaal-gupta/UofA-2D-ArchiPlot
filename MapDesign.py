import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def draw_points(PointArray, category_names, title):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink',
              'violet']  # Define colors for each set

    fig, ax = plt.subplots()

    polygons = []
    for i, points_category in enumerate(PointArray):
        color = colors[i % len(colors)]
        category_polygons = []
        for points in points_category:
            points = np.array(points)
            polygon = plt.Polygon(points, closed=True, fill=True, edgecolor=color, facecolor=color, alpha=0.5,
                                  linewidth=3.5)
            category_polygons.append(polygon)
            ax.add_patch(polygon)
            plt.plot(points[:, 0], points[:, 1], marker='.', color='black')
        polygons.append(category_polygons)

    plt.title(title)
    legend_handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], linewidth=4.5, label=category_names[i]) for i
                      in range(len(PointArray))]
    plt.legend(handles=legend_handles, loc='best')

    def onclick(event):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            for category_index, category_polygons in enumerate(polygons):
                for polygon in category_polygons:
                    if polygon.get_path().contains_point((x, y)):
                        print(f"Clicked within '{category_names[category_index]}' at ({x}, {y})")
                        print("Polygon coordinates:")
                        print(polygon.get_xy())
                        break

    fig.canvas.mpl_connect('button_press_event', onclick)

    return fig


class Application(tk.Tk):
    def __init__(self, PointArray, category_names, title, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Map Design")

        # Create a container
        container = ttk.Frame(self)
        container.grid(padx=10, pady=10, sticky="nsew")

        # Create the figure
        fig = draw_points(PointArray, category_names, title)

        # Embed the figure in Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=container)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Adding a button to quit the application
        quit_button = ttk.Button(container, text="Quit", command=self.quit)
        quit_button.grid(row=1, column=0, pady=10)

    def quit(self):
        self.destroy()

