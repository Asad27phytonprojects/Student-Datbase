import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------- Database Connection ----------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="asad.",
    database="studens_record"
)
cursor = conn.cursor(dictionary=True)

# ---------------------- Login Window ----------------------
def login_window():
    def try_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        cursor.execute(
            "SELECT * FROM users_table WHERE username=%s AND Passwor=%s AND is_active=1",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            login.destroy()
            if user['rol'] == 'admin':
                admin_dashboard(user)
            elif user['rol'] == 'student':
                student_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login = tk.Tk()
    login.title("Student Management System - Login")
    login.geometry("350x220")
    login.configure(bg="#f0f2f5")

    tk.Label(login, text="Login", font=("Helvetica", 18, "bold"), bg="#f0f2f5").pack(pady=10)
    tk.Label(login, text="Username", bg="#f0f2f5").pack()
    username_entry = tk.Entry(login, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    tk.Label(login, text="Password", bg="#f0f2f5").pack()
    password_entry = tk.Entry(login, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=5)

    tk.Button(login, text="Login", font=("Helvetica", 12), bg="#4a7abc", fg="white", width=15, command=try_login).pack(pady=15)

    login.mainloop()

# ---------------------- Admin Dashboard ----------------------
def admin_dashboard(user):
    admin = tk.Tk()
    admin.title(f"Admin Dashboard - {user['username']}")
    admin.geometry("900x600")
    admin.configure(bg="#f0f2f5")

    # Sidebar
    sidebar = tk.Frame(admin, bg="#2c3e50", width=180)
    sidebar.pack(side="left", fill="y")

    tk.Label(sidebar, text="Admin Menu", bg="#2c3e50", fg="white", font=("Helvetica", 14, "bold")).pack(pady=20)

    frame = tk.Frame(admin, bg="#f0f2f5")
    frame.pack(side="right", fill="both", expand=True)

    # ---------------------- Functions ----------------------
    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def view_students():
        clear_frame()
        tk.Label(frame, text="All Students", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)

        cursor.execute("SELECT * FROM students_table")
        students = cursor.fetchall()

        columns = ("ID", "Name", "Email", "Enrolled")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        for s in students:
            tree.insert("", "end", values=(s["students_id"], s["Namee"], s["email"], s["enrolled"]))

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, pady=10)

    def view_payments():
        clear_frame()
        tk.Label(frame, text="All Payments", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)

        cursor.execute("SELECT * FROM payments_table")
        payments = cursor.fetchall()

        columns = ("PaymentID", "StudentID", "Amount", "Status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        for p in payments:
            tree.insert("", "end", values=(p["payments_id"], p["students_id"], p["amount"], p["order_status"]))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, pady=10)

    # ---------------------- Show Graph ----------------------
    def show_graph():
        clear_frame()
        tk.Label(frame, text="Student Statistics", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)

        cursor.execute("SELECT COUNT(*) as total FROM students_table")
        total_students = cursor.fetchone()["total"]

        # Create figure
        fig = Figure(figsize=(4.5, 3.5), dpi=100)
        ax = fig.add_subplot(111)

        bars = ax.bar(["Students"], [total_students], color="#4a90e2", edgecolor="black")

        # Add value labels
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 1, str(yval),
                    ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax.set_ylim(0, 50)
        ax.set_ylabel("Number of Students", fontsize=11)
        ax.set_title("Total Students Count", fontsize=12, fontweight="bold")
        ax.yaxis.grid(True, linestyle="--", alpha=0.7)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    def logout():
        admin.destroy()
        login_window()

    # Sidebar Buttons
    tk.Button(sidebar, text="View Students", bg="#34495e", fg="white", font=("Helvetica", 12), width=18, command=view_students).pack(pady=10)
    tk.Button(sidebar, text="View Payments", bg="#34495e", fg="white", font=("Helvetica", 12), width=18, command=view_payments).pack(pady=10)
    tk.Button(sidebar, text="Show Graph", bg="#34495e", fg="white", font=("Helvetica", 12), width=18, command=show_graph).pack(pady=10)
    tk.Button(sidebar, text="Logout", bg="#e74c3c", fg="white", font=("Helvetica", 12), width=18, command=logout).pack(side="bottom", pady=20)

    admin.mainloop()

# ---------------------- Student Dashboard ----------------------
def student_dashboard(user):
    cursor.execute("SELECT * FROM students_table WHERE user_id=%s", (user["user_id"],))
    student = cursor.fetchone()

    stud = tk.Tk()
    stud.title(f"Student Dashboard - {student['Namee']}")
    stud.geometry("700x400")
    stud.configure(bg="#f0f2f5")

    sidebar = tk.Frame(stud, bg="#2c3e50", width=150)
    sidebar.pack(side="left", fill="y")

    frame = tk.Frame(stud, bg="#f0f2f5")
    frame.pack(side="right", fill="both", expand=True)

    tk.Label(sidebar, text="Student Menu", bg="#2c3e50", fg="white", font=("Helvetica", 14, "bold")).pack(pady=20)

    def clear_frame():
        for widget in frame.winfo_children():
            widget.destroy()

    def view_details():
        clear_frame()
        tk.Label(frame, text="My Details", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)
        tk.Label(frame, text=f"ID: {student['students_id']}", bg="#f0f2f5", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(frame, text=f"Name: {student['Namee']}", bg="#f0f2f5", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(frame, text=f"Email: {student['email']}", bg="#f0f2f5", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(frame, text=f"Enrolled: {student['enrolled']}", bg="#f0f2f5", font=("Helvetica", 12)).pack(pady=5)

    def view_payments():
        clear_frame()
        tk.Label(frame, text="My Payments", font=("Helvetica", 16, "bold"), bg="#f0f2f5").pack(pady=10)

        cursor.execute("SELECT * FROM payments_table WHERE students_id=%s", (student["students_id"],))
        payments = cursor.fetchall()

        columns = ("PaymentID", "Amount", "Status")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        for p in payments:
            tree.insert("", "end", values=(p["payments_id"], p["amount"], p["order_status"]))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, pady=10)

    def logout():
        stud.destroy()
        login_window()

    tk.Button(sidebar, text="My Details", bg="#34495e", fg="white", font=("Helvetica", 12), width=18, command=view_details).pack(pady=10)
    tk.Button(sidebar, text="My Payments", bg="#34495e", fg="white", font=("Helvetica", 12), width=18, command=view_payments).pack(pady=10)
    tk.Button(sidebar, text="Logout", bg="#e74c3c", fg="white", font=("Helvetica", 12), width=18, command=logout).pack(side="bottom", pady=20)

    stud.mainloop()

# ---------------------- Run ----------------------
login_window()

cursor.close()
conn.close()
