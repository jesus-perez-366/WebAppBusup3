from passlib.hash import sha256_crypt
from bd import conn

#insertar usuario y clave codificada en la tabla de usuarios
clave='Busup_technologies123'
user='rui@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='alex@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()

clave='Busup_technologies123'
user='e.aymerich@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='eva@busup'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='danilo@busup'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='christian@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='o.lujan@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='i.martin@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()

clave='Busup_technologies123'
user='thibaud@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='j.duarte@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_technologies123'
user='christian@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()

clave='Busup_technologies123'
user='r.boada@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_spain123'
user='spain@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_portugal123'
user='portugal@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()

clave='Busup_brazil123'
user='brazil@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_usa123'
user='usa@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


clave='Busup_mexico123'
user='mexico@busup.com'
a=(sha256_crypt.encrypt(clave))
with conn.cursor() as cursor:
    cursor.execute(f"INSERT INTO  dbo.USERS (username, password)  select '{user}','{a}'; commit;")
cursor.close()


