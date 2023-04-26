import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
from tkcalendar import DateEntry
import customtkinter as ctk
from main import Index

class GUI:
    def __init__(self, path:str):
        self.window = tk.Tk()
        self.index = Index(path)
        self.data = self.index.data
        self.window.title("E-Commerce Dashboard")
        self.window.geometry("1280x800")


        # Set the default style for all widgets
        foreground_color = '#FFFFFF'
        background_color = '#23395D'
        font_style = "Sens serif"
        font_size = 10
        font_weight = "bold"

        # Apply the default style for all widgets
        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure("TButton", foreground=foreground_color, background=background_color, font=(font_style, font_size, font_weight))
        style.configure("TLabel", foreground=foreground_color, background=background_color, font=(font_style, font_size, font_weight))
        style.configure("TEntry", foreground=foreground_color, background=background_color, font=(font_style, font_size, font_weight))
        style.configure("Treeview", foreground=foreground_color, background=background_color, font=(font_style, font_size))
        style.configure("Treeview.Heading", foreground=foreground_color, background=background_color, font=(font_style, font_size, font_weight))

        # Search Criteria Frame
        criteria_frame = tk.LabelFrame(self.window, text="Search Criteria")
        criteria_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Property Type Label and Combobox
        category_type_label = tk.Label(criteria_frame, text="Category Type:")
        category_type_label.grid(row=0, column=0, padx=5, pady=5)

        category_type_values = [' '] + list(self.data['category_name_1'].unique())
        self.category_type_combobox = ttk.Combobox(criteria_frame, values=category_type_values)
        self.category_type_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.category_type_combobox.current(0)

        # Item ID Label and Entry
        item_id_label = tk.Label(criteria_frame, text="Item ID:")
        item_id_label.grid(row=1, column=0, padx=5, pady=5)

        self.min_item_id_entry = tk.Entry(criteria_frame)
        self.min_item_id_entry.grid(row=1, column=1, padx=5, pady=5)

        dash_label = tk.Label(criteria_frame, text="-")
        dash_label.grid(row=1, column=2, padx=5, pady=5)

        self.max_item_id_entry = tk.Entry(criteria_frame)
        self.max_item_id_entry.grid(row=1, column=3, padx=5, pady=5)

        # Price Range Label and Entry
        price_range_label = tk.Label(criteria_frame, text="Price Range:")
        price_range_label.grid(row=2, column=0, padx=5, pady=5)

        self.min_price_entry = tk.Entry(criteria_frame)
        self.min_price_entry.grid(row=2, column=1, padx=5, pady=5)

        dash_label = tk.Label(criteria_frame, text="-")
        dash_label.grid(row=2, column=2, padx=5, pady=5)

        self.max_price_entry = tk.Entry(criteria_frame)
        self.max_price_entry.grid(row=2, column=3, padx=5, pady=5)

        # Date Range Label and Entry
        date_range_label = tk.Label(criteria_frame, text="Date Range:")
        date_range_label.grid(row=3, column=0, padx=5, pady=5)

        self.min_date_entry = DateEntry(criteria_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.min_date_entry.grid(row=3, column=1, padx=5, pady=5)

        dash_label = tk.Label(criteria_frame, text="-")
        dash_label.grid(row=3, column=2, padx=5, pady=5)

        self.max_date_entry = DateEntry(criteria_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.max_date_entry.grid(row=3, column=3, padx=5, pady=5)

        # Search Button
        search_button = ttk.Button(criteria_frame, text="Search", command=self.search, style='TButton')
        search_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Clear Results Button
        clear_button = ttk.Button(criteria_frame, text="Clear", command=self.clear_all, style='TButton')
        clear_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        # Search Results Frame
        results_frame = tk.LabelFrame(self.window, text="Search Results")
        results_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Search Results Table
        table_columns = list(self.data.columns)
        self.results_table = ttk.Treeview(results_frame, columns=table_columns, show="headings")
        for column in table_columns:
            self.results_table.heading(column, text=column)
            self.results_table.column(column, anchor="center")
        self.results_table.pack(expand=True, fill="both", padx=15, pady=15)

        # Create the vertical scrollbar
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_table.yview)
        vsb.pack(side="right", fill="y")

        # Create the horizontal scrollbar
        hsb = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_table.xview)
        hsb.pack(side="bottom", fill="x")

        # Set the scrollbar commands for the Treeview widget
        self.results_table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def search(self):
        min_id = self.min_item_id_entry.get()
        # if min id not numeric
        if min_id and not min_id.isnumeric():
            messagebox.showerror("Error", "Item ID must be an integer")
            return
        max_id = self.max_item_id_entry.get()
        # if max id not numeric
        if max_id and not max_id.isnumeric():
            messagebox.showerror("Error", "Item ID must be an integer")
            return
        min_price = self.min_price_entry.get()
        # if min id not numeric
        if min_price and not min_price.isnumeric():
            messagebox.showerror("Error", "Price must be an integer")
            return
        max_price = self.max_price_entry.get()
        # if max id not numeric
        if max_price and not max_price.isnumeric():
            messagebox.showerror("Error", "Price must be an integer")
            return
        min_date = self.min_date_entry.get()
        max_date = self.max_date_entry.get()
        category_type = self.category_type_combobox.get()
       
        # check if only min id is input and nothing else
        if min_id and not max_id and not min_price and not max_price:
            result = self.index.search('item_id', float(min_id))

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)
            
            if len(result) == 0:
                messagebox.showerror("Error", "No results found")
            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_item_id_entry.delete(0,'end')
                self.category_type_combobox.set(" ")

        # check if only min price is input and nothing else
        elif min_price and not min_id and not max_id and not max_price:
            result = self.index.search('price', float(min_price))

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)

            if len(result) > 50000:
                messagebox.showerror("Error", "Too many results found, result may take time")    

            if len(result) == 0:
                messagebox.showerror("Error", "No results found")
            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_price_entry.delete(0,'end')
                self.max_price_entry.delete(0,'end')
            
        # check if only min id and max id are input and nothing else
        elif min_id and max_id and not min_price and not max_price:
            result = self.index.rangeSearch('item_id', float(min_id), float(max_id))

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)

            if len(result) > 50000:
                messagebox.showerror("Error", "Too many results found, result may take time")  

            if len(result) == 0:
                messagebox.showerror("Error", "No results found")
            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_item_id_entry.delete(0,'end')
                self.max_item_id_entry.delete(0,'end')

        # check if only min price and max price are input and nothing else
        elif min_price and max_price and not min_id and not max_id:
            result = self.index.rangeSearch('price', float(min_price), float(max_price))

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)

            if len(result) > 50000:
                messagebox.showerror("Error", "Too many results found, result may take time")

            if len(result) == 0:
                messagebox.showerror("Error", "No results found")
            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_price_entry.delete(0,'end')
                self.max_price_entry.delete(0,'end')

        # check if only min id and min price are input and nothing else
        elif min_id and min_price and not max_id and not max_price:
            result1 = self.index.search('item_id', float(min_id))
            result2 = self.index.search('price', float(min_price))
            result = self.index.intersection(result1,result2)

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)

            if len(result) > 50000:
                messagebox.showerror("Error", "Too many results found, result may take time")

            if len(result) == 0:
                messagebox.showerror("Error", "No results found")

            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_item_id_entry.delete(0,'end')
                self.min_price_entry.delete(0,'end')

        # check if only min id and max id and min price are input and nothing else
        elif min_id and max_id and min_price and not max_price:
            result1 = self.index.rangeSearch('item_id', float(min_id), float(max_id))
            result2 = self.index.search('price', float(min_price))
            result = self.index.intersection(result1,result2)

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)

            if len(result) > 50000:
                messagebox.showerror("Error", "Too many results found, result may take time")

            if len(result) == 0:
                messagebox.showerror("Error", "No results found")

            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_item_id_entry.delete(0,'end')
                self.max_item_id_entry.delete(0,'end')
                self.min_price_entry.delete(0,'end')

        # check if all input
        elif min_id and max_id and min_price and max_price:
            result1 = self.index.rangeSearch('item_id', float(min_id), float(max_id))
            result2 = self.index.rangeSearch('price', float(min_price), float(max_price))
            result = self.index.intersection(result1,result2)

            if category_type != " ":
                result = self.index.filter(category_type,result)

            if min_date != '4/26/23' and max_date != '4/26/23':
                result = self.index.filterByDate(pd.to_datetime(min_date), pd.to_datetime(max_date),result)

            if len(result) > 50000:
                messagebox.showerror("Error", "Too many results found, result may take time")

            if len(result) == 0:
                messagebox.showerror("Error", "No results found")

            else:
                result = self.index.get_sorted_indices(result)

                for i in self.results_table.get_children():
                    self.results_table.delete(i)

                for _, record in result.iterrows():
                    self.results_table.insert("", "end", values=list(record))

                self.min_item_id_entry.delete(0,'end')
                self.max_item_id_entry.delete(0,'end')
                self.min_price_entry.delete(0,'end')
                self.max_price_entry.delete(0,'end')
            
    def clear_all(self):
        for i in self.results_table.get_children():
            self.results_table.delete(i)

        self.min_item_id_entry.delete(0,'end')
        self.max_item_id_entry.delete(0,'end')
        self.min_price_entry.delete(0,'end')
        self.max_price_entry.delete(0,'end')
        self.category_type_combobox.set(" ")
        self.min_date_entry.set_date('4/26/23')
        self.max_date_entry.set_date('4/26/23')
        
    def run(self):
        self.window.mainloop()