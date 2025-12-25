from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from sqlalchemy import create_engine,text
import time
import sys


username = sys.argv[1]  # ดึง argument ที่ถูกส่งเข้ามา (ค่าที่ 1)

tk = tk.Tk()
tk.title("pst_stocktake")
screen_width = tk.winfo_screenwidth()   # ความกว้างหน้าจอ
screen_height = tk.winfo_screenheight() # ความสูงหน้าจอ
tk.geometry(f"{screen_width}x{screen_height}+0+0")
tk.configure(bg='#f0f0f0')

label_welcome = tk.Label(tk, text=f"Welcome, {username}!", font=("Arial", 24), bg='#f0f0f0')
label_welcome.pack(pady=20)

tk.mainloop()




