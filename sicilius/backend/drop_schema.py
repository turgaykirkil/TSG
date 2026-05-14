import psycopg2
import os

try:
    conn = psycopg2.connect("postgresql://sicilius:Kr6_vP9_Xz2_Nb7_Qj1_Sm@127.0.0.1:5434/sicilius")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("DROP SCHEMA IF EXISTS app CASCADE;")
    cursor.execute("CREATE SCHEMA app;")
    print("Schema dropped and recreated.")
except Exception as e:
    print(f"Error: {e}")
