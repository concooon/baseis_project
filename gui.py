import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import entrybox as eb

class DatabaseGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Εκδοτικός Οίκος")

        # Set window size and position (centered)
        width = 1000
        height = 600
        self.root.geometry(f"{width}x{height}")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - width) // 2
        y_coordinate = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

        # Style
        style = ThemedStyle(root)
        style.set_theme("breeze")  # List of themes at https://ttkthemes.readthedocs.io/en/latest/themes.html

        # Create tabs container
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(expand=1, fill="both")
        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_selected) # on tab change, "build" that tab 

        # Tables of the database (each table is a tab)
        # Each table has a list of columns:
        # + Column name
        # + Description
        # + regex for validation
        # + Field type (entry, combobox, etc)
        # + (Optional) Values for combobox field
        self.tables = {
            "Employee": [
                ("AFM", "ΑΦΜ υπαλλήλλου (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"), 
                ("Last_name", "Επώνυμο (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("First_name", "Όνομα (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Address", "Διέυθυνση [Οδός, Αριθμός, Τ.Κ.] (αλφαριθμητικό)", r"^(.*?),\s(\d+),\s(\w+)$", "entry"),
                ("Contact_number", "Τηλέφωνο επικοινωνίας (ακέραιος - 10 ψηφία)", r"^\d{10}$", "entry"),
                ("Email", "Διεύθυνση Email (αλφαριθμητικό)", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "entry"),
                ("Dno", "Κωδικός τμήματος (ακέραιος 1-10)", None, "entry"), #todo department numbers??
                ("Salary", "Μηνιαίος μισθός [€] (ακέραιος)", r"^\d+$", "entry")
            ],
            "Department": [
                ("ID", "placeholder", None,  "combobox", ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")), 
                ("Name", "placeholder", None, "entry")
            ]
        }

        # Create tabs
        for table, columns in self.tables.items():
            tab = ttk.Frame(self.tabs)
            self.tabs.add(tab, text=table)

    def on_tab_selected(self, event):
        # Get the currently selected tab
        current_tab_index = self.tabs.index(self.tabs.select())
        current_tab = self.tabs.winfo_children()[current_tab_index]

        # Get the columns for the current tab
        current_table = list(self.tables.keys())[current_tab_index]
        current_columns = self.tables[current_table]

        # Create fields for the current tab
        self.create_tab_fields(current_tab, current_columns)


    def create_tab_fields(self, tab, columns):
        # Populate tab i.e. create fields for table columns
        # tab : parent window
        # columns : list of columns of table

        num_columns = 3 # number of columns in grid
        width = 40 # width of elements
        self.entries = {} # dictionary of entries
        tab.bind("<Button-1>", lambda event: tab.focus_set()) # on bg click, focus tab, i.e. remove focus from entry fields

        # -------- entry fields --------
        # for each column of table...
        for i, column in enumerate(columns):
            # 1. Set row and column
            row = i // num_columns
            col = i % num_columns

            # 2. Create housing frame and assign to dictionary
            self.entries[column[0]] = eb.EnntryBox(tab, row, col, width, column, callback=self.update)


        # -------- buttons --------
        # Search button
        self.search_button = ttk.Button(tab, text="Search", state="disabled", command=None)
        self.search_button.grid(row=len(columns) + 1, column=1, padx=5, pady=50, sticky="e")

        # Add button
        self.add_button = ttk.Button(tab, text="Add", state="disabled", command=None)
        self.add_button.grid(row=len(columns) + 1, column=2, padx=5, pady=50, sticky="w")
        
        # Reset button
        self.reset_button = ttk.Button(tab, text="Reset", command=self.reset)
        self.reset_button.grid(row=len(columns) + 1, column=2, padx=110, pady=50, sticky="w")

    def update(self, event):
        # Callback function for entry fields losing focus.
        # Enables/disables buttons as follows
        # checked values are stored in self.data of each item in self.entries dictionary
        
        # + Search button is enabled if there are no erros at least one entry is not empty
        # if any value is False, then search is invalid -> disable search button
        # if all values are "", then search is empty -> disable search button
        # if at least one value != "", then search is allowed -> enable search button
        if any(value.data != "" for value in self.entries.values()) and all(value.data != False for value in self.entries.values()):
            self.search_button.config(state="enabled")
        else:
            self.search_button.config(state="disabled")

        # + Add button is enabled if all entries are valid and not empty
        # if any value is False or "", then add is invalid -> disable add button
        # if all values are not False and != "", then add is allowed -> enable add button
        if all(value.data != "" and value.data != False for value in self.entries.values()):
            self.add_button.config(state="enabled")
        else:
            self.add_button.config(state="disabled")

        # + Reset button is always enabled
    
    def reset(self):
        # Resets all entry fields and buttons
        for  value in self.entries.values():
            value.reset()
        self.update(None)


    def search_data(self, tab, table):
        # Placeholder for search functionality
        print(f"Searching in {table} tab")

    def add_data(self, tab, table):
        # Placeholder for add functionality
        print(f"Adding data in {table} tab")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
