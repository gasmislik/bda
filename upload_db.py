import mysql.connector

local = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="edt_examens"
)
local_cursor = local.cursor(dictionary=True)

remote = mysql.connector.connect(
    host="shortline.proxy.rlwy.net",
    user="root",
    password="mtocJNYsziRERDOCwMnndSAsvepYzheL",
    database="railway",
    port=20801,
    connection_timeout=300 
)
remote_cursor = remote.cursor()

tables = ["departements", "formations", "groupes", "professeurs", "lieu_examen", "examens", "etudiant_groupe"]

batch_size = 50 

for table in tables:
    local_cursor.execute(f"SELECT * FROM {table}")
    rows = local_cursor.fetchall()
    
    if not rows:
        continue
    
    columns = rows[0].keys()
    placeholders = ", ".join(["%s"] * len(columns))
    column_names = ", ".join(columns)
    insert_query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
    
    
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i+batch_size]
        remote_cursor.executemany(insert_query, [tuple(r.values()) for r in batch])
    
    print(f"✅ Table {table} uploaded with {len(rows)} rows")

remote.commit()
remote_cursor.close()
remote.close()
local_cursor.close()
local.close()

print("🎉 All tables are now online on Railway!")
