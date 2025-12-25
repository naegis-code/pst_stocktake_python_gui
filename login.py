import tkinter as tk
from tkinter import messagebox
from sqlalchemy import text
import db_connect as dbc
from b2s_program import B2SProgram


def exit_program(event=None):
    """ฟังก์ชันปิดโปรแกรมเมื่อกด ESC"""
    root.destroy()


def login():
    # ตรวจสอบว่า username และ password ถูกกรอก
    if not entry_user.get() or not entry_pass.get():
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return
    if not selected_program.get() or selected_program.get() == "Select Program":
        messagebox.showwarning("Input Error", "Please select a program.")
        return

    username = entry_user.get()
    password = entry_pass.get()

    # สร้าง connection ผ่าน db_connect
    dbc.engine = dbc.configure_connection(username, password)

    try:
        # ทดสอบการเชื่อมต่อฐานข้อมูล
        with dbc.engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        # แสดงข้อความสำเร็จ
        messagebox.showinfo("Login Successful", f"Welcome to pst_stocktake program: {selected_program.get()}")

        # เรียกโปรแกรม Tkinter App ของ B2S
        root.destroy()
        app = B2SProgram(username, dbc.engine)
        app.mainloop()

    except Exception as e:
        messagebox.showerror("Login Failed", f"Invalid username or password. Error: {e}")


# สร้าง GUI ของโปรแกรมหลัก
root = tk.Tk()
root.title("pst_stocktake")

# ตั้งค่า geometry ให้เต็มหน้าจอ
screen_width = 800   # ความกว้างหน้าจอ
screen_height = 600   # ความสูงหน้าจอ
root.geometry(f"{screen_width}x{screen_height}+0+0")

# อยู่ตรงกลางหน้าจอ
# อยู่ตรงกลางหน้าจอ (สำหรับคอมพิวเตอร์)
root.update_idletasks()
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w // 2) - (screen_width // 2)
y = (screen_h // 2) - (screen_height // 2)
root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

# Dropdown สำหรับเลือกโปรแกรม
program_list = ["OFM - OfficeMate", "B2S - Book to Stationery", "SSP - SuperSports"]
selected_program = tk.StringVar(value="Select Program")  # ค่าเริ่มต้นคือ 'Select Program'
program_dropdown = tk.OptionMenu(root, selected_program, *program_list)
program_dropdown.pack(pady=20)

# ป้ายข้อความ Login
label_user = tk.Label(root, text="Username:")
label_user.pack(pady=10)

# ฟิลด์สำหรับกรอก Username
entry_user = tk.Entry(root)
entry_user.focus_set()
entry_user.pack(pady=10)

# ป้ายข้อความ Password
label_pass = tk.Label(root, text="Password:")
label_pass.pack(pady=10)

# ฟิลด์สำหรับกรอก Password
entry_pass = tk.Entry(root, show="*")
entry_pass.bind("<Return>", lambda event: login())
entry_pass.pack(pady=10)

# ปุ่ม Login
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)



# ตรวจจับ ESC เพื่อออกจากโปรแกรม
root.bind("<Escape>", exit_program)

# เริ่มโปรแกรม GUI
root.mainloop()