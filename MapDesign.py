import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Button

def draw_points(point_list):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink']  # Define colors for each set

    def plot_points():
        ax.clear()  # Clear the previous plot
        for i, coordinatesList in enumerate(point_list):
            x_coords = []
            y_coords = []

            for coordinates in coordinatesList:
                x_coords.append(coordinates[0])
                y_coords.append(coordinates[1])

            ax.scatter(x_coords, y_coords, color=colors[i % len(colors)])  # Plot points for each set
            ax.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]], color=colors[i % len(colors)])

        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_title('Plot of Points')
        canvas.draw()  # Redraw the figure

    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Interactive Plot")

    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Initial plot
    plot_points()

    # Run the Tkinter main loop
    root.mainloop()

