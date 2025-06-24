import mysql.connector
from mysql.connector import Error

# Step 1: Create database if not exists
def create_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sunnybunny.123"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS gamingzone")
        conn.commit()
        conn.close()
    except Error as e:
        print("[Error] Could not create database:", e)

# Step 2: Connect to the `gamingzone` database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sunnybunny.123",
            database="gamingzone"
        )
        return conn
    except Error as e:
        print("[Error] Could not connect to database:", e)
        return None

# Step 3: Create tables if not exists
def create_tables():
    create_database()  # ensure DB exists first
    conn = connect_db()
    if conn is None:
        return
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        type VARCHAR(100),
        charge_per_hour DECIMAL(6,2)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        membership_type ENUM('daily', 'monthly', 'yearly'),
        hours_spent INT DEFAULT 0,
        hours_left INT DEFAULT 0
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gameplays (
        id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT,
        game_id INT,
        hours_played INT,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (game_id) REFERENCES games(id)
    )""")

    conn.commit()
    conn.close()
