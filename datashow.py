import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

class DisplayApp:
    def __init__(self, columns, rows, column_mask):
        self.columns = columns
        self.rows = rows
        self.column_mask = column_mask

        self.root = tk.Tk()
        self.root.title("Database Viewer")
        style = ThemedStyle(self.root)
        style.set_theme("breeze")

        # Create Treeview widget
        self.tree = ttk.Treeview(self.root, columns=self.column_mask, show='headings')
        for col in self.column_mask:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')  # You can adjust the width as needed

        for row in self.rows:
            filtered_row = [row[self.columns.index(col)] for col in self.column_mask]
            self.tree.insert("", "end", values=filtered_row)

        self.tree.pack(fill='both', expand=True)

        # Bind the selection event
        self.tree.bind("<ButtonRelease-1>", self.show_selected_row)

        # Resize the window based on the number of columns
        window_width = len(self.column_mask) * 100 + 20  # Assuming each column has a width of 100 pixels
        self.root.geometry(f"{window_width}x400")

    def show_selected_row(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            row_index = self.tree.index(selected_item)
            # Get the complete row data using the original columns list
            complete_row = [self.rows[row_index][self.columns.index(col)] for col in self.column_mask]
            print("Selected Row:", complete_row)

    def run(self):
        self.root.mainloop()

# Example usage:
if __name__ == "__main__":
    columns = ["ID", "Name", "Age", "Salary"]
    rows = [
        [1, "John", 25, 50000],
        [2, "Alice", 30, 60000],
        [3, "Bob", 22, 45000],
        # Add more rows as needed
    ]
    column_mask = ["ID", "Age", "Salary"]  # Specify the columns to display

    app = DisplayApp(columns, rows, column_mask)
    app.run()
