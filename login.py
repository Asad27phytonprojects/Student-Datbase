import mysql.connector

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="asad.",          # change if needed
    database="studens_record"
)

cursor = conn.cursor(dictionary=True)


# ---------------------- Admin Menu ----------------------
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View all students")
        print("2. View all payments")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            cursor.execute("SELECT * FROM students_table")
            students = cursor.fetchall()
            print("\nAll Students:")
            for s in students:
                print(f"ID: {s['students_id']}, Name: {s['Namee']}, Email: {s['email']}, Enrolled: {s['enrolled']}")

        elif choice == "2":
            cursor.execute("SELECT * FROM payments_table")
            payments = cursor.fetchall()
            print("\nAll Payments:")
            for p in payments:
                print(f"Payment ID: {p['payments_id']}, Student ID: {p['students_id']}, Amount: {p['amount']}, Status: {p['order_status']}")

        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("❌ Invalid choice, try again.")


# ---------------------- Student Menu ----------------------
def student_menu(user_id):
    while True:
        print("\n--- Student Menu ---")
        print("1. View my details")
        print("2. View my payments")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            cursor.execute("SELECT * FROM students_table WHERE user_id = %s", (user_id,))
            student = cursor.fetchone()
            if student:
                print(f"\nID: {student['students_id']}, Name: {student['Namee']}, Email: {student['email']}, Enrolled: {student['enrolled']}")
            else:
                print("❌ Student record not found.")

        elif choice == "2":
            cursor.execute("SELECT * FROM students_table WHERE user_id = %s", (user_id,))
            student = cursor.fetchone()
            if student:
                cursor.execute("SELECT * FROM payments_table WHERE students_id = %s", (student['students_id'],))
                payments = cursor.fetchall()
                print("\nMy Payments:")
                for p in payments:
                    print(f"Payment ID: {p['payments_id']}, Amount: {p['amount']}, Status: {p['order_status']}")
            else:
                print("❌ No payment records found.")

        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("❌ Invalid choice, try again.")


# ---------------------- Login ----------------------
def login():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    cursor.execute(
        "SELECT * FROM users_table WHERE username = %s AND Passwor = %s AND is_active = 1",
        (username, password)
    )
    user = cursor.fetchone()

    if user:
        if user["rol"] == "admin":
            print(f"✅ Welcome Admin {user['username']}!")
            admin_menu()
        elif user["rol"] == "student":
            cursor.execute("SELECT * FROM students_table WHERE user_id = %s", (user["user_id"],))
            student = cursor.fetchone()
            if student:
                print(f"✅ Welcome {student['Namee']}!")
                student_menu(user["user_id"])
            else:
                print("❌ No student details found, contact admin.")
    else:
        print("❌ Invalid login credentials")


# ---------------------- Run ----------------------
login()

cursor.close()
conn.close()
