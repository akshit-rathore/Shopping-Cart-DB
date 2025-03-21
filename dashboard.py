import tkinter as tk
from tkinter import ttk,messagebox
import psycopg2
from Shop import shopgui

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


# Function to Fetch User Profile
def fetch_user_profile(logged_in_user):
    cursor.execute("""SELECT u.userid, u.name, u.phoneNumber, COUNT(o.orderNumber)
                   FROM users u
                   LEFT JOIN orders o ON u.userid = o.userid
                   WHERE u.userid = %s
                   GROUP BY u.userid;"""
                   , (logged_in_user,))
    return cursor.fetchone()

def fetch_address(logged_in_user):
    cursor.execute("""SELECT a.addrid, a.name, a.contactPhoneNumber, a.province, a.city, a.streetaddr, a.postCode
                   FROM address a
                   WHERE a.userid = %s;"""
                   , (logged_in_user,))
    return cursor.fetchall()

# Function to Fetch Order History
def fetch_order_history(logged_in_user):
    cursor.execute("""SELECT o.orderNumber, o.totalAmount, o.paymentState, o.creationTime, COUNT(oi.itemid)
                   FROM orders o
                   JOIN orderitem oi ON o.orderNumber = oi.orderNumber
                   WHERE o.userid = %s
                   GROUP BY o.orderNumber;"""
                   , (logged_in_user,))
    return cursor.fetchall()

# Function to Display Dashboard
def open_dashboard(logged_in_user):
    dashboard = tk.Tk()
    dashboard.title("User Dashboard")
    dashboard.geometry("600x400")

    # Fetch Data
    user_data = fetch_user_profile(logged_in_user)
    address_data = fetch_address(logged_in_user)
    
    def handle_orders():
        
        order_history = tk.Tk()
        order_history.title("Order History")
        order_history.geometry("600x400")

        orders = fetch_order_history(logged_in_user)
        # Order History
        tk.Label(order_history, font=("Arial", 12, "bold")).pack()
        order_table = ttk.Treeview(order_history, columns=("Order ID", "Total Price","Status", "Date", "Items"), show="headings")
        order_table.heading("Order ID", text="Order ID")
        order_table.heading("Total Price", text="Total Price")
        order_table.heading("Status", text="Status")
        order_table.heading("Date", text="Date")
        order_table.heading("Items", text="Items")
        order_table.pack()

        for order in orders:
            order_table.insert("", "end", values=order)


    def handle_shop():
        shopgui(logged_in_user)


    # User Info
    tk.Label(dashboard, text="User Profile", font=("Arial", 14, "bold")).pack()
    tk.Label(dashboard, text=f"Name: {user_data[1]}").pack()
    tk.Label(dashboard, text=f"Phone: {user_data[2]}").pack()
    tk.Label(dashboard, text=f"Total Orders: {user_data[3]}").pack()

    tk.Label(dashboard, text="Addresses", font=("Arial", 12, "bold")).pack()
    address = ttk.Treeview(dashboard, columns=("Name", "Phone Number", "Province", "City", "Street Address", "Post Code"), show="headings")
    address.heading("Name", text="Name")
    address.heading("Phone Number", text="Phone Number")
    address.heading("Province", text="Province")
    address.heading("City", text="City")
    address.heading("Street Address", text="Street Address")
    address.heading("Post Code", text="Post Code")
    address.pack()

    for add in address_data:
        address.insert("", "end", values=add)

    tk.Button(dashboard, text="Order History", command=handle_orders).pack()
    tk.Button(dashboard, text="Shop", command=handle_shop).pack()
    

    dashboard.mainloop()
