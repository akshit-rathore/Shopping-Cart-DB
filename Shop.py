import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import date   

def shopgui(logged_in_user):
    try:
        # Database connection
        conn = psycopg2.connect(
            dbname="shoppingcart",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        print("Connected to PostgreSQL successfully!")
        cursor = conn.cursor()
    except Exception as e:
        print("Error connecting to the database:", e)
        exit()

    # Fetch Products
    def fetch_products():
        cursor.execute("SELECT pid, name, price FROM product;")
        return cursor.fetchall()

    # Add Product to Cart
    def add_to_cart():
        selected_item = product_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a product.")
            return

        item = product_list.item(selected_item)["values"]
        cart.insert("", "end", values=item)

    # Remove Product from Cart
    def remove_from_cart():
        selected_item = cart.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove.")
            return
        cart.delete(selected_item)
    
    def update_database_after_checkout(cart,total_amount,items_amt,items_price):
        cursor.execute("SELECT * FROM users where userid = %s",(logged_in_user,))
        count = cursor.fetchall()
        if not count:
            cursor.execute("INSERT INTO buyer VALUES (%s);",(logged_in_user))
        
        date = "2019-02-16"
        orderNumber = random.randint(10000000, 99999999)
        cursor.execute("INSERT INTO Orders VALUES(%s,%s,'Paid',%s,%s);",(orderNumber,logged_in_user,date,total_amount))

        for item_id in items_amt.keys():
            cursor.execute("SELECT MAX(itemid) FROM OrderItem;")
            iid = cursor.fetchone()[0] + 1 
            cursor.execute("INSERT INTO OrderItem VALUES(%s,%s,%s,%s,%s);",(iid,orderNumber,item_id,items_amt[item_id],items_amt[item_id]*items_price[item_id]))

    # Checkout
    def checkout():
        if not cart.get_children():
            messagebox.showerror("Error", "Cart is empty.")
            return
        total_amount = 0
        
        items_amt = dict()
        items_price = dict()
        for item in cart.get_children():
            pid = cart.item(item)["values"][0]
            price = cart.item(item)["values"][2]  # Get price value
            total_amount += price
            if pid not in items_amt.keys():
                items_amt[pid] = 1
                items_price[pid] = price
            else:
                items_amt[pid] += 1

        update_database_after_checkout(cart,total_amount,items_amt,items_price)
        conn.commit()

        messagebox.showinfo("Success", f"Purchase completed!\nTotal Amount: {total_amount}")
        cart.delete(*cart.get_children())  # Clear cart after checkout



    # GUI Setup
    root = tk.Tk()
    root.title("Shopping Cart")
    root.geometry("500x400")

    # Product List
    ttk.Label(root, text="Available Products").grid(row=0, column=0, padx=10, pady=5)
    product_list = ttk.Treeview(root, columns=("ID", "Product", "Price"), show="headings", height=8)
    product_list.heading("ID", text="ID")
    product_list.heading("Product", text="Product Name")
    product_list.heading("Price", text="Price")
    product_list.grid(row=1, column=0, padx=10, pady=5)

    # Populate Product List
    for product in fetch_products():
        product_list.insert("", "end", values=product)

    # Shopping Cart
    ttk.Label(root, text="Your Cart").grid(row=0, column=1, padx=10, pady=5)
    cart = ttk.Treeview(root, columns=("ID", "Product", "Price"), show="headings", height=8)
    cart.heading("ID", text="ID")
    cart.heading("Product", text="Product Name")
    cart.heading("Price", text="Price")
    cart.grid(row=1, column=1, padx=10, pady=5)

    # Buttons
    ttk.Button(root, text="Add to Cart", command=add_to_cart).grid(row=2, column=0, pady=10)
    ttk.Button(root, text="Remove", command=remove_from_cart).grid(row=2, column=1, pady=10)
    ttk.Button(root, text="Checkout", command=checkout).grid(row=3, column=0, columnspan=2, pady=10)

    # Start the GUI
    root.mainloop()

    # # Close Database Connection
    # cursor.close()
    # conn.close()

