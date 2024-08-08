from tkinter import simpledialog


class CustomDialog(simpledialog.Dialog):
    def __init__(self, master, room_name):
        self.room_name = room_name
        super().__init__(master)

    def body(self, master):
        tk.Label(master, text=f"Enter new name for Room: {self.room_name}").pack(pady=5)
        self.entry = tk.Entry(master, width=30)
        self.entry.pack(pady=5)

    def apply(self):
        self.result = self.entry.get()
