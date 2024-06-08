import matplotlib.pyplot as plt
import numpy as np


def draw_points(PointArray, category_names):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink', 'violet']  # Define colors for each set

    for i, points_category in enumerate(PointArray):
        color = colors[i % len(colors)]
        for points in points_category:
            points = np.array(points)
            plt.plot(points[:, 0], points[:, 1], marker='.', color='black')
            plt.plot(np.append(points[:, 0], points[0, 0]), np.append(points[:, 1], points[0, 1]), color=color, linewidth = '3.5')
            plt.fill(np.append(points[:, 0], points[0, 0]), np.append(points[:, 1], points[0, 1]), color=color, alpha=0.5)


    plt.title('Map Design with Different Point Categories')

    legend_handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], linewidth=4.5, label=category_names[i]) for i in range(len(PointArray))]
    plt.legend(handles=legend_handles, loc='best')

    plt.show()



# def draw_points(point_list):
#     colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink']  # Define colors for each set
#
#     def plot_points():
#         ax.clear()  # Clear the previous plot
#         for i, coordinatesList in enumerate(point_list):
#             x_coords = []
#             y_coords = []
#
#             for coordinates in coordinatesList:
#
#                     x_coords.append(coordinates[0])
#                     y_coords.append(coordinates[1])
#
#             ax.scatter(x_coords, y_coords, color=colors[0])  # Plot points for each set
#             ax.plot(x_coords + [x_coords[0]], y_coords + [y_coords[0]], color=colors[1])
#
#         ax.set_xlabel('X-axis')
#         ax.set_ylabel('Y-axis')
#         ax.set_title('Plot of Points')
#         canvas.draw()  # Redraw the figure
#
#     # Create a new Tkinter window
#     root = tk.Tk()
#     root.title("Interactive Plot")
#
#     # Create a Matplotlib figure and axis
#     fig, ax = plt.subplots()
#     canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#
#     # Initial plot
#     plot_points()
#
#     # Run the Tkinter main loop
#     root.mainloop()

