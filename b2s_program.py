import tkinter as tk
import pandas as pd
from sqlalchemy import text


class B2SProgram(tk.Tk):
    def __init__(self, username, engine):
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
        exit_button = tk.Button(self, text="Exit Program", font=("Arial", 14), bg='#d9534f', fg='white',
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