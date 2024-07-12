import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import ttk, simpledialog

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

BuildingMap = {}


import os
import shutil

def create_new_xml_folder(building_map, floor):
    # Define the project directory
    project_directory = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
    backup_folder_path = os.path.join(project_directory, "new_xml")

    # Create the backup folder if it doesn't exist
    os.makedirs(backup_folder_path, exist_ok=True)
    print(f"Backup directory ensured: {backup_folder_path}")

    # Define categories
    categories = [
        'Room',
        'Entrance',
        'Elevator',
        'Hallway',
        'Washroom',
        'StairPoints',
        'X'
    ]

    # Create level folder for the specified floor
    level_folder_path = os.path.join(backup_folder_path, f"Level_{floor}")
    os.makedirs(level_folder_path, exist_ok=True)

    # Create subfolders for each category if they don't exist
    for category in categories:
        category_folder_path = os.path.join(level_folder_path, category)
        os.makedirs(category_folder_path, exist_ok=True)

    # Copy each XML file from BuildingMap to the backup folder
    for room_number, xml_paths in building_map.items():
        for xml_path in xml_paths:  # Iterate through the list of XML paths
            print(room_number)
            if os.path.exists(xml_path):
                # Logic to assign the XML file to a specific category
                if 'Entrance' in room_number:
                    category = 'Entrance'
                elif 'Elevator' in room_number:
                    category = 'Elevator'
                elif 'Hallway' in room_number:
                    category = 'Hallway'
                elif 'Washroom' in room_number:
                    category = 'Washroom'
                elif 'Stair' in room_number:
                    category = 'StairPoints'
                elif 'X' in room_number:
                    category = 'X'
                else:
                    category = 'Room'  # Default category

                # Construct the new file path in the appropriate category folder
                base_filename = f"{room_number}.xml"
                backup_file_path = os.path.join(level_folder_path, category, base_filename)

                # Check if file already exists and rename if necessary
                if os.path.exists(backup_file_path):
                    # Generate a new filename with a suffix
                    base, ext = os.path.splitext(base_filename)
                    counter = 2
                    while os.path.exists(backup_file_path):
                        backup_file_path = os.path.join(level_folder_path, category, f"{base}_{counter}{ext}")
                        counter += 1

                shutil.copy(xml_path, backup_file_path)  # Copy the XML file
                print(f"Copied {xml_path} to {backup_file_path}")
            else:
                print(f"XML file for room {room_number} does not exist: {xml_path}")



def draw_points(PointArray, category_names, title, onclick_callback, selected_polygons, floor):
    colors = ['red', 'blue', 'green', 'orange', 'black', 'grey', 'yellow', 'pink', 'violet']  # Define colors for each set

    fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the figure size here

    polygons = []
    for i, points_category in enumerate(PointArray):
        color = colors[i % len(colors)]
        category_polygons = []
        for points in points_category:
            room_number = points[0][0]  # Get the room number
            room_file_path = points[0][1]

            if room_number is not None:
                if room_number in BuildingMap:
                    # Initialize as a list if it's not already
                    if BuildingMap[room_number] is None:
                        BuildingMap[room_number] = []
                    BuildingMap[room_number].append(room_file_path)
                else:
                    BuildingMap[room_number] = [room_file_path]

            points = np.array(points[1:])
            polygon = plt.Polygon(points, closed=True, fill=True, edgecolor=color, facecolor=color, alpha=0.5, linewidth=3.5)
            category_polygons.append((polygon, room_number))
            ax.add_patch(polygon)
            plt.plot(points[:, 0], points[:, 1], marker='.', color='black')
        polygons.append(category_polygons)
    for i in BuildingMap:
        print(i, BuildingMap[i])

    # Pass the floor to create_xml_backup_folder
    create_new_xml_folder(BuildingMap, floor)

    # Highlight selected polygons
    for selected_polygon in selected_polygons:
        selected_polygon.set_edgecolor('gray')
        selected_polygon.set_facecolor('gray')

    plt.title(title)
    legend_handles = [plt.Line2D([0], [0], color=colors[i % len(colors)], linewidth=4.5, label=category_names[i]) for i in range(len(PointArray))]
    plt.legend(handles=legend_handles, loc='best')

    fig.canvas.mpl_connect('button_press_event', lambda event: onclick_callback(event, polygons, category_names))
    return fig


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.selected_polygons = []
        self.original_colors = {}

        super().__init__(*args, **kwargs)
        self.title("Floor Design")
        self.geometry("1200x900")
        self.resizable(True, True)

        # Configure row and column weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a container
        self.container = ttk.Frame(self)
        self.container.grid(padx=10, pady=10, sticky="nsew")

        # Configure row and column weights of the container
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

        # Create CheckRoomNameErrors button, initially hidden
        self.check_errors_button = ttk.Button(self.container, text="Check Room Name Errors", command=self.check_room_name_errors)
        self.check_errors_button.grid(row=0, column=1, pady=10, padx=(0, 10), sticky='ne')
        self.check_errors_button.grid_remove()  # Hide the button initially

        # Placeholder for selected rooms for door addition
        self.selected_rooms = []

    def check_room_name_errors(self):
        # Logic to check room name errors
        print("Checking room name errors...")
        # Implement your error checking logic here

    def plot_floor_map(self, floor):
        # Show the Check Room Name Errors button when a floor is clicked
        self.check_errors_button.grid()  # Make the button visible

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()  # Remove any previous canvas frame widgets

        # Fetch and categorize coordinate map for the floor
        points_categories, category_names, title = self.get_floor_data(floor)

        # Create the figure
        fig = draw_points(points_categories, category_names, title, self.checkFunction, self.selected_polygons, floor)

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

    # Select Functions --------------------------------------------------

    def checkFunction(self, event, polygons, category_names):
        if event.inaxes is not None:
            x, y = event.xdata, event.ydata
            for category_index, category_polygons in enumerate(polygons):
                for polygon, room_number in category_polygons:
                    if polygon.get_path().contains_point((x, y)):
                        print(f"Room clicked: {room_number}")  # Print the room number
                        self.handleCheck(room_number, (x, y))

                        # Highlight the selected polygon if not already selected
                        if polygon not in self.selected_polygons:
                            self.selected_polygons.append(polygon)
                            # Remove the following lines to avoid changing the polygon color
                            # polygon.set_edgecolor('gray')
                            # polygon.set_facecolor('gray')

                        self.canvas.draw()  # Refresh the canvas
                        break

    def handleCheck(self, room_name, coordinates):
        action = simpledialog.askstring("Action", "Enter action: add_door, correct_name, or add_wall")
        print(room_name)
        if action == "add_door":
            self.add_door(room_name)
        elif action == "correct_name":
            self.correct_room_name(room_name)
        elif action == "add_wall":
            self.add_wall(coordinates)

    # 3 Main Functions --------------------------------------------------------

    def add_door(self, room_name):
        self.selected_rooms.append(room_name)
        if len(self.selected_rooms) == 2:
            # Add door logic here
            room1, room2 = self.selected_rooms
            print(f"Adding door between {room1} and {room2}")
            # Update XML
            self.update_xml_with_door(room1, room2)
            self.selected_rooms = []

    def correct_room_name(self, room_name):
        new_name = simpledialog.askstring("Correct Room Name", f"Enter new name for {room_name}:")
        if new_name:
            print(f"Changing {room_name} to {new_name}")
            # Update XML
            self.update_xml_with_new_name(room_name, new_name)

    def add_wall(self, coordinates):
        # Logic to add wall here
        point1, point2 = coordinates  # You will need to select two points
        print(f"Adding wall between {point1} and {point2}")
        # Update XML
        self.update_xml_with_wall(point1, point2)

    # Update XML Functions ---------------------------------------------------

    def update_xml_with_door(self, room1, room2):
        pass

    def update_xml_with_new_name(self, old_name, new_name):
        oldXMLFilePath = BuildingMap.get(old_name)
        if not oldXMLFilePath:
            print(f"No file path found for room: {old_name}")
            return

        # Define the path to access the XML files in the new_xml folder in the project directory
        project_directory = os.path.dirname(os.path.abspath(__file__))  # Get the current project directory
        updated_folder_path = os.path.join(project_directory, "new_xml")

        try:
            # Construct the path for the old XML file
            old_xml_path = os.path.join(updated_folder_path, f"{old_name}.xml")
            if not os.path.exists(old_xml_path):
                print(f"File not found: {old_xml_path}")
                return

            # Parse the original XML file
            print(f"Parsing XML file from: {old_xml_path}")
            tree = ET.parse(old_xml_path)
            root = tree.getroot()

            # Update the XML content
            print(f"Updating XML content for room: {old_name} to {new_name}")
            root.set('name', new_name)
            root.set('key', new_name)
            for field in root.findall('.//field'):
                if field.get('key') == 'name':
                    content_element = field.find('content')
                    if content_element is not None:
                        content_element.text = new_name

            # Write the updated tree back to the existing XML file with the new name
            new_xml_path = os.path.join(updated_folder_path, f"{new_name}.xml")
            print(f"Saving updated XML file to: {new_xml_path}")
            tree.write(new_xml_path, encoding='utf-8', xml_declaration=True)

            # Remove the old XML file
            os.remove(old_xml_path)
            print(f"Deleted old XML file: {old_xml_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def update_xml_with_wall(self, point1, point2):
        pass

