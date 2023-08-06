import mysql.connector

mydb = mysql.connector.connect(
  host="https://datacentral.org.au/vo/tap",
  user="",
  password="",
  database=""
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM galah_dr2.galahdr2cat WHERE field_id = 32 and rv_synt > 200 and rv_synt < 230")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)