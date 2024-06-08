import matplotlib.pyplot as plt
import numpy as np


def draw_points(PointArray, category_names, title):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink', 'violet']  # Define colors for each set

    for i, points_category in enumerate(PointArray):
        color = colors[i % len(colors)]
        for points in points_category:
            points = np.array(points)
            plt.plot(points[:, 0], points[:, 1], marker='.', color='black')
            plt.plot(np.append(points[:, 0], points[0, 0]), np.append(points[:, 1], points[0, 1]), color=color, linewidth = '3.5')
            plt.fill(np.append(points[:, 0], points[0, 0]), np.append(points[:, 1], points[0, 1]), color=color, alpha=0.5)


    plt.title(title)

    legend_handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], linewidth=4.5, label=category_names[i]) for i in range(len(PointArray))]
    plt.legend(handles=legend_handles, loc='best')

    plt.show()
    plt.clf()


