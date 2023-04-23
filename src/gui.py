
import datetime
import sv_ttk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
#import ttkbootstrap as ttk
import pandas as pd
from tkcalendar import DateEntry
import customtkinter

from main import Index
        
class GUI:

    def __init__(self, data: pd.DataFrame):
        # Create the main window
    
        #self.category_var = tk.StringVar()
        self.start_date_var = DateEntry()
        self.end_date_var = DateEntry()
        #self.search_term_var = tk.StringVar()
        self.data = data
        self.index = Index('data\Pakistan Largest Ecommerce Dataset.csv')

        self.root = tk.Tk()
        #self.root.geometry("800x600")
        self.root.title("Sales Dashboard")
        customtkinter.set_appearance_mode("black")
        customtkinter.set_default_color_theme("dark-blue")
        # Set the default theme for all widgets
        self.bg_color = "#F5F5F5"
        self.fg_color = "#333333"
        self.accent_color = "#00A0D2"
        self.font_family = "Sens serif"
        self.font_size = 10
        # Create a frame for the search field and category filter
        # # # Create the top frame for search and category selection
        # # top_frame = ttk.Frame(root, padding="30 15 30 0")
        
        # Create a label and entry field for the search term
        #search results frame 
        criteria_frame = tk.LabelFrame(self.root, text="Search Criteria")
        criteria_frame.pack(side="top", fill="x", padx=15, pady=15)

        # Create a frame for the table and visualization
        results_frame = tk.LabelFrame(self.root, text="Search Results")
        results_frame.pack(side="top", fill="x", expand=True, padx=15, pady=15)

        # search_results_frame = tk.LabelFrame(self.root, text = "Search Results")
        # search_results_frame.pack(side=tk.TOP, padx=15, pady=0, fill=tk.X)
        search_label = customtkinter.CTkLabel(criteria_frame, text="Order ID Range: ")
        search_label.grid(row=0, column=0, padx=5, pady=5)
        self.min_search = ttk.Entry(criteria_frame, width=15)
        self.dash = customtkinter.CTkLabel(criteria_frame, text="-")
        self.dash.grid(row=0, column=2, padx=5, pady=5)
        self.min_search.grid(row=0, column=1, padx=5, pady=5)
        self.max_search = ttk.Entry(criteria_frame, width=15)
        self.max_search.grid(row=0, column=3, padx=5, pady=5)
        #self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        # search by order id 

        # Create a label and entry field for the search term
        search_label = customtkinter.CTkLabel(criteria_frame, text="Search at Order ID: ")
        search_label.grid(row=2, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(criteria_frame, width=15)
        self.search_entry.grid(row=2, column=1, padx=5, pady=5)

        price_label = customtkinter.CTkLabel(criteria_frame, text="Price Range: ")
        price_label.grid(row=6, column=0, padx=5, pady=5)
        self.min_price_entry = ttk.Entry(criteria_frame, width=15)
        self.min_price_entry.grid(row=6, column=1, padx=5, pady=5)

        dash_label = customtkinter.CTkLabel(criteria_frame, text="-")
        dash_label.grid(row=5, column=2, padx=5, pady=5)

        self.max_price_entry = ttk.Entry(criteria_frame, width=15)
        self.max_price_entry.grid(row=6, column=3, padx=5, pady=5)

        self.status = customtkinter.CTkLabel(criteria_frame, text="Status: ")
        self.status.grid(row=0, column=7, padx=5, pady=5)
        self.status_var = tk.StringVar()
        self.status_var.set("All")
        self.status_choices = ['complete', 'canceled', 'order_refunded', 'received', 'refund' ,'closed','fraud', 'holded' ,'exchange', 'pending_paypal', 'paid', '\\N' ,'cod' ,'pending','processing' ,'payment_review']
        self.status_dropdown = ttk.OptionMenu(criteria_frame, self.status_var, *self.status_choices)
        self.status_dropdown.grid(row=0, column=8, padx=5, pady=5)

        
        # Create a table to display the search results
        table_columns = list(self.data.columns)
        self.table = ttk.Treeview(results_frame, columns=table_columns, show="headings" ,padding="5 5 5 5")
        for column in table_columns:
            self.table.heading(column, text=column)
        self.table.pack(side="left", fill="both", expand=True)

        # Fill data in the table
        # for index,row in self.data.iterrows():
        #     #print(row)
        #     self.table.insert("", tk.END, values=list(row))

        # Create a scrollbar for the table
        #horizontal scrollbar
        table_scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.table.xview)
        table_scroll_x.pack(side="bottom", fill="x")
        self.table.configure(xscrollcommand=table_scroll_x.set)
        
        #vertical scrollbar
        table_scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.table.yview)
        table_scroll_y.pack(side="right", fill="both")
        self.table.configure(yscrollcommand=table_scroll_y.set)
        # Create a button for the order id search
        search_button = ttk.Button(criteria_frame, text="Search", width=10, command=self.search_by_order_id_range)
        search_button.grid(row=0, column=4, padx=10, pady=10)
        
        # create a button for price range search 
        price_range_button = ttk.Button(criteria_frame, text="Price Range", width=11, command=self.search_by_price_range)
        price_range_button.grid(row=10, column=1, padx=10, pady=10)

        # button for filter search 
        filter_button = ttk.Button(criteria_frame, text="Filter", width=10, command=self.filter_search)
        filter_button.grid(row=10, column=3, padx=10, pady=10)

        #sort button
        sort_button = ttk.Button(criteria_frame, text="Sort", width=10, command=self.sort_by_price)
        sort_button.grid(row=10, column=2, padx=10, pady=10)

        # status button
        status_button = ttk.Button(criteria_frame, text="Status", width=10, command=self.status_choice)
        status_button.grid(row=10, column=0, padx=10, pady=10)

        # report_button = ttk.Button(sidebar_frame, text="Generate Report", command=self.generate_report,width=15)
        # report_button.grid(row=9, column=1, padx=10, pady=10)
        # search button for order id
        search_button = ttk.Button(criteria_frame, text="Order ID", width=10, command=self.find_closest_order_id)
        search_button.grid(row=10, column=4, padx=10, pady=10)
    
        # Set the default style for all widgets
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".", font=(self.font_family, self.font_size), foreground=self.fg_color, background=self.bg_color)
        style.configure("TButton", padding=6, relief="flat", foreground=self.fg_color, background=self.accent_color, font=(self.font_family, self.font_size, "bold"))
        style.map("TButton", background=[("active", "#0081A7")])
        style.configure("TLabel", padding=5)
        style.configure("TEntry", padding=5, relief="flat", foreground="0000", background=self.bg_color, font=(self.font_family, self.font_size, "bold"))
        style.configure("TCombobox", padding=5, relief="flat", foreground=self.fg_color, background=self.bg_color)
        style.configure("Treeview", padding=5, relief="flat", foreground=self.fg_color, background=self.bg_color)
        style.configure("Treeview.Heading", font=(self.font_family, self.font_size, "bold"), background=self.accent_color, foreground=self.bg_color)


    def search_by_price_range(self):
        print("Searching by price range")
        print(self.min_price_entry.get())
        print(self.max_price_entry.get())
        if self.min_price_entry.get() == "" or self.max_price_entry.get() == "":
            messagebox.showerror("Error", "Please enter a price range")
            return
        else:

            result = self.index.rangeSearch('price', float(self.min_price_entry.get()), float(self.max_price_entry.get()))
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
    def search_by_order_id_range(self):
        print("Searching by order id range")
        print(self.min_search.get())
        print(self.max_search.get())
        if self.min_search.get() == "" or self.max_search.get() == "":
            messagebox.showerror("Error", "Please enter an order ID range")
            return
        else:
            result = self.index.rangeSearch('item_id', float(self.min_search.get()), float(self.max_search.get()))
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))

    def filter_search(self):
        print("Filtering search results")
        print(self.min_search.get())
        print(self.max_search.get())
        print(self.min_price_entry.get())
        print(self.max_price_entry.get())
        if self.min_search.get() == "" or self.max_search.get() == "":
            messagebox.showerror("Error", "Please enter an order ID range")
            return
        else:
            # Perform range search by order id
            result1 = self.index.rangeSearch('item_id', float(self.min_search.get()), float(self.max_search.get()))
            # Perform range search by price
            result2 = self.index.rangeSearch('price', float(self.min_price_entry.get()), float(self.max_price_entry.get()))
            # Merge the two results using inner join
            result = pd.merge(result1, result2, how='inner')
            if result.empty:
                messagebox.showerror("Error", "No results found")
                return
            # Update the table in the GUI
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
            return result
    def search_order_id (self):
        print("Searching by order id")
        print(self.search_entry.get())
        if self.search_entry.get() == "":
            messagebox.showerror("Error", "Please enter an order ID")
            return
        else:
            result = self.index.search('item_id', float(self.search_entry.get()))
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
                #clear the search entry after search
                self.search_entry.delete(0, 'end')


    def sort_by_price(self):
        
        print("Sorting by price")
        result = self.filter_search()
        result = result.sort_values(by=['price'])
        for i in self.table.get_children():
            self.table.delete(i)
        for index, row in result.iterrows():
            self.table.insert("", tk.END, values=list(row))
    def find_closest_order_id(self):
        print("Finding closest order ID")
        print(self.search_entry.get())
        if self.search_entry.get() == "":
            messagebox.showerror("Error", "Please enter an order ID")
            return
        else:
            #check if the value is in the tree
            result = self.index.search('item_id', float(self.search_entry.get()))
            for ids in result['item_id']:
                if float(self.search_entry.get()) == ids:
                    print("Value is in the tree")
                    for i in self.table.get_children():
                        self.table.delete(i)
                    for index, row in result.iterrows():
                        self.table.insert("", tk.END, values=list(row))
                        #clear text box after search
            # if the value is not in the tree, find the closest value
                else:
                        print("Value is not in the tree")
                        result = self.index.successor1('item_id', float(self.search_entry.get()))
                        for i in self.table.get_children():
                            self.table.delete(i)
                        for index, row in result.iterrows():
                            self.table.insert("", tk.END, values=list(row))
                            #clear text box after search
                            self.search_entry.delete(0, 'end') 

    def status_choice(self):
        #check if delivered status is selected return only result of the delivered status
        # check if the combox value is selected
        if self.status_var == 'complete':
            result = self.filter_search()

            result = result[result['status'] == 'complete']
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
        elif self.status_var == 'canceled':
            result = self.filter_search()
            result = result[result['status'] == 'canceled']
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
        elif self.status_var == 'order_refunded':
            result = self.filter_search()
            result = result[result['status'] == 'order_refunded']
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
        elif self.status_var == 'order_cancelled':
            result = self.filter_search()
            result = result[result['status'] == 'order_cancelled']
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
        elif self.status_var == 'order_refunded':
            result = self.filter_search()
            result = result[result['status'] == 'order_refunded']
            for i in self.table.get_children():
                self.table.delete(i)
            for index, row in result.iterrows():
                self.table.insert("", tk.END, values=list(row))
       
    def run(self):
        self.root.mainloop()
    #create object

#if __name__ == "__main__":


    



