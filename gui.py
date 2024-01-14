import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import entrybox as eb
import dbms
import datashow as ds

class DatabaseGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Εκδοτικός Οίκος")

        # Set window size and position (centered)
        width = 1200
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
        # Each table has a list of columns consisting of:
        # + Column name
        # + Description
        # + regex for validation
        # + Field type (entry, combobox, etc)
        # + (Optional) Values for combobox field
        self.tables = {
            "Employee": [
                ("AFM", "ΑΦΜ υπαλλήλλου (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("Dno", "Κωδικός τμήματος (ακέραιος 1-10)", r"^[1-9]$", "entry"),
                ("First_name", "Όνομα (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Last_name", "Επώνυμο (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Salary", "Μηνιαίος μισθός [€] (ακέραιος)", r"^\d+$", "entry"),
                ("Address", "Διέυθυνση [Οδός, Αριθμός, Τ.Κ.] (αλφαριθμητικό)", r"^(.*?),\s(\d+),\s(\w+)$", "entry"),
                ("Contact_number", "Τηλέφωνο επικοινωνίας (ακέραιος - 10 ψηφία)", r"^\d{10}$", "entry"),
                ("Email", "Διεύθυνση Email (αλφαριθμητικό)", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "entry")
            ],
            "Department": [
                ("Dnumber", "κωδικός τμήματος [1-9]", r"^[1-9]$",  "combobox", ("1", "2", "3", "4", "5", "6", "7", "8", "9")), 
                ("Name", "Όνομα τμήματος", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "combobox", ('Λογιστήριο', 'Νομικό', 'Διαφήμιση', 'Editing', 'IT', 'Πωλήσεις', 'Μεταφράσεις', 'Production', 'Εξυπνηρέτηση πελατών'))
            ],
            "Book": [
                ("ISBN", "ISBN βιβλίου (ακέραιος - 13 ψηφία)", r"^\d{13}$", "entry"), 
                ("Title", "Τίτλος βιβλίου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Author", "Συγγραφέας βιβλίου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Language", "Γλώσσα βιβλίου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Page_count", "αριθμός σελίδων (ακέραιος)", r"^\d+$", "entry"),
                ("Inventory_count", "αριθμός αποθέματος (ακέραιος)", r"^\d+$", "entry"),
                ("Price", "Τιμή βιβλίου [€] (δεκαδικός)", r"^\d+\.\d\d$", "entry"),
                ("Project_Id", "Κωδικός έργου (ακέραιος)", r"^\d+$", "entry")
            ],
            "Take_on": [
                ("Dno", "Κωδικός τμήματος (ακέραιος 1-10)", r"^[1-9]$","combobox", ("1", "2", "3", "4", "5", "6", "7", "8", "9")),
                ("Pno", "Κωδικός έργου (ακέραιος)", r"^\d+$", "entry")
            ],
            "Works_on": [
                ("Emp_AFM", "ΑΦΜ υπαλλήλλου (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("Pno", "Κωδικός έργου (ακέραιος)", r"^\d+$", "entry"),
                ("Hours", "Ώρες εργασίας (ακέραιος)", r"^\d+$", "entry")
            ],
            "COOPERATES": [
                ("AFM", "ΑΦΜ υπαλλήλλου (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("Pno", "Κωδικός έργου (ακέραιος)", r"^\d+$", "entry"),
                ("Payment", "Πληρωμή (ακέραιος)", r"^\d+$", "entry"),
                ("Notes", "Σημειώσεις (αλφαριθμητικό)", r".*", "entry")
            ],
            "FREELANCER": [
                ("AFM", "ΑΦΜ ελεύθερου επαγγελματία (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("First_name", "Όνομα (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Last_name", "Επώνυμο (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Address", "Διέυθυνση [Οδός, Αριθμός, Τ.Κ.] (αλφαριθμητικό)", r"^(.*?),\s(\d+),\s(\w+)$", "entry"),
                ("Email", "Διεύθυνση Email (αλφαριθμητικό)", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "entry"),
                ("Contact_number", "Τηλέφωνο επικοινωνίας (ακέραιος - 10 ψηφία)", r"^\d{10}$", "entry"),
                ("Profession", "Επάγγελμα (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry")
            ],
            "PROJECT": [
                ("Project_number", "Κωδικός έργου (ακέραιος)", r"^\d+$", "entry"),
                ("Title", "Τίτλος έργου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Description", "Περιγραφή έργου (αλφαριθμητικό)", r".*", "entry"),
                ("Type", "Τύπος έργου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Start_date", "Ημερομηνία έναρξης (yyyy-mm-dd)", r"^\d{4}-\d{2}-\d{2}$", "entry"),
                ("End_date", "Ημερομηνία λήξης (yyyy-mm-dd)", r"^\d{4}-\d{2}-\d{2}$", "entry"),
                ("Real_start_date", "Πραγματική ημερομηνία έναρξης (yyyy-mm-dd)", r"^\d{4}-\d{2}-\d{2}$", "entry"),
                ("Real_end_date", "Πραγματική ημερομηνία λήξης (yyyy-mm-dd)", r"^\d{4}-\d{2}-\d{2}$", "entry")
            ],
            "BOOK": [
                ("ISBN", "ISBN βιβλίου (ακέραιος - 13 ψηφία)", r"^\d{13}$", "entry"),
                ("Title", "Τίτλος βιβλίου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Author", "Συγγραφέας βιβλίου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Language", "Γλώσσα βιβλίου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Page_count", "Αριθμός σελίδων (ακέραιος)", r"^\d+$", "entry"),
                ("Inventory_count", "Αριθμός αποθέματος (ακέραιος)", r"^\d+$", "entry"),
                ("Price", "Τιμή βιβλίου [€] (δεκαδικός)", r"^\d+.\d\d$", "entry"),
                ("Project_Id", "Κωδικός έργου (ακέραιος)", r"^\d+$", "entry")
            ],
            "BOOKSTORE": [
                ("AFM", "ΑΦΜ βιβλιοπωλείου (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("Name", "Όνομα βιβλιοπωλείου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry"),
                ("Address", "Διεύθυνση βιβλιοπωλείου (αλφαριθμητικό)", r"^(.*?),\s(\d+),\s(\w+)$", "entry"),
                ("Email", "Διεύθυνση Email βιβλιοπωλείου (αλφαριθμητικό)", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "entry"),
                ("Website", "Ιστοσελίδα βιβλιοπωλείου (αλφαριθμητικό)", r"^(http://www\.|https://www\.|http://|https://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", "entry")
            ],
            "PERSON": [
                ("AFM", "ΑΦΜ προσώπου (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("Name", "Όνομα προσώπου (αλφαριθμητικό)", r"^[A-Za-zΑ-ΩΆΈΉΊΌΎΏα-ωάέήίόύώ-]+$", "entry")
            ],
            "CUSTOMER": [
                ("AFM", "ΑΦΜ πελάτη (ακέραιος - 9 ψηφία)", r"^\d{9}$", "entry"),
                ("Contact_phone", "Τηλέφωνο επικοινωνίας πελάτη (ακέραιος - 10 ψηφία)", r"^\d{10}$", "entry")
            ],
            "SALE": [
                ("Id", "Κωδικός πώλησης (ακέραιος)", r"^\d+$", "entry"),
                ("Date", "Ημερομηνία πώλησης (yyyy-mm-dd HH:MM:SS)", r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", "entry"),
                ("Subtotal", "Σύνολο χωρίς έκπτωση [€] (δεκαδικός)", r"^\d+.\d\d$", "entry"),
                ("Discount", "Έκπτωση (%)", r"^\d+$", "entry"),
                ("Total", "Συνολικό ποσό [€] (δεκαδικός)", r"^\d+.\d\d$", "entry"),
                ("Customer_Id", "Κωδικός πελάτη (ακέραιος)", r"^\d+$", "entry")
            ],
            "TO_SALE": [
                ("Book_id", "Κωδικός βιβλίου (αλφαριθμητικό)", r"^.*$", "entry"),
                ("Sale_id", "Κωδικός πώλησης (ακέραιος)", r"^\d+$", "entry"),
                ("Quantity", "Ποσότητα (ακέραιος)", r"^\d+$", "entry")
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
        self.search_button = ttk.Button(tab, text="Search", state="disabled", command=self.search_data)
        self.search_button.grid(row=len(columns) + 1, column=1, padx=5, pady=50, sticky="e")

        # Add button
        self.add_button = ttk.Button(tab, text="Add", state="disabled", command=self.add_data)
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


    def search_data(self):
        #search entry data in database
        new_dict = {key: (value.data, True) for key, value in self.entries.items()}

        # Get the currently selected tab which is the table name
        current_tab_index = self.tabs.index(self.tabs.select())
        current_tab = self.tabs.winfo_children()[current_tab_index]
        tab = self.tabs.tab(current_tab, option="text")

        # query database
        columns, results, column_mask =  dbms.search(tab, new_dict)
        print("Columns:", columns)
        print("Results:", results)
        print("Column Mask:", column_mask)
        ds.DisplayApp(columns, results, column_mask).run()

    def add_data(self):
        #insert entry data to database
        new_dict = {key: value.data for key, value in self.entries.items()}

        # Get the currently selected tab which is the table name
        current_tab_index = self.tabs.index(self.tabs.select())
        current_tab = self.tabs.winfo_children()[current_tab_index]
        tab = self.tabs.tab(current_tab, option="text")

        # query database
        dbms.add_data(tab, new_dict)


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseGUI(root)
    root.mainloop()
