import tkinter as tk
from tkinter import messagebox
import psycopg2
from dashboard import open_dashboard

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

# Function to Register New User
def register_user(name, phoneNumber):
    cursor.execute("SELECT userid FROM users WHERE name = %s AND phoneNumber = %s;", (name.strip(),phoneNumber.strip()))
    return cursor.fetchone()

# Function to Verify User Login
def login_user(username, password):
    cursor.execute("SELECT userid, phoneNumber FROM users WHERE name = %s;", (username.strip(),))
    user = cursor.fetchone()
       
    if user and user[1]==password:
        return user[0]  # Return user ID if login is successful
    return None


# Global variable to store logged-in user ID
logged_in_user = None

# Function to Handle Login
def handle_login():
    global logged_in_user
    username = username_entry.get()
    password = password_entry.get()

    user_id = login_user(username, password)
    if user_id:
        logged_in_user = user_id
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        login_window.destroy()  # Close login window
        open_dashboard(logged_in_user)
        
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to Handle Signup
def handle_signup():
    username = username_entry.get()
    password = password_entry.get()

    if register_user(username, password):
        messagebox.showerror("Signup Failed", "User already exists.")
    else:
        cursor.execute("SELECT MAX(userid) FROM users;")
        uid = cursor.fetchone()[0] + 1 
        cursor.execute("INSERT INTO users (userid,name,phoneNumber) VALUES (%s,%s,%s);",(uid,username,password))
        conn.commit()
        messagebox.showinfo("Signup Successful", "You can now log in.")
        
# Create Login Window
login_window = tk.Tk()
login_window.title("Login / Signup")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=handle_login).pack(pady=5)
tk.Button(login_window, text="Sign Up", command=handle_signup).pack()

login_window.mainloop()
