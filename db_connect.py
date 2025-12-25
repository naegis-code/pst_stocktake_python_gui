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

user_test = 'prthanapat'
pwd_test = '20020015'
host_test = '103.22.182.82'
port_test = '5432'
database_db3 = 'pstdb3'
database_db = 'pstdb'
engine_test_db = create_engine(f"postgresql://{user_test}:{pwd_test}@{host_test}:{port_test}/{database_db}")
engine_test_db3 = create_engine(f"postgresql://{user_test}:{pwd_test}@{host_test}:{port_test}/{database_db3}")