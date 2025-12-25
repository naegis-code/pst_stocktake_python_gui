import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, text
import subprocess
import os

login_path = './login.py'
abs_login_path = os.path.abspath(login_path)
print(f"login.py file path : {abs_login_path}")  # Debugging log

next_python_file = './b2s_program.py'  # ตรวจสอบว่าตรงกับตำแหน่งไฟล์จริง
abs_path = os.path.abspath(next_python_file)  # สร้างเส้นทางแบบ absolute
print(f"b2s_program file path: {abs_path}")  # Debugging log