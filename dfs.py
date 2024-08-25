
    def __init__(self, building, campus, *args, **kwargs):
        self.adding_wall = None
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
        self.legend_window = None
        self.title("UofA Building 2D UI")
        self.geometry("1200x800")  # Adjusted default size
        self.resizable(True, True)

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.container.grid_rowconfigure(0, weight=0)
        self.container.grid_rowconfigure(1, weight=0)
        self.container.grid_rowconfigure(2, weight=1)  # Make sure the canvas row expands
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=0)

        self.welcome_label = tk.Label(self.container, text=f"Welcome to UofA {building} Architecture UI",
                                      font=("Helvetica", 24, "bold"), anchor="center")
        self.welcome_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        button_frame = ttk.Frame(self.container)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        floors = count_level_subfolders(Original_Building_Path, campus, building, "interior")
        if not floors:
            self.no_data_label = tk.Label(self.container, text="No data found", font=("Helvetica", 18, "italic"),
                                          fg="red")
            self.no_data_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")
            button_frame.grid_remove()
        else:
            self.no_data_label = None
            for floor in floors:
                button = ttk.Button(button_frame, text=f"Floor {floor}",
                                    command=lambda f=floor: self.plot_floor_map(f, building, campus))
                button.pack(side=tk.LEFT, padx=5, pady=5)

        style = ttk.Style()
        style.configure('TButton', font=("Helvetica", 12, "bold"), background='#4CAF50', foreground='white')

        self.canvas_frame = ttk.Frame(self.container)
        self.canvas_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.check_errors_button = ttk.Button(self.container, text="Check Room Name", command=self.correct_room_name,
                                              style='TButton')
        self.check_errors_button.grid(row=1, column=1, pady=5, padx=10, sticky='n')
        self.check_errors_button.grid_remove()

        self.generate_neighbours_button = ttk.Button(self.container, text="Generate Neighbours Data",
                                                     command=self.calling_generating_neigbours_func, style='TButton')
        self.generate_neighbours_button.grid(row=2, column=1, pady=5, padx=10, sticky='n')
        self.generate_neighbours_button.grid_remove()

        self.add_wall_button = ttk.Button(self.container, text="Add Wall", command=self.add_wall_func, style='TButton')
        self.add_wall_button.grid(row=3, column=1, pady=5, padx=10, sticky='n')
        self.add_wall_button.grid_remove()

        self.selected_rooms = []

        self.bind("<Configure>", self.on_resize)  # Bind resize event

    def plot_floor_map(self, floor, building, campus):
        self.current_floor = floor
        self.check_errors_button.grid()
        self.generate_neighbours_button.grid()
        self.add_wall_button.grid()

        if self.legend_window is not None and self.legend_window.winfo_exists():
            self.legend_window.destroy()

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        points_categories, category_names, title = self.get_floor_data(floor, building, campus)
        self.fig, room_colors, colors = self.create_figure(points_categories, category_names, title)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.update_plot()

        self.legend_window = show_legend_window(colors, category_names, floor)

    def create_figure(self, points_categories, category_names, title):
        fig, ax = plt.subplots(figsize=(8, 6))  # Default figure size
        ax.set_title(title)
        for points_category in points_categories:
            for points in points_category:
                room_number = points[0][0]
                room_points = np.array(points[1:])
                centroid = np.mean(room_points, axis=0)
                ax.fill(room_points[:, 0], room_points[:, 1], alpha=0.5, label=room_number)
                ax.text(centroid[0], centroid[1], room_number, fontsize=10, ha='center', va='center')
        ax.legend()
        return fig, [], []  # Adjust as needed

    def on_resize(self, event):
        self.update_plot()

    def update_plot(self):
        if self.canvas:
            self.fig.set_size_inches(self.canvas.get_width_height()[0] / self.fig.dpi,
                                     self.canvas.get_width_height()[1] / self.fig.dpi, forward=True)
            self.canvas.draw()

=
