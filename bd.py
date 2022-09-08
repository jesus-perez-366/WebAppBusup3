import pyodbc
from cryptography.fernet import Fernet

# Configure Database URI: 
key = b'MTjfzcbVFZt_mCOGYjKo_lGMAeP_Un7-znPgsK_4pJI='
server = "busup.database.windows.net"
bdName = "busup"
user = "busup"
pwdCryp = b'gAAAAABiSw_4xFc3pq99ZaJdO_omEEh9oezL-gnrg5OCWRtZQqm2QdKZdtggtNU7Ehkm3QHIA7Gb_JiRKZ96o3RX6QUO6xcyxA=='
cipher_suite = Fernet(key)
pwdBin =  (cipher_suite.decrypt(pwdCryp))
pwd = bytes(pwdBin).decode("utf-8")
sch='meta'
try:
    conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s"%(server,bdName,user,pwd))
    
except Exception as e:
    print("Error al conectar al origen de datos ",e)


