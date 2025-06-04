import tkinter as tk
from tkinter import messagebox
import mysql.connector
import dashboard1  # Your main dashboard

# ---------- DATABASE FUNCTIONS ----------

def verify_login(username, password):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@9920600274',
            database='mental_health'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False

def register_user(username, password):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='@9920600274',
            database='mental_health'
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        messagebox.showerror("Registration Error", "Username already exists.")
        return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False

# ---------- ACTIONS ----------

def login():
    user = username_entry.get()
    pwd = password_entry.get()
    if verify_login(user, pwd):
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()
        main_app = tk.Tk()
        dashboard1.DashboardApp(main_app)
        main_app.mainloop()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password...Please check again")

def register():
    user = reg_username_entry.get()
    pwd = reg_password_entry.get()
    if user and pwd:
        if register_user(user, pwd):
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            reg_username_entry.delete(0, tk.END)
            reg_password_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Required", "Please fill in all fields.")

# ---------- GUI ----------

root = tk.Tk()
root.title("Login Page")
root.geometry("1300x1200")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="white", bd=2, relief="groove", padx=40, pady=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Login Section
tk.Label(frame, text="Login", font=("Castellar", 20 , "bold"), bg="white").pack(pady=10)

tk.Label(frame, text="Username:", font=("Arial", 12), bg="white").pack(anchor="w")
username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
username_entry.pack(pady=5)

tk.Label(frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w")
password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
password_entry.pack(pady=5)

tk.Button(frame, text="Login", command=login, bg="lightblue", font=("Arial", 12), width=20, height=2).pack(pady=15)

# Separator
tk.Label(frame, text="--------------------------", bg="white", fg="gray").pack(pady=10)

# Register Section
tk.Label(frame, text="New User? Register Below", font=("Arial", 12, "italic"), bg="white").pack(pady=5)

tk.Label(frame, text="Username:", font=("Arial", 12), bg="white").pack(anchor="w")
reg_username_entry = tk.Entry(frame, font=("Arial", 12), width=30)
reg_username_entry.pack(pady=5)

tk.Label(frame, text="Password:", font=("Arial", 12), bg="white").pack(anchor="w")
reg_password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=30)
reg_password_entry.pack(pady=5)

tk.Button(frame, text="Register", command=register, bg="lightgreen", font=("Arial", 12), width=20, height=2).pack(pady=15)

root.mainloop()
