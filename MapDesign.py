import os
import shutil
import tkinter as tk
from tkinter import ttk
from RoomManager import RoomManager
from XMLDataExtract import Original_Building_Path, Edited_Building_Path, count_level_subfolders, \
    parse_xml_for_roomnumber_and_floor, parse_xml_for_coordinates, turtleConverter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DialogueBox import CustomDialog
import xml.etree.ElementTree as ET

BuildingMap = {}
BuildingName = Original_Building_Path.split('/')[-1]
updatedRowsArray = []

RoomsDataArray = []

def create_edited_building_subfolders(directory_path="Athabasca2DMapping/Buildings Data"):
    subfolders = [
        "Augustana Campus",
        "Calgary Centre",
        "Campus Saint-Jean",
        "Enterprise Square",
        "North Campus",
        "South Campus"
    ]

    edited_building_path = os.path.join(directory_path, "Edited Building")
    if not os.path.exists(edited_building_path):
        os.makedirs(edited_building_path)

    for subfolder in subfolders:
        subfolder_path = os.path.join(edited_building_path, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)


def show_legend_window(colors, category_names, floor):
    # Create the legend window
    legend_window = tk.Toplevel()
    legend_window.title(f"Legend - Floor {floor}")

    # Dynamically calculate the window height based on the number of categories
    window_height = min(50 + len(category_names) * 30, 600)  # Max height is 600px
    legend_window.geometry(f"300x{window_height}")

    # Create a frame to hold the canvas and scrollbar
    content_frame = ttk.Frame(legend_window)
    content_frame.pack(fill="both", expand=True)

    # Create a canvas widget
    canvas = tk.Canvas(content_frame)
    canvas.pack(side="left", fill="both", expand=True)

    # Create a vertical scrollbar linked to the canvas
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the Matplotlib figure
    figure_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=figure_frame, anchor="nw")

    # Create the Matplotlib figure and legend
    fig, ax = plt.subplots(figsize=(3, len(category_names) * 0.3))  # Adjusted height per category
    ax.axis('off')  # Hide the axes

    # Create legend handles for the categories
    legend_handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], linewidth=4.5, label=category_names[i])
                      for i in range(len(category_names))]

    # Add legend to the axis
    ax.legend(handles=legend_handles, loc='center', frameon=False)

    # Adjust layout to minimize extra space
    fig.tight_layout(pad=0)

    # Embed the Matplotlib figure inside the frame
    canvas_figure = FigureCanvasTkAgg(fig, master=figure_frame)
    canvas_figure.draw()
    canvas_figure.get_tk_widget().pack()

    # Update the scroll region to include the entire figure
    figure_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

    return legend_window


def draw_points(PointArray, category_names, title, onclick_callback, selected_polygons, floor):
    global RoomsDataArray
    colors = ['red', 'blue', 'green', 'orange', 'maroon', 'grey', 'yellow', 'pink', 'violet']

    fig, ax = plt.subplots(figsize=(10, 8))

    polygons = []
    room_colors = []

    for i, points_category in enumerate(PointArray):
        for j in points_category:
            RoomsDataArray.append(j)
        color = colors[i % len(colors)]
        category_polygons = []

        for points in points_category:
            room_number = points[0][0]
            room_file_path = points[0][1]

            if room_number is not None:
                if room_number in BuildingMap:
                    if BuildingMap[room_number] is None:
                        BuildingMap[room_number] = []
                    BuildingMap[room_number].append(room_file_path)
                else:
                    BuildingMap[room_number] = [room_file_path]

            points = np.array(points[1:])
            polygon = plt.Polygon(points, closed=True, fill=True, edgecolor=color, facecolor=color, alpha=0.5,
                                  linewidth=3.5)
            category_polygons.append((polygon, room_number))
            ax.add_patch(polygon)
            plt.plot(points[:, 0], points[:, 1], marker='.', color='black')

            room_colors.append((room_number, color))

        polygons.append(category_polygons)

    create_edited_building_subfolders(directory_path="Buildings Data")

    for selected_polygon in selected_polygons:
        selected_polygon.set_edgecolor('gray')
        selected_polygon.set_facecolor('gray')

    plt.title(title)

    fig.canvas.mpl_connect('button_press_event', lambda event: onclick_callback(event, polygons, category_names))
    return fig, room_colors, colors


def get_initials(text):
    try:
        int(text)
        return text
    except ValueError:
        words = text.split()
        initials = []

        for word in words:
            if word.isdigit():
                initials.append(word)
            else:
                initials.append(word[0].upper())

        return ''.join(initials)

class Application(tk.Tk):
    def __init__(self, building, campus, *args, **kwargs):

        self.adding_door = None
        self.canvas = None
        self.adding_door = False
        self.building = building
        self.campus = campus
        self.originalXMLfolderPath = f"Buildings Data/Buildings/{self.campus}/{self.building}"
        self.editedXMLfolderPath = f"Buildings Data/Edited Building/{self.campus}/{self.building}"
        self.selected_polygons = []
        self.original_colors = {}
        self.current_floor = None
        super().__init__(*args, **kwargs)
        self.legend_window = None  # To track the legend window instance
        self.title("UofA Building 2D UI")
        self.geometry("1200x900")
        self.resizable(True, True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.container = ttk.Frame(self)
        self.container.grid(padx=10, pady=10, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=0)
        self.container.grid_rowconfigure(1, weight=0)
        self.container.grid_rowconfigure(2, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=0)
        self.welcome_label = tk.Label(self.container, text="Welcome to UofA " + building + " Architecture UI",
                                      font=("Helvetica", 24, "bold"), anchor="center")
        self.welcome_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")
        button_frame = ttk.Frame(self.container)
        button_frame.grid(row=1, column=0, pady=20, sticky="nsew")
        floors = count_level_subfolders(Original_Building_Path, campus, building, "interior")

        if not floors:
            self.no_data_label = tk.Label(self.container, text="No data found", font=("Helvetica", 18, "italic"),
                                          fg="red")
            self.no_data_label.grid(row=1, column=0, pady=20, sticky="nsew")
            button_frame.grid_remove()
        else:
            self.no_data_label = None
            for floor in floors:
                button = ttk.Button(button_frame, text=f"Floor {floor}",
                                    command=lambda f=floor: self.plot_floor_map(f, building, campus))
                button.pack(side=tk.LEFT, padx=(10, 5))

        style = ttk.Style()
        style.configure('TButton', font=("Helvetica", 12, "bold"), background='#4CAF50', foreground='white')

        self.canvas_frame = ttk.Frame(self.container)
        self.canvas_frame.grid(row=4, column=0, sticky="nsew")

        self.check_errors_button = ttk.Button(self.container, text="Check Room Name", command=self.correct_room_name, style='TButton')
        self.check_errors_button.grid(row=1, column=1, pady=(0, 0), padx=(10, 10), sticky='n')
        self.check_errors_button.grid_remove()

        self.generate_neighbours_button = ttk.Button(self.container, text="Generate Neighbours Data", command=self.calling_generating_neigbours_func, style='TButton')
        self.generate_neighbours_button.grid(row=3, column=1, pady=(0, 0), padx=(10, 10), sticky='n')
        self.generate_neighbours_button.grid_remove()

        self.add_door_button = ttk.Button(self.container, text="Add door", command=self.add_door_func, style='TButton')
        self.add_door_button.grid(row=4, column=1, pady=(0, 0), padx=(10, 10), sticky='n')
        self.add_door_button.grid_remove()

        self.selected_rooms = []

    def plot_floor_map(self, floor, building, campus):
        self.current_floor = floor
        self.check_errors_button.grid()
        self.generate_neighbours_button.grid()
        self.add_door_button.grid()

        # Close the previous legend window if it exists
        if self.legend_window is not None and self.legend_window.winfo_exists():
            self.legend_window.destroy()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        points_categories, category_names, title = self.get_floor_data(floor, building, campus)
        fig, room_colors, colors = draw_points(points_categories, category_names, title, self.onCanvasClick,
                                               self.selected_polygons, floor)

        self.polygons = []
        for category_polygons in points_categories:
            for points in category_polygons:
                room_number = points[0][0]
                polygon_points = np.array(points[1:])
                polygon = plt.Polygon(polygon_points, closed=True, fill=True, edgecolor='black', facecolor='red',
                                      alpha=0.5)
                self.polygons.append((polygon, room_number))

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)

        for points_category in points_categories:
            for points in points_category:
                room_number = points[0][0]
                room_points = np.array(points[1:])
                centroid = np.mean(room_points, axis=0)
                room_label = get_initials(room_number)

                label_color = next((color for rn, color in room_colors if rn == room_number), 'black')

                plt.text(centroid[0], centroid[1], room_label, fontsize=10, ha='center', va='center',
                         color='black', fontweight='bold',
                         bbox=dict(facecolor=label_color, alpha=0.7, edgecolor=label_color, boxstyle='round,pad=0.3'))

        # Show legend in a new window with the floor number in the title
        self.legend_window = show_legend_window(colors, category_names, floor)

    def get_floor_data(self, floor, building, campus):
        import XMLDataExtract

        def fetchCoordinateMap(floorNumber):
            return XMLDataExtract.main(floorNumber, building, campus)

        def categorizesCoordinateMap(floorNumber):
            CoordinateMap = fetchCoordinateMap(floorNumber)
            return [CoordinateMap[key] for key in CoordinateMap], [str(key) for key in CoordinateMap]

        points_categories, category_names = categorizesCoordinateMap(floor)
        title = f'Architectural Map of Floor {floor}'

        return points_categories, category_names, title

    def onCanvasClick(self, event, polygons, category_names):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            print(f"Coordinates: ({x}, {y})")

            for category_index, category_polygons in enumerate(polygons):
                for polygon, room_number in category_polygons:
                    if polygon.get_path().contains_point((x, y)):
                        if room_number != "Building Outline":
                            print(f"Room clicked: {room_number}" + "\n")
                            if polygon not in self.selected_polygons:
                                self.selected_polygons.append(polygon)
                            self.canvas.draw()
                            return

        print("Event not in axes or no polygon contains the point" + "\n")

    def correct_room_name(self):
        self.update_xml_with_new_name()

    def find_xml_file_path(self, root_folder, file_name='xml', roomname='X'):
        room_path = os.path.join(root_folder, 'Interior', f'{self.current_floor}', roomname)
        room_path = room_path.replace('/', '\\')

        if not os.path.isdir(room_path):
            print('XML Directory does not exist:', room_path)
            return None

        filePathArray = []
        for root, dirs, files in os.walk(room_path):
            if file_name in files:
                if file_name == 'xml':
                    file_path = os.path.join(root, file_name).replace('\\', '/')
                    filePathArray.append(file_path)

        return filePathArray

    def update_xml_with_new_name(self):
        if self.current_floor is None:
            raise ValueError("Current floor is not set.")
        XML_Filename = "xml"
        room_name = 'X'
        original_xml_path_array = self.find_xml_file_path(self.originalXMLfolderPath, XML_Filename, room_name)

        for i in original_xml_path_array:
            print('Original File Path: ', i)
            if i is None:
                raise FileNotFoundError(
                    f"Original XML file '{XML_Filename}' not found in '{self.originalXMLfolderPath}'.")

            x_position = i.find('X/') + len('X/')
            xml_file_path = i[x_position:]

            temp = i[x_position:]

            edited_folder_path = os.path.join(self.editedXMLfolderPath, 'Interior', self.current_floor, room_name,
                                              xml_file_path)
            edited_xml_path = os.path.join(edited_folder_path, XML_Filename)

            os.makedirs(edited_folder_path, exist_ok=True)

            if not os.path.isfile(i):
                raise FileNotFoundError(f"The path '{i}' is not a file.")

            shutil.copy2(i, edited_xml_path)
            print(f'Copied the XML file:  {edited_xml_path}')

            root = tk.Tk()
            root.withdraw()

            dialog = CustomDialog(root, temp, dialog_title='Changing Room Name')
            new_name = dialog.result

            try:
                tree = ET.parse(edited_xml_path)
                root = tree.getroot()

                if root.tag == 'item':
                    root.set('name', new_name)
                    root.set('key', new_name)

                    tree.write(edited_xml_path, encoding='utf-8', xml_declaration=True)
                    print(f"Name Change: The item name & key have been updated in room {room_name} to {new_name}.\n")
                else:
                    print("The root element is not <item>.")

                self.update_records(self.building, self.campus, self.current_floor, new_name, edited_xml_path)

            except ET.ParseError as e:
                print(f"Failed to parse XML file: {e}")
        self.Update_TurtleOuput_for_name_change('OutputFiles/TurtleOutput.txt', self.building, self.campus, self.current_floor, 'X')

    def update_records(self, building, campus, floor, room, file):

        global updatedRowsArray
        RoomNumber, Level = parse_xml_for_roomnumber_and_floor(file)
        coordinateList = parse_xml_for_coordinates(file)
        turtleData = turtleConverter(building, campus, floor, room, coordinateList) + '\n'
        updatedRowsArray.append(turtleData)


    def Update_TurtleOuput_for_name_change(self, file_path, building, campus, floor, room):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    lines = file.readlines()
            else:
                lines = []
            filtered_lines = []
            for line in lines:
                if not (f"Building: {building}, Campus: {campus}, Floor: {floor}, Room: {room}" in line):
                    filtered_lines.append(line)

            filtered_lines += updatedRowsArray

            with open(file_path, 'w') as file:
                file.writelines(filtered_lines)

            print(f"Name-change records updated in Turtle File\n")

        except IOError as e:
            print(f"An error occurred while accessing the file: {e}")

    def Update_TurtleOutput_for_door_addition(self, building, room1, room2, door_start, door_end):
        file_path = 'OutputFiles/TurtleOutput.txt'
        updated_lines = []
        door_info = f"{room1}: {door_start}, {room2}: {door_end}"

        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if building in line and f'Room: {room1}' in line:
                    # Update the matching record
                    # Assuming the format is such that door info is appended at the end of the line
                    if "door_info:" in line:
                        # If door_info already exists, append to it
                        line = line.strip() + " | " + door_info + "\n"
                    else:
                        # If door_info does not exist, add it
                        line = line.strip() + " door_info: " + door_info + "\n"

                updated_lines.append(line)
            # Write the updated lines to the file
            file.writelines(updated_lines)

    def calling_generating_neigbours_func(self):
        global RoomsDataArray

        room_manager = RoomManager(RoomsDataArray, self.campus, self.building, self.current_floor)
        room_manager.generating_neighbours()

    def add_door_func(self):
        print('Note: Please dont select rooms with same name for door addition like Stairs, X etc. Otherwise Turtle function would add door info to all records with same room name. To fix this please edit XML file item -> key with the new name before executing name change')
        self.adding_door = True
        self.selected_rooms = []

        tk.messagebox.showinfo("Add door", "Please select two rooms to add a door between them.")
        self.canvas.mpl_connect('button_press_event', self.on_select_room_for_door)


    def on_select_room_for_door(self, event):
        if not self.adding_door or not hasattr(self, 'polygons'):
            return

        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            for polygon, room_number in self.polygons:
                if polygon.get_path().contains_point((x, y)) and room_number != "Building Outline":
                    room_info = (polygon, room_number)

                    # Check if the room_info is not already in selected_rooms
                    if room_info not in self.selected_rooms:
                        self.selected_rooms.append(room_info)

                    if len(self.selected_rooms) == 2:
                        self.adding_door = False
                        if self.selected_rooms[0][1] != self.selected_rooms[1][1]:
                            self.show_2d_diagram_of_selected_rooms()
                        else:
                            print('Can not add a door to same rooms')
                    return

    def show_2d_diagram_of_selected_rooms(self):
        if len(self.selected_rooms) != 2:
            print("Please select exactly two rooms.")
            return

        self.room_names_for_door = self.selected_rooms

        # Extract room names and polygons
        (polygon1, room1), (polygon2, room2) = self.selected_rooms

        # Create a new window to show the 2D diagram
        diagram_window = tk.Toplevel(self)
        diagram_window.title(f"Add door to Rooms {room1} & {room2}")
        diagram_window.geometry("800x600")

        # Create a frame to hold the buttons
        button_frame = ttk.Frame(diagram_window)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Create buttons for zooming in and zooming out
        zoom_in_button = ttk.Button(button_frame, text="Zoom In", command=lambda: self.zoom_in(ax, fig))
        zoom_in_button.pack(side=tk.LEFT, padx=5)

        zoom_out_button = ttk.Button(button_frame, text="Zoom Out", command=lambda: self.zoom_out(ax, fig))
        zoom_out_button.pack(side=tk.LEFT, padx=5)

        # Create a Matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot the polygons of the selected rooms
        for polygon, room_number in self.selected_rooms:
            polygon_patch = plt.Polygon(polygon.get_path().vertices, closed=True, edgecolor='black',
                                        facecolor='gray', alpha=0.5)
            ax.add_patch(polygon_patch)
            plt.plot(polygon.get_path().vertices[:, 0], polygon.get_path().vertices[:, 1], marker='.',
                     color='black')

        ax.set_title(f"2D Diagram of Rooms: {room1} & {room2}")
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_aspect('equal')
        plt.grid(True)
        plt.tight_layout()

        # Create a canvas to display the Matplotlib figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=diagram_window)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill="both")

        # Connect click event to add door coordinates
        canvas.mpl_connect('button_press_event',
                           lambda event: self.on_select_door_coordinates(event, ax, fig, diagram_window))

    def zoom_out(self, ax, fig):
        # Get current limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Define the zoom factor
        zoom_factor = 1.2

        # Calculate new limits
        x_center = (xlim[1] + xlim[0]) / 2
        y_center = (ylim[1] + ylim[0]) / 2
        x_range = (xlim[1] - xlim[0]) * zoom_factor
        y_range = (ylim[1] - ylim[0]) * zoom_factor

        ax.set_xlim([x_center - x_range / 2, x_center + x_range / 2])
        ax.set_ylim([y_center - y_range / 2, y_center + y_range / 2])

        # Redraw the canvas
        fig.canvas.draw()

    def zoom_in(self, ax, fig):
        # Get current limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Define the zoom factor
        zoom_factor = 1.2

        # Calculate new limits
        x_center = (xlim[1] + xlim[0]) / 2
        y_center = (ylim[1] + ylim[0]) / 2
        x_range = (xlim[1] - xlim[0]) / zoom_factor
        y_range = (ylim[1] - ylim[0]) / zoom_factor

        ax.set_xlim([x_center - x_range / 2, x_center + x_range / 2])
        ax.set_ylim([y_center - y_range / 2, y_center + y_range / 2])

        # Redraw the canvas
        fig.canvas.draw()

    def on_select_door_coordinates(self, event, ax, fig, diagram_window):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata

            # Check if we already have the start coordinates for the door
            if hasattr(self, 'door_start'):
                # Plot the line representing the door
                ax.plot([self.door_start[0], x], [self.door_start[1], y], color='red', linewidth=2)
                fig.canvas.draw()

                self.door_end = (x, y)

                room0 = self.get_room_from_coordinates(self.door_start)
                room1 = self.get_room_from_coordinates(self.door_end)

                if (room0 and room1 and
                        room0 != room1 and
                        room0 in self.selected_rooms[0][1] and room1 in self.selected_rooms[1][1]):

                    # Add the door to the original UI
                    ...
                    self.add_door_to_original_ui(self.door_start, self.door_end, [room0, room1])
                else:
                    print("Cannot add a door between the same room or invalid coordinates or rooms not selected.")

                # Reset the door_start attribute for the next door
                delattr(self, 'door_start')
            else:
                # Set the starting point for the door
                self.door_start = (x, y)

    def add_door_to_original_ui(self, start_coords, end_coords, room_names):
        if self.canvas is None:
            return

        fig = self.canvas.figure
        ax = fig.gca()

        room0_name = self.get_room_from_coordinates(start_coords)
        room1_name = self.get_room_from_coordinates(end_coords)

        # Define paths for original and edited buildings
        root_folder_original = f"Buildings Data/Buildings/{self.campus}/{self.building}"
        root_folder_edited = f"Buildings Data/Edited Building/{self.campus}/{self.building}"

        # Find the paths of the XML files for the rooms
        room0_path_original = self.find_xml_file_path(root_folder_original, file_name='xml', roomname=room_names[0])[0]
        room1_path_original = self.find_xml_file_path(root_folder_original, file_name='xml', roomname=room_names[1])[0]

        # Create the edited folder if it doesn't exist
        if not os.path.exists(root_folder_edited):
            os.makedirs(root_folder_edited)

        # Define paths for the copied XML files by replacing the folder
        copied_room0_path = room0_path_original.replace(root_folder_original, root_folder_edited)
        copied_room1_path = room1_path_original.replace(root_folder_original, root_folder_edited)

        # Create any intermediate directories for the copied files if they don't exist
        copied_room0_dir = os.path.dirname(copied_room0_path)
        copied_room1_dir = os.path.dirname(copied_room1_path)

        if not os.path.exists(copied_room0_dir):
            os.makedirs(copied_room0_dir)
        if not os.path.exists(copied_room1_dir):
            os.makedirs(copied_room1_dir)

        try:
            # Copy the XML files to the new folder
            shutil.copy2(room0_path_original, copied_room0_path)
            shutil.copy2(room1_path_original, copied_room1_path)
            print('Copied XML files to Edited Building folder for door addition')
        except Exception as e:
            print(f"Error copying XML files: {e}")

        if (room0_name and room1_name and
                room0_name != room1_name and
                room0_name in [room[1] for room in self.selected_rooms] and
                room1_name in [room[1] for room in self.selected_rooms]):

            ax.plot([start_coords[0], end_coords[0]], [start_coords[1], end_coords[1]], color='red', linewidth=2)
            self.canvas.draw()
            print(f"Plotted a door between rooms {room_names[0]} and {room_names[1]} from {start_coords} to {end_coords}", end='\n')


            try:
                self.add_door_to_text_file(copied_room0_path, room_names, start_coords, end_coords)
                self.Update_TurtleOutput_for_door_addition(self.building, room_names[0], room_names[1], start_coords, end_coords)
                print(f"Added door info in Turtle & Txt file for room: {room_names[0]}", end='\n\n')

            except Exception as e:
                print(f'Error adding door info: {room_names[0]} {e}')

            try:
                self.add_door_to_text_file(copied_room1_path, room_names, start_coords, end_coords)
                self.Update_TurtleOutput_for_door_addition(self.building, room_names[1], room_names[0], start_coords, end_coords)
                print(f"Added door info in Turtle & Txt file for room: {room_names[0]}", end='\n\n')

            except Exception as e:
                print(f'Error adding door info: {room_names[0]} {e}')

        else:
            print(f"Cannot add a door between the same room or invalid coordinates or rooms not selected.")

    def get_room_from_coordinates(self, coords):
        for polygon, room_number in self.polygons:
            if room_number != "Building Outline" and polygon.get_path().contains_point(coords):
                return room_number
        return None

    def add_door_to_text_file(self, file_path, room_names, start_coords, end_coords):

        new_entry = f"{room_names[0]}: {start_coords}, {room_names[1]}: {end_coords}"
        file_path = file_path.replace('xml', 'door_info.text')
        print(f'Generated a text file with door info in {file_path}')

        try:
            with open(file_path, 'a') as file:
                file.write(new_entry + '\n')
        except Exception as e:
            print(f"An error occurred: {e}")















