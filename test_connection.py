# test_connection.py (Tekrar Güncellenmiş Hali)
import psycopg2
import os

db_name = os.getenv('DB_NAME', 'postgres')
db_user = os.getenv('DB_USER', 'postgres')
db_password = os.getenv('DB_PASSWORD', 'password')
# Host'u 127.0.0.1 olarak tutalım
db_host = os.getenv('DB_HOST', '127.0.0.1') 
db_port = os.getenv('DB_PORT', '5432')

print(f"Attempting to connect to:")
print(f"  Host: {db_host}")
print(f"  Port: {db_port}")
print(f"  DB Name: {db_name}")
print(f"  User: {db_user}")

try:
    # Bağlantı zaman aşımını 10 saniye olarak ayarlayalım
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        connect_timeout=10 
    )
    print("\nConnection successful!") 
    conn.close()
    print("Connection closed.")
except psycopg2.OperationalError as e:
    print(f"\nERROR: Connection failed!")
    # Hatanın detayını farklı şekillerde yazdırmayı deneyelim:
    print(f"Error details (str): {str(e)}") 
    print(f"Error details (repr): {repr(e)}") 
except Exception as e:
    print(f"\nAn unexpected error occurred:")
    print(f"Error details (str): {str(e)}")
    print(f"Error details (repr): {repr(e)}") 