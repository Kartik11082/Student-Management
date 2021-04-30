import sqlite3

con = None
try:
	r = 4
	conn = sqlite3.connect("student_data.db")
	cursor= conn.cursor()
	# cursor.execute("INSERT INTO student_data(rno, name, marks) VALUES (?, ?, ?)",[3, "Test3", 42])
	# sql = "DELETE FROM student_data WHERE rno = %d"
	# cursor.execute(sql % (r))
	cursor.execute("SELECT * FROM student_data")
	data = cursor.fetchall()
	conn.commit()
	print(data)
except Exception as e:
	print("Failure", e)
finally:
	if con is not None:
		con.close()
