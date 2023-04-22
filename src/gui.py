
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
#data = [("1001", "Pending", "2022-01-01", "SKU001", "10.00", "2", "20.00", "Clothing", "Credit Card", "CUST001"),
                #("1002", "Shipped", "2022-01-02", "SKU002", "20.00", "1", "20.00", "Electronics", "Paypal", "CUST002"),
                #("1003", "Delivered", "2022-01-03", "SKU003", "5.00", "3", "15.00", "Toys", "Credit Card", "CUST003"),
                #("1004", "Pending", "2022-01-04", "SKU004", "15.00", "2", "30.00", "Home & Kitchen", "Paypal", "CUST004"),
                #("1005", "Delivered", "2022-01-05", "SKU005", "25.00", "1", "25.00", "Jewelry", "Credit Card", "CUST005")]

       
        
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
        criteria_frame.pack(side="left", fill="y", padx=15, pady=15)

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

        # Create a label and dropdown menu for category selection
        # category_label = customtkinter.CTkLabel(criteria_frame, text="Category: ")
        # category_label.grid(row=1, column=2, padx=5, pady=5)
        # category_var=tk.StringVar()
        
        # category_choices = ["All", "Fashion", "Electronics", "Appliances"]
        # category_dropdown = ttk.OptionMenu(criteria_frame, category_var, *category_choices)
        # category_dropdown.grid(row=1, column=3, padx=5, pady=5)

        price_label = customtkinter.CTkLabel(criteria_frame, text="Price Range: ")
        price_label.grid(row=5, column=0, padx=5, pady=5)
        self.min_price_entry = ttk.Entry(criteria_frame, width=15)
        self.min_price_entry.grid(row=5, column=1, padx=5, pady=5)

        dash_label = customtkinter.CTkLabel(criteria_frame, text="-")
        dash_label.grid(row=5, column=2, padx=5, pady=5)

        self.max_price_entry = ttk.Entry(criteria_frame, width=15)
        self.max_price_entry.grid(row=5, column=3, padx=5, pady=5)

        # Create a frame for the table and visualization
        results_frame = tk.LabelFrame(self.root, text="Search Results" , padx=10, pady=10)
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

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

        #create vertical scrollbar


        # table_scroll_y = tk.Scrollbar(self.root, orient="vertical", command=table.yview)
        # table_scroll_y.pack(side="right", fill="y")
        # table.configure(yscrollcommand=table_scroll_y.set)
        # table.pack(side="left",fill="both", expand=True)
        # table_scroll_y.config(command=table.yview)
        # # Create a scrollbar for the table
        table_scroll_x = tk.Scrollbar(self.root, orient="horizontal", command=self.table.xview)
        table_scroll_x.pack(side="bottom", fill="x", padx=5, pady=5)
        self.table.configure(xscrollcommand=table_scroll_x.set)

        # scrollbar = Scrollbar(self.root)
        # scrollbar.pack( side = RIGHT, fill = Y )
        # mylist = Listbox(self.root, yscrollcommand = scrollbar.set )
        # for line in range(100):
        #    mylist.insert(END, 'This is line number' + str(line))
        # mylist.pack( side = LEFT, fill = BOTH )
        # scrollbar.config( command = mylist.yview )
        # mainloop()

        
        # Create a button for the order id search
        search_button = ttk.Button(criteria_frame, text="Search", width=10, command=self.search_by_order_id_range)
        search_button.grid(row=1, column=1, padx=10, pady=10)
        
        # create a button for price range search 
        price_range_button = ttk.Button(criteria_frame, text="Price Range", width=11, command=self.search_by_price_range)
        price_range_button.grid(row=9, column=1, padx=10, pady=10)

        # button for filter search 
        filter_button = ttk.Button(criteria_frame, text="Filter", width=10, command=self.filter_search)
        filter_button.grid(row=10, column=3, padx=10, pady=10)
        
        # report_button = ttk.Button(sidebar_frame, text="Generate Report", command=self.generate_report,width=15)
        # report_button.grid(row=9, column=1, padx=10, pady=10)

    
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
    # def search_orderid(self):
    #     #print("Searching for order ID")
    #     #order_id_var = search_term_var.get()
    #     #print(self.search_entry.get())
    #     #order_id = int(order_id_var)
    #     order_id_var = (self.search_entry.get())

    #     #print((order_id_var))
    #     if order_id_var == "":
    #         messagebox.showerror("Error", "Please enter an order ID")
    #     else:
    #         order_id = float(order_id_var)

    #     #"Order Status", "Date of Order", "SKU", "Price","Quantity", "Grand Total", "Category", "Payment Method", "Customer ID" of that order id
    #     # if not order_id_var:
    #     #     messagebox.showerror("Error", "Please enter an order ID")
    #     #     return
    #     # else:
    #         df = self.data
    #         order_data = df[df["item_id"] == order_id]
    #         if order_data.empty:
    #             messagebox.showerror("Error", "No order found with this order ID")
    #             return
    #         else:
    #             for i in self.table.get_children():
    #                 self.table.delete(i)
    #             for index, row in order_data.iterrows():
    #                 #'item_id', 'status', 'created_at', 'sku', 'price', 'qty_ordered','grand_total', 'category_name_1', 'payment_method', 'Working Date','Customer Since', 'Customer ID'
    #                 self.table.insert("", tk.END, values=list(row))
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


    # def test_range_search(self):
    # # Test range search for price attribute
    #     result = self.index.rangeSearch('price', 20, 50)
    #     expected_output = pd.DataFrame({
    #     'item_id': [2, 3, 4, 5],
    #     'price': [20, 30, 40, 50]
    # })
    #     assert result.equals(expected_output), f"Expected {expected_output}, but got {result['price'].tolist()}"
    # # def price_range(self, min_price, max_price):
    #     min_price = min_price.get()
    #     max_price = max_price.get()
    #     if min_price == "" or max_price == "":
    #         messagebox.showerror("Error", "Please enter a price range")
    #     else:
    #         df = pd.DataFrame(self.data)
    #         price_data = df[(df["price"] >= min_price) & (df["price"] <= max_price)]
    #         print(price_data)

    # def intersection_of_result(self, order_id, min_price, max_price):
    #     order_id = order_id.get()
    #     min_price = min_price.get()
    #     max_price = max_price.get()
    #     if order_id == "" or min_price == "" or max_price == "":
    #         messagebox.showerror("Error", "Please enter a price range")

    #     else:   
    #         df = pd.DataFrame(data)
    #         order_data = df[df["order_id"] == order_id]
    #         price_data = df[(df["price"] >= min_price) & (df["price"] <= max_price)]
    #         #print(order_data)
    #         #print(price_data)
    #         result = pd.merge(order_data, price_data, how='inner', on=['order_id'])
    #         print(result)
        #print 
        # Create a frame for the main content
        #df = pd.read_csv("data.csv")
    # def price_range(self):
    #     min_price = self.min_price.get()
    #     max_price = self.max_price.get()
    #     if min_price == "" or max_price == "":
    #         messagebox.showerror("Error", "Please enter a price range")
    #     else:
    #         df = pd.DataFrame(self.data)
    #         price_data = df[(df["price"] >= min_price) & (df["price"] <= max_price)]
    #         #print(price_data)
    #         for i in self.table.get_children():
    #             self.table.delete(i)
    #         for index, row in price_data.iterrows():
    #             self.table.insert("", tk.END, values=list(row))
    def sort_by_id(self):
        print("Sorting by order ID")
        result = self.index.sort('item_id')
        for i in self.table.get_children():
            self.table.delete(i)
        for index, row in result.iterrows():
            self.table.insert("", tk.END, values=list(row))

        
    def run(self):
        self.root.mainloop()
    #create object

#if __name__ == "__main__":


    



