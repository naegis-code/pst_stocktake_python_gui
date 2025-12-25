from sqlalchemy import create_engine

# ตัวแปรสำหรับเก็บ username และ password
username = None
password = None

# การกำหนด connection database
def configure_connection(user, pwd):
    global username, password
    username = user
    password = pwd

    host = '103.22.182.82'
    port = '5432'
    database = 'pstdb3'

    # สร้าง engine สำหรับใช้เชื่อมต่อกับ PostgreSQL
    return create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")

# เริ่มค่า engine เป็น None จนกว่าจะกำหนดที่ login.py
engine = None