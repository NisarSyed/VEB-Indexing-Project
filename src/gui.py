import datetime
import sv_ttk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#import ttkbootstrap as ttk
import pandas as pd
from tkcalendar import DateEntry
import customtkinter

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("E-Commerce Dataset Search")
        self.window.geometry("800x600")

        # Search Criteria Frame
        criteria_frame = tk.LabelFrame(self.window, text="Search Criteria")
        criteria_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Property Type Label and Combobox
        property_type_label = tk.Label(criteria_frame, text="Property Type:")
        property_type_label.grid(row=0, column=0, padx=5, pady=5)

        property_type_values = ["Apartment", "House", "Condominium", "Townhouse", "Loft", "Other"]
        self.property_type_combobox = ttk.Combobox(criteria_frame, values=property_type_values)
        self.property_type_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.property_type_combobox.current(0)

        # Price Range Label and Entry
        price_range_label = tk.Label(criteria_frame, text="Price Range:")
        price_range_label.grid(row=1, column=0, padx=5, pady=5)

        self.min_price_entry = tk.Entry(criteria_frame)
        self.min_price_entry.grid(row=1, column=1, padx=5, pady=5)

        dash_label = tk.Label(criteria_frame, text="-")
        dash_label.grid(row=1, column=2, padx=5, pady=5)

        self.max_price_entry = tk.Entry(criteria_frame)
        self.max_price_entry.grid(row=1, column=3, padx=5, pady=5)

        # Search Button
        search_button = tk.Button(criteria_frame, text="Search", command=self.search)
        search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        # Search Results Frame
        results_frame = tk.LabelFrame(self.window, text="Search Results")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Search Results Table
        self.results_table = ttk.Treeview(results_frame, columns=("id", "name", "host_name", "neighbourhood", "room_type", "price"), show="headings")
        self.results_table.column("id", width=50, anchor="center")
        self.results_table.column("name", width=200, anchor="center")
        self.results_table.column("host_name", width=150, anchor="center")
        self.results_table.column("neighbourhood", width=150, anchor="center")
        self.results_table.column("room_type", width=150, anchor="center")
        self.results_table.column("price", width=100, anchor="center")

        self.results_table.heading("id", text="ID")
        self.results_table.heading("name", text="Name")
        self.results_table.heading("host_name", text="Host Name")
        self.results_table.heading("neighbourhood", text="Neighbourhood")
        self.results_table.heading("room_type", text="Room Type")
        self.results_table.heading("price", text="Price")

        self.results_table.pack(fill="both", expand=True)

    def run(self):
        self.window.mainloop()

    def search(self):
        # Get search criteria
        property_type = self.property_type_combobox.get()
        min_price = int(self.min_price_entry.get()) if self.min_price_entry.get() else 0
        max_price = int(self.max_price_entry.get()) if self.max_price_entry.get() else 1000000

        # Load listings data
        listings = pd.read_csv("listings.csv")

        # Filter listings data
        listings = listings[listings["room_type"] == property_type]
        listings = listings[listings["price"] >= min_price] 
        listings = listings[listings["price"] <= max_price]

        # Clear table
        for record in self.results_table.get_children():
            self.results_table.delete(record)

        # Insert filtered listings into table
        for index, row in listings.iterrows():
            self.results_table.insert("", "end", values=(row["id"], row["name"], row["host_name"], row["neighbourhood"], row["room_type"], row["price"]))

if __name__ == "__main__":
    gui = GUI()
    gui.run()