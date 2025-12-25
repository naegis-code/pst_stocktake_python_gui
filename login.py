import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, text
import subprocess
import os

def exit_program(event=None):
    # ฟังก์ชันปิดโปรแกรมเมื่อกด ESC
    root.destroy()

def login():
    if not entry_user.get() or not entry_pass.get():
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    if not selected_program.get() or selected_program.get() == "Select Program":
        messagebox.showwarning("Input Error", "Please select a program.")
        return

    username = entry_user.get()
    password = entry_pass.get()
    host = '103.22.182.82'
    port = '5432'
    database = 'pstdb3'

    engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        # แสดงข้อความสำเร็จ
        messagebox.showinfo("Login Successful", f"Welcome to pst_stocktake program: {selected_program.get()}")

        # เปิดโปรแกรมที่เกี่ยวข้องโดยใช้ subprocess และส่งค่า username ไปยังไฟล์ถัดไป
        next_python_file = selected_program.get()[:3].lower() + "_program.py"
        next_python_file = './' + next_python_file  # ไฟล์อยู่ในไดเรกทอรีเดียวกัน

        if os.path.exists(next_python_file):  # ตรวจสอบว่าไฟล์มีอยู่จริง
            root.destroy()
            subprocess.run(["python", next_python_file, username], check=True)
        else:
            messagebox.showerror("File Error", f"Program file '{next_python_file}' not found.")
    except Exception as e:
        messagebox.showerror("Login Failed", f"Invalid username or password. Error: {e}")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("pst_stocktake")

# ดึงขนาดหน้าจอ
screen_width = root.winfo_screenwidth()   # ความกว้างหน้าจอ
screen_height = root.winfo_screenheight() # ความสูงหน้าจอ

# ตั้งค่า geometry ให้เต็มหน้าจอ
root.geometry(f"{screen_width}x{screen_height}+0+0")

# ตรวจจับปุ่ม ESC เพื่อออกจากโปรแกรม
root.bind("<Escape>", exit_program)

# ส่วนที่เกี่ยวกับ Login
label_user = tk.Label(root, text="Username:")
label_user.pack(pady=10)
entry_user = tk.Entry(root)
entry_user.focus_set()
entry_user.pack(pady=10)

label_pass = tk.Label(root, text="Password:")
label_pass.pack(pady=10)
entry_pass = tk.Entry(root, show="*")
entry_pass.bind("<Return>", lambda event: login())
entry_pass.pack(pady=10)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

# Dropdown เลือกโปรแกรม
program_list = ["OFM - OfficeMate", "B2S - Book to Stationery", "SSP - SuperSports"]
selected_program = tk.StringVar(value="Select Program")  # ค่าเริ่มต้นคือ 'Select Program'
program_dropdown = tk.OptionMenu(root, selected_program, *program_list)
program_dropdown.pack(pady=10)

# เริ่มโปรแกรม GUI
root.mainloop()