import tkinter as tk
from tkinter import ttk  # สำหรับ Combobox
import pandas as pd
from sqlalchemy import text
import tkinter.messagebox as messagebox
from sqlalchemy import create_engine
import db_connect as dbc
import subprocess

# นำ engine จาก db_connect
engine_db = dbc.engine_test_db
engine_db3 = dbc.engine_test_db3


def countnum(engine):
    """ดึงข้อมูล cntnum จาก database"""
    query = text("SELECT cntnum FROM stocktakeid WHERE status NOT IN ('closed','cancel')")
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error retrieving cntnum: {e}")
        return pd.DataFrame()


def cntnum_detail(engine, cntnum):
    """ดึงรายละเอียดของ cntnum จาก database"""
    query = text("SELECT stcode, cntdate, atype, count_step, status, branch FROM stocktakeid WHERE cntnum = :cntnum")
    try:
        df = pd.read_sql(query, engine, params={"cntnum": cntnum})
        return df
    except Exception as e:
        print(f"Error retrieving cntnum details: {e}")
        return pd.DataFrame()


class Dashboard_b2s(tk.Tk):
    def __init__(self, engine):
        super().__init__()
        self.title("b2s_stocktake")
        self.engine = engine

        # ตั้งค่าหน้าจอให้เต็มจอ
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.configure(bg="#FFFFFF")

        # Header
        self.header = tk.Frame(self, bg="#002FFF", height=50)
        self.header.place(x=300, y=0, width=screen_width)

        self.logout_button = tk.Button(self, text="Logout", command=self.quit_program,
                                       cursor="hand2", bg="#00FFF2", fg="black", font=("Arial", 12, "bold"))
        self.logout_button.place(x=screen_width - 100, y=10, width=80, height=30)

        # Detail Frame (ด้านซ้าย)
        self.detail_frame = tk.Frame(self, bg="#FFFFFF")
        self.detail_frame.place(x=0, y=0, width=300, height=screen_height)

        # พื้นที่แสดงผล Display (ด้านขวา)
        self.display_frame = tk.Frame(self, bg="#DADADA")
        self.display_frame.place(x=300, y=50, width=screen_width - 300, height=screen_height - 55)

        # สร้าง Combobox และปุ่มควบคุม
        self.create_cntnum_combobox()
        self.create_control_buttons()

    def create_cntnum_combobox(self):
        """สร้าง Combobox เพื่อเลือก Count Number"""
        # ดึงข้อมูล cntnum จาก database
        df = countnum(self.engine)

        # แปลง DataFrame เป็น list ของค่า
        cntnum_list = df['cntnum'].tolist() if not df.empty else ["No Data"]

        tk.Label(self.detail_frame, text="Select Count Num:", bg="#FFFFFF", font=("Arial", 12, "bold")).place(x=10, y=20)
        self.cntnum_combobox = ttk.Combobox(self.detail_frame, values=cntnum_list, font=("Arial", 10), state="readonly")
        self.cntnum_combobox.place(x=10, y=60, width=280, height=30)
        self.cntnum_combobox.set("Select CountNum")  # ตั้งค่าเริ่มต้น

        # Bind Event เพื่อแสดง cntnum detail เมื่อลูกค้าเลือกค่า Count Number
        self.cntnum_combobox.bind("<<ComboboxSelected>>", lambda e: self.show_cntnum_detail())

    def create_control_buttons(self):
        """สร้างปุ่มควบคุมด้านซ้าย"""
        self.menu_createcount = tk.Button(self.detail_frame, text="Create", fg="black",
                                          font=("Arial", 12, "bold"), cursor="hand2")
        self.menu_createcount.place(x=10, y=130, width=120, height=40)

        self.menu_download_cntnum = tk.Button(self.detail_frame, text="Download", fg="black",
                                              font=("Arial", 12, "bold"), cursor="hand2", command=self.run_create_master)
        self.menu_download_cntnum.place(x=150, y=130, width=120, height=40)

    def show_cntnum_detail(self):
        """แสดงรายละเอียด cntnum ใน display_frame"""
        cntnum = self.cntnum_combobox.get()
        if not cntnum or cntnum == "Select CountNum":
            # ยังไม่มีการเลือกค่า ไม่ทำอะไร
            return

        # ดึงข้อมูลรายละเอียด
        df_detail = cntnum_detail(self.engine, cntnum)
        if df_detail.empty:
            messagebox.showinfo("Info", f"No details found for Count Number: {cntnum}")
            return

        # ลบข้อมูลเก่าใน display_frame ก่อนแสดงข้อมูลใหม่
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        # แสดงรายละเอียดแต่ละคอลัมน์
        for idx, (col, value) in enumerate(df_detail.iloc[0].items()):
            tk.Label(self.display_frame, text=f"{col}:", bg="#DADADA", font=("Arial", 12, "bold")).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            tk.Label(self.display_frame, text=f"{value}", bg="#DADADA", font=("Arial", 12)).grid(row=idx, column=1, sticky="w", padx=10, pady=5)

    def run_create_master(self):
        """เรียกฟังก์ชัน download เพื่อลงข้อมูล"""
        cntnum = self.cntnum_combobox.get()
        if cntnum == "Select CountNum" or not cntnum:
            messagebox.showerror("Error", "Please select a Count Number before running!")
            return
        try:
            # เรียก subprocess เพื่อรัน b2s_create_master.py พร้อม cntnum ที่เลือก
            subprocess.run(["python", "b2s_create_master.py", cntnum], check=True)
            messagebox.showinfo("Success", f"Stocktake creation process for {cntnum} completed.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run create_db for {cntnum}. Error: {e.stderr.decode('utf-8') if e.stderr else str(e)}.")

    def quit_program(self):
        """ฟังก์ชัน Logout"""
        if not messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            return
        messagebox.showinfo("Logout", "You have been logged out.")
        self.destroy()


def win():
    """เริ่มโปรแกรม Dashboard"""
    dashboard = Dashboard_b2s(engine_db3)
    dashboard.mainloop()


if __name__ == "__main__":
    win()





'''
class B2SProgram(tk.Tk,self):
    super().__init__()
    self.username = username
    self.engine = engine

    # ตั้งค่าหน้าต่างหลัก
    self.title("pst_stocktake")
    self.configure(bg='#f0f0f0')
    screen_width = self.winfo_screenwidth()
    screen_height = self.winfo_screenheight()
    self.geometry(f"{screen_width}x{screen_height}+0+0")

    # สร้าง UI
    self.create_widgets()

def create_widgets(self):
    """สร้างองค์ประกอบ UI"""
    # ข้อความต้อนรับ
    label_welcome = tk.Label(self, text=f"Welcome, {self.username}!", font=("Arial", 24), bg='#f0f0f0')
    label_welcome.pack(pady=20)

    # เพิ่มปุ่ม Refresh Data
    refresh_button = tk.Button(self, text="Refresh Data", font=("Arial", 14), bg='#5cb85c', fg='white',
                                command=self.fetch_data)
    refresh_button.pack(pady=10)

    # ปุ่ม Exit Program
    exit_button = tk.Button(self, text="Exit Program", font=("Arial", 14), bg="#c99290", fg='white',
                                command=self.destroy)
    exit_button.pack(pady=10)

def fetch_data(self):
    """ดึงข้อมูลจากฐานข้อมูล"""
    cntnum = "B2S50019F111225001"
    query = "SELECT * FROM location_master WHERE cntnum = %(cntnum)s"

    try:
        df = pd.read_sql_query(query, con=self.engine, params={"cntnum": cntnum})
        print(f"Data fetched:\n{df.head()}")
        tk.messagebox.showinfo("Data Fetched", f"Fetched {len(df)} rows successfully.")
    except Exception as e:
        print(f"Error fetching data: {e}")
        tk.messagebox.showerror("Error", f"Failed to fetch data.\n{e}")


if __name__ == "__main__":
    # ทดสอบการทำงานของ B2SProgram
    import db_connect as dbc

    # ตั้งค่า username และ engine สำหรับการทดสอบ
    if dbc.engine is None or dbc.username is None:
        print("Database connection is not configured. Please login first.")
    else:
        app = B2SProgram(dbc.username, dbc.engine)
        app.mainloop()
'''