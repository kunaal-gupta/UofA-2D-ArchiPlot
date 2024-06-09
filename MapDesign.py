import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def draw_points(PointArray, category_names, title):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink', 'violet']  # Define colors for each set

    fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the figure size here

    polygons = []
    for i, points_category in enumerate(PointArray):
        color = colors[i % len(colors)]
        category_polygons = []
        for points in points_category:
            points = np.array(points)
            polygon = plt.Polygon(points, closed=True, fill=True, edgecolor=color, facecolor=color, alpha=0.5, linewidth=3.5)
            category_polygons.append(polygon)
            ax.add_patch(polygon)
            plt.plot(points[:, 0], points[:, 1], marker='.', color='black')
        polygons.append(category_polygons)

    plt.title(title)
    legend_handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], linewidth=4.5, label=category_names[i]) for i in range(len(PointArray))]
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Floor Design")
        self.geometry("1200x900")  # Initial window size
        self.resizable(True, True)  # Allow window resizing

        # Configure row and column weights to make the container expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a container
        self.container = ttk.Frame(self)
        self.container.grid(padx=10, pady=10, sticky="nsew")

        # Configure row and column weights of the container to make the canvas expandable
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create button frame
        button_frame = ttk.Frame(self.container)
        button_frame.grid(row=0, column=0, pady=10)

        # Add buttons for each floor
        floors = [1, 2, 3, 4]
        for floor in floors:
            button = ttk.Button(button_frame, text=f"Floor {floor}", command=lambda f=floor: self.plot_floor_map(f))
            button.pack(side=tk.LEFT, padx=5)

        # Create the canvas holder frame
        self.canvas_frame = ttk.Frame(self.container)
        self.canvas_frame.grid(row=1, column=0, sticky="nsew")

        # Adding a button to quit the application
        quit_button = ttk.Button(self.container, text="Quit", command=self.quit)
        quit_button.grid(row=2, column=0, pady=10, sticky="ew")

    def plot_floor_map(self, floor):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()  # Remove any previous canvas frame widgets

        # Fetch and categorize coordinate map for the floor
        points_categories, category_names, title = self.get_floor_data(floor)

        # Create the figure
        fig = draw_points(points_categories, category_names, title)

        # Embed the figure in Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

    def get_floor_data(self, floor):
        # Call your function to fetch and categorize coordinates here
        import XMLDataExtract

        def fetchCoordinateMap(floorNumber):
            return XMLDataExtract.main(floorNumber=floorNumber)

        def categorizesCoordinateMap(floorNumber: int):
            CoordinateMap = fetchCoordinateMap(floorNumber)
            RoomPoints = CoordinateMap['Room']
            EntrancePoints = CoordinateMap['Entrance']
            ElevatorPoints = CoordinateMap['Elevator']
            HallwayPoints = CoordinateMap['Hallway']
            WashroomPoints = CoordinateMap['Washroom']
            StairPoints = CoordinateMap['Stairs']
            XPoints = CoordinateMap['X']
            return [RoomPoints, EntrancePoints, ElevatorPoints, HallwayPoints, WashroomPoints, StairPoints, XPoints]

        points_categories = categorizesCoordinateMap(floor)
        category_names = ['RoomPoints', 'EntrancePoints', 'ElevatorPoints', 'HallwayPoints', 'WashroomPoints', 'StairPoints', 'XPoints']
        title = f'Architectural Map of Floor {floor}'

        return points_categories, category_names, title
