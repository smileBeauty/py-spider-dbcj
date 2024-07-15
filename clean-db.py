import mysql.connector

conn = mysql.connector.connect(host='', user='', password='', database='duang')

cursor = conn.cursor()

sql = "DELETE FROM spider;"

cursor.execute(sql)

conn.commit()

cursor.close()

conn.close()

print('清空数据库表数据成功')
