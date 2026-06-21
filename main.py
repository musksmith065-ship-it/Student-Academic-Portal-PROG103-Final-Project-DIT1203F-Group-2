import tkinter as tk
from tkinter import messagebox
import json
import os

# ==========================================
# 1. COURSE CONSTANTS & DATA CONFIGURATION
# ==========================================
EXCELLENT = "Excellent"
GOOD = "Good"
CREDIT = "Credit"
PASS = "Pass"
FAIL = "Fail"

DATA_FILE = "student_data.json"
student_records = []


# ==========================================
# 2. FILE PERSISTENCE & DATA STORAGE FUNCTIONS
# ==========================================

def load_data_from_file():
    """Reads data from the local JSON file on startup."""
    global student_records
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                student_records = json.load(file)
        except json.JSONDecodeError:
            student_records = []
            messagebox.showwarning("Data Warning", "Data file was corrupted. Initializing empty portal.")
    else:
        student_records = []


def save_data_to_file():
    """Permanently commits the memory records to the local JSON file."""
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(student_records, file, indent=4)
        return True
    except Exception as e:
        messagebox.showerror("Storage Error", f"Could not write data to disk: {str(e)}")
        return False


# ==========================================
# 3. CORE STRUCTURED BACKEND FUNCTIONS
# ==========================================

def calculate_grade(mark):
    if mark >= 80:
        return "A", EXCELLENT
    elif mark >= 70:
        return "B", GOOD
    elif mark >= 60:
        return "C", CREDIT
    elif mark >= 50:
        return "D", PASS
    else:
        return "F", FAIL


def add_student_record(student_id, name, course_mark):
    try:
        mark_float = float(course_mark)
        if mark_float < 0 or mark_float > 100:
            return False, "Error: Marks must be between 0 and 100."

        for student in student_records:
            if student["ID"] == student_id:
                return False, f"Validation Error: A student with ID '{student_id}' already exists."

        letter_grade, classification = calculate_grade(mark_float)

        record = {
            "ID": student_id,
            "Name": name,
            "Mark": mark_float,
            "Grade": letter_grade,
            "Status": classification
        }

        student_records.append(record)

        if save_data_to_file():
            return True, f"Successfully added and saved record for {name}!"
        else:
            return False, "Database save failed."

    except ValueError:
        return False, "Error: Marks must be a valid numerical value."


def generate_summary_report():
    if not student_records:
        return "No records available to summarize."

    total_students = len(student_records)
    total_marks = 0
    passed_students = 0

    for student in student_records:
        total_marks += student["Mark"]
        if student["Grade"] != "F":
            passed_students += 1

    average_mark = total_marks / total_students
    pass_rate = (passed_students / total_students) * 100

    summary = (
        f"--- PORTAL SUMMARY REPORT ---\n"
        f"Total Registered Students: {total_students}\n"
        f"Class Average Mark: {average_mark:.2f}%\n"
        f"Overall Pass Rate: {pass_rate:.1f}%\n"
        f"-----------------------------"
    )
    return summary


# ==========================================
# 4. GUI EVENT HANDLERS
# ==========================================

def handle_add_student():
    s_id = entry_id.get().strip()
    s_name = entry_name.get().strip()
    s_mark = entry_mark.get().strip()

    if not s_id or not s_name or not s_mark:
        messagebox.showerror("Input Error", "All fields are mandatory!")
        return

    success, message = add_student_record(s_id, s_name, s_mark)

    if success:
        messagebox.showinfo("Success", message)
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_mark.delete(0, tk.END)
        refresh_records_display()
    else:
        messagebox.showerror("Validation Error", message)


def refresh_records_display():
    text_display.config(state=tk.NORMAL)
    text_display.delete("1.0", tk.END)

    text_display.insert(tk.END, f"{'ID':<10}{'Name':<20}{'Mark':<10}{'Grade':<10}{'Status':<15}\n")
    text_display.insert(tk.END, "=" * 65 + "\n")

    for s in student_records:
        text_display.insert(
            tk.END,
            f"{s['ID']:<10}{s['Name']:<20}{s['Mark']:<10.1f}{s['Grade']:<10}{s['Status']:<15}\n"
        )
    text_display.config(state=tk.DISABLED)


def handle_show_summary():
    summary_text = generate_summary_report()
    messagebox.showinfo("Portal Summary Metrics", summary_text)


def handle_view_all_records():
    """Opens a separate persistent view window retrieving all data from disk storage."""
    load_data_from_file()  # Ensure we load the freshest state from disk storage

    if not student_records:
        messagebox.showinfo("Empty Storage", "There are no student records stored in the system database.")
        return

    # Generate a sleek secondary cyber layout window frame
    view_window = tk.Toplevel(root)
    view_window.title("System Database - All Stored Records")
    view_window.geometry("550x400")
    view_window.configure(bg="#0d1117")

    tk.Label(
        view_window,
        text="RETRIEVED STUDENT DATABASE",
        font=("Tahoma", 11, "bold"),
        bg="#1f2937",
        fg="#00f0ff",
        pady=8
    ).pack(fill=tk.X)

    display_box = tk.Text(view_window, height=18, width=65, font=("Courier New", 10), bg="#1f2937", fg="#39ff14")
    display_box.pack(padx=15, pady=15)

    display_box.insert(tk.END, f"{'ID':<10}{'Name':<20}{'Mark':<10}{'Grade':<10}{'Status':<15}\n")
    display_box.insert(tk.END, "=" * 60 + "\n")

    for s in student_records:
        display_box.insert(
            tk.END,
            f"{s['ID']:<10}{s['Name']:<20}{s['Mark']:<10.1f}{s['Grade']:<10}{s['Status']:<15}\n"
        )
    display_box.config(state=tk.DISABLED)


def handle_clear_all():
    global student_records
    if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete all stored records?"):
        student_records = []
        save_data_to_file()
        refresh_records_display()


# ==========================================
# 5. GUI LAYOUT DESIGN
# ==========================================

load_data_from_file()

root = tk.Tk()
root.title("Student Academic Portal - SDG 4 Quality Education")
root.geometry("680x560")  # Expanded size to distribute buttons comfortably on a single row
root.configure(bg="#0d1117")

# --- Title Header Panel ---
label_title = tk.Label(
    root,
    text="STUDENT ACADEMIC PORTAL",
    font=("Tahoma", 14, "bold"),
    bg="#1f2937",
    fg="#00f0ff",
    pady=10
)
label_title.pack(fill=tk.X)

# --- Input Fields Frame ---
frame_inputs = tk.LabelFrame(
    root,
    text=" Student Record Input ",
    font=("Tahoma", 10, "bold"),
    bg="#0d1117",
    fg="#00f0ff",
    padx=15,
    pady=5
)
frame_inputs.pack(padx=20, pady=15, fill=tk.X)

# Student ID Row
tk.Label(frame_inputs, text="Student ID:", font=("Tahoma", 10, "bold"), bg="#0d1117", fg="#00f0ff").grid(row=0,
                                                                                                         column=0,
                                                                                                         sticky=tk.W,
                                                                                                         pady=5)
entry_id = tk.Entry(frame_inputs, font=("Tahoma", 10), bg="#1f2937", fg="white", insertbackground="white", width=35)
entry_id.grid(row=0, column=1, pady=5, padx=10)

# Student Name Row
tk.Label(frame_inputs, text="Full Name:", font=("Tahoma", 10, "bold"), bg="#0d1117", fg="#00f0ff").grid(row=1, column=0,
                                                                                                        sticky=tk.W,
                                                                                                        pady=5)
entry_name = tk.Entry(frame_inputs, font=("Tahoma", 10), bg="#1f2937", fg="white", insertbackground="white", width=35)
entry_name.grid(row=1, column=1, pady=5, padx=10)

# Student Course Mark Row
tk.Label(frame_inputs, text="Course Mark (%):", font=("Tahoma", 10, "bold"), bg="#0d1117", fg="#00f0ff").grid(row=2,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=5)
entry_mark = tk.Entry(frame_inputs, font=("Tahoma", 10), bg="#1f2937", fg="white", insertbackground="white", width=35)
entry_mark.grid(row=2, column=1, pady=5, padx=10)

# --- Control Buttons Frame ---
frame_buttons = tk.Frame(root, bg="#0d1117")
frame_buttons.pack(pady=5)

btn_add = tk.Button(frame_buttons, text="Add Student", font=("Tahoma", 10, "bold"), bg="#059669", fg="white",
                    activebackground="#34d399", padx=10, command=handle_add_student)
btn_add.grid(row=0, column=0, padx=4)

btn_view = tk.Button(frame_buttons, text="View All Records", font=("Tahoma", 10, "bold"), bg="#8b5cf6", fg="white",
                     activebackground="#a78bfa", padx=10, command=handle_view_all_records)
btn_view.grid(row=0, column=1, padx=4)

btn_summary = tk.Button(frame_buttons, text="Generate Summary", font=("Tahoma", 10, "bold"), bg="#2563eb", fg="white",
                        activebackground="#60a5fa", padx=10, command=handle_show_summary)
btn_summary.grid(row=0, column=2, padx=4)

btn_clear = tk.Button(frame_buttons, text="Clear Data", font=("Tahoma", 10, "bold"), bg="#d97706", fg="white",
                      activebackground="#fbbf24", padx=10, command=handle_clear_all)
btn_clear.grid(row=0, column=3, padx=4)

btn_exit = tk.Button(frame_buttons, text="Exit", font=("Tahoma", 10, "bold"), bg="#dc2626", fg="white",
                     activebackground="#f87171", padx=15, command=root.quit)
btn_exit.grid(row=0, column=4, padx=4)

# --- Output Display Area ---
label_records = tk.Label(root, text="Registered Records Listing:", font=("Tahoma", 10, "bold"), bg="#0d1117",
                         fg="#00f0ff")
# noinspection PyTypeChecker
label_records.pack(anchor=tk.W, padx=20, pady=(10, 2))

# noinspection PyTypeChecker
text_display = tk.Text(root, height=12, width=78, font=("Courier New", 10), bg="#1f2937", fg="#39ff14",
                       state=tk.DISABLED)
text_display.pack(padx=20, pady=5)

refresh_records_display()

root.mainloop()
