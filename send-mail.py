import mysql.connector
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

currentDate = datetime.date.today()

conn = mysql.connector.connect(host='', user='', password='', database='duang')

cursor = conn.cursor()

sql = "SELECT * FROM spider where publishDate = %s  and title like %s"

cursor.execute(sql, (currentDate, '%课题%'))

result = cursor.fetchall()

conn.commit()

cursor.close()

conn.close()

body = "<div><ul>"

for row in result:
    body += f"<li><span>项目名称: {row[1]}</span><span>项目类型: {row[2]}</span><span>发布日期: {row[3]}</span><span>截止日期: {row[4]}</span><span>联系人: {row[5]}</span><span>网页链接: {row[6]}</span></li>"

body += "</ul></div>"

print(body)

message = MIMEMultipart()
message["From"] = "995401608@qq.com"
message["To"] = "995401608@qq.com"
message["Subject"] = "搜索结果"
message.attach(MIMEText(body, "plain"))

smtp_server = "smtp.qq.com"
smtp_port = 465
smtp_username = "995401608@qq.com"
smtp_password = ""
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_username, smtp_password)

server.send_message(message)
server.quit()
