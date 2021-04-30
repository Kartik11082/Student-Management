# Imports
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import requests
import bs4
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

# Data
f_1 = ("Courier", 15, 'bold')
f_2 = ("Courier", 20, 'bold')
main_bg = "#121212"
main_fg = "#EDEDED"
button_bg = "#282923"
button_fg = "#f2f2f2"
label_bg = "#262626"

# Functions

def ifexists(rno):
	conn = sqlite3.connect("student_data.db")
	c = conn.cursor()
	c.execute("SELECT rno from student_data")
	rnos = c.fetchall()
	res = False
	for r in rnos:
		if rno in r:
			res = True
	return res

def chart():
	try:
		mark = []
		name = []
		conn = None
		conn = sqlite3.connect("student_data.db")
		c = conn.cursor()
		c.execute("SELECT name, marks from student_data")
		marks_data = c.fetchall()
		for marks in marks_data:
			name.append(marks[0])
			mark.append(marks[1])
		plt.bar(name, mark, linewidth=4, color="teal")
		plt.xlabel("Names")
		plt.ylabel("Marks")
		plt.title("Student's Performance")
		plt.show()
	except Exception as e:
		showerror("Failure", e)
	finally:
		if conn is not None:
			conn.close()

def update_data():
	try:
		conn = None
		if (not (entry_rno_u.get()).isdigit()):
			raise Exception("Roll number cannot contain integers")
		r = int(entry_rno_u.get())
		n = entry_name_u.get()
		m = int(entry_marks_u.get())

		if (int(r) < 0) or (not (r)):
			raise Exception("Roll number can't be empty or negative")
		if (len(n) < 2) or (not n.isalpha()):
			raise Exception("Name can't be numeric/ less than 2 characters or contain special characters")
		if (int(m) > 100) or (int(m) < 0):
			raise Exception("Marks should be between 0 and 100")

		conn = sqlite3.connect("student_data.db")
		c = conn.cursor()
		c.execute("UPDATE student_data SET name=?, marks=? WHERE rno=?", (n, m, r))
		if (c.rowcount) > 0:
			showinfo("Success", f"Updated data of Roll number {r}")
			conn.commit()
		else:
			showerror("Not found", f"Record with roll number {r} doesnot exists")
	except Exception as e:
		showerror("Error:", e)
	finally:
		entry_marks_u.delete(0, END)
		entry_rno_u.delete(0, END)
		entry_name_u.delete(0, END)
		if conn is not None:
			conn.close()
		return


def delete_data():
	try:
		conn = None
		rno = int(entry_rno_d.get())
		conn = sqlite3.connect("student_data.db")
		c = conn.cursor()
		sql = "DELETE FROM student_data WHERE rno = %d"
		c.execute(sql % (rno))
		if (c.rowcount) > 0:
			showinfo("Success", f"Deleted data of Roll number {rno}")
			conn.commit()
		else:
			showerror("Not found", f"Record with roll number {rno} doesnot exists")
	except Exception as e:
		showerror("Error", "Only Integer value is expected")
	finally:
		entry_rno_d.delete(0, END)
		if conn is not None:
			conn.close()


def save_data():
	try:
		conn = None
		if (not ((entry_rno_a.get()).isdigit())) or (int(entry_rno_a.get()) < 0) or (not (entry_rno_a.get())):
			raise Exception("Roll number can't be empty/ negative or alphabetic")
		if (len(entry_name_a.get()) < 2) or (not (entry_name_a.get()).isalpha()):
			raise Exception("Name can't be empty/ numeric or less than 2 characters")
		if (not (entry_marks_a.get()).isdigit()) or (int(entry_marks_a.get()) > 100) or (int(entry_marks_a.get()) < 0):
			raise Exception("Marks should be between 0 and 100 and cannot contain special characters")
		rno = int(entry_rno_a.get())
		if (ifexists(rno)):
			raise Exception(f"Data with Roll number {rno} already exists")
		conn = sqlite3.connect("student_data.db")
		c = conn.cursor()
		d = [int(entry_rno_a.get()), entry_name_a.get(), int(entry_marks_a.get())]
		c.execute("INSERT INTO student_data(rno, name, marks) VALUES (?, ?, ?)", d)
		conn.commit()
		showinfo("Success", "Data added sucessfully, you can view it in view tab")
	except Exception as e:
		showerror("Error", e)
	finally:
		entry_rno_a.delete(0, END)
		entry_name_a.delete(0, END)
		entry_marks_a.delete(0, END)
		if conn is not None:
			conn.close()

def view_data():
	try:
		conn = None
		conn = sqlite3.connect("student_data.db")
		c = conn.cursor()
		c.execute("SELECT * FROM student_data")
		data = c.fetchall()
		view_text_v.config(state=NORMAL)
		view_text_v.delete(1.0, END)
		info = ""
		for d in data:
			info = " Roll number: "+str(d[0])+" |  Name: "+str(d[1])+" |  Marks: "+str(d[2])+"\n"
			view_text_v.insert(INSERT, info)
		view_text_v.config(state=DISABLED)
	except Exception as e:
		showerror("Error", e)
	finally:
		if conn is not None:
			conn.close()


def qotd():
	try:
		wa = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(wa)
		data = bs4.BeautifulSoup(res.text, "html.parser")
		info = data.find('img', {'class':'p-qotd'})
		qotd1, qotd2 = info['alt'].split("-")
		qotd_label_m.config(text=qotd1+"\n\t\t\t- "+qotd2)
	except Exception as e:
		print("Error:",e)
		qotd_label_m.config(text="QOTD not found")

def location():
	try:
		wa = "https://ipinfo.io/"
		res = requests.get(wa)

		data = res.json()

		global city_name_l

		city_name_l = data['city']
		state_name_l =data['region']
		loc_label_m.config(text=city_name_l+", "+state_name_l)
		return
	except Exception as e:
		print("Error ocurred",e)
		loc_label_m.config(text="Location not found")

def temp():
	try:
		city_name_t = city_name_l

		a1 = "https://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q=" + city_name_t
		a3 = "&appid=" + "e863f8eb4b575c9f7081d3befd43903d"
		wa = a1 + a2 + a3
		res = requests.get(wa)

		data = res.json()

		temp = data['main']['temp']
		temp_label_m.config(text="Temperature: "+str(temp))
		return
	except Exception as e:
		print("Error ocurred",e)
		temp_label_m.config(text="Temperature not found")

def main_window_to_add():
	main_window.withdraw()
	add_window.deiconify()

def main_window_to_view():
	main_window.withdraw()
	view_window.deiconify()
	
def main_window_to_update():
	main_window.withdraw()
	update_window.deiconify()

def main_window_to_delete():
	main_window.withdraw()
	delete_window.deiconify()

def to_main(window_name):
	window_name.withdraw()
	main_window.deiconify()

def quit():
	if (askokcancel("Quit", "Do you really want to Quit")):
		main_window.destroy()
	else:
		return

# Functions

# main_window (SMS)
main_window = Tk()
main_window.geometry("800x700+400+50")
main_window.title("Student Manager System")
main_window.config(bg = main_bg)

add_btn_m = Button(main_window, text="Add", font=f_1, width=10, fg = button_fg, bg = button_bg, command = main_window_to_add)
view_btn_m = Button(main_window, text="View", font=f_1, width=10, fg = button_fg, bg = button_bg, command=lambda:[main_window_to_view(), view_data()])
update_btn_m = Button(main_window, text="Update", font=f_1, width=10, fg = button_fg, bg = button_bg, command=main_window_to_update)
delete_btn_m = Button(main_window, text="Delete", font=f_1, width=10, fg = button_fg, bg = button_bg, command=main_window_to_delete)
chart_btn_m = Button(main_window, text="Chart", font=f_1, width=10, fg = button_fg, bg = button_bg, command=chart)
quit_button = Button(main_window, text="Quit", font=f_1, width=5, fg = button_fg, bg = button_bg, command=quit)
loc_label_m = Label(main_window, text="Location", fg = main_fg, bg = main_bg, font=f_1)
temp_label_m = Label(main_window, text="Temp", fg = main_fg, bg = main_bg, font=f_1)
qotd_label_m = Label(main_window, text="QOTD", fg = main_fg, bg = main_bg, font=f_1, wraplength=600)

add_btn_m.place(relx=0.275, rely=0.05, relwidth=0.45, relheight=0.09)
view_btn_m.place(relx=0.275, rely=0.15, relwidth=0.45, relheight=0.09)
update_btn_m.place(relx=0.275, rely=0.25, relwidth=0.45, relheight=0.09)
delete_btn_m.place(relx=0.275, rely=0.35, relwidth=0.45, relheight=0.09)
chart_btn_m.place(relx=0.275, rely=0.45, relwidth=0.45, relheight=0.09)
quit_button.place(relx=0.525, rely=0.56, relwidth=0.2, relheight=0.05)
loc_label_m.place(relx=0.080, rely=0.7, relwidth=0.45, relheight=0.09)
temp_label_m.place(relx=0.55, rely=0.7, relwidth=0.35, relheight=0.09)
qotd_label_m.place(relx=0.06, rely=0.8, relwidth=0.9, relheight=0.2)

location()
temp()
qotd()
# main_window (SMS)

# Add Student
add_window = Toplevel(main_window)
add_window.geometry("800x700+400+50")
add_window.title("Add Student")
add_window.withdraw()
add_window.config(bg = main_bg)

label_rno_a = Label(add_window, text="Enter Roll number", font=f_2, fg = main_fg, bg = main_bg)
label_name_a = Label(add_window, text="Enter Name", font=f_2, fg = main_fg, bg = main_bg)
label_marks_a = Label(add_window, text="Enter Marks", font=f_2, fg = main_fg, bg = main_bg)
entry_rno_a = Entry(add_window, font=f_1)
entry_name_a = Entry(add_window, font=f_1)
entry_marks_a = Entry(add_window, font=f_1)
save_btn_a = Button(add_window, text="Save", font=f_1, fg = button_fg, bg = button_bg, command=save_data)
add_back_btn_a = Button(add_window, text="Back", font=f_1, fg = button_fg, bg = button_bg, command=lambda:[to_main(add_window)])

label_rno_a.place(relx=0.275, rely=0.01, relwidth=0.45, relheight=0.06)
entry_rno_a.place(relx=0.275, rely=0.1, relwidth=0.45, relheight=0.06)
label_name_a.place(relx=0.275, rely=0.25, relwidth=0.45, relheight=0.06)
entry_name_a.place(relx=0.275, rely=0.35, relwidth=0.45, relheight=0.06)
label_marks_a.place(relx=0.275, rely=0.55, relwidth=0.45, relheight=0.06)
entry_marks_a.place(relx=0.275, rely=0.65, relwidth=0.45, relheight=0.06)
save_btn_a.place(relx=0.28, rely=0.78, relwidth=0.45, relheight=0.06)
add_back_btn_a.place(relx=0.28, rely=0.85, relwidth=0.45, relheight=0.06)

entry_rno_a.focus()
# Add Student

# View Student
view_window = Toplevel(main_window)
view_window.geometry("800x700+400+50")
view_window.title("View Student")
view_window.withdraw()
view_window.config(bg = main_bg)

view_text_v = ScrolledText(view_window, width=60, height=22, font=f_1)
view_back_btn_v = Button(view_window, text="Back", font=f_1, fg = button_fg, bg = button_bg, command=lambda:[to_main(view_window)])

view_text_v.pack(pady = 10)
view_back_btn_v.place(relx=0.35, rely=0.85, relwidth=0.3, relheight=0.09)
# View Student

# Update Student
update_window = Toplevel(main_window)
update_window.geometry("800x700+400+50")
update_window.title("Update Student")
update_window.withdraw()
update_window.config(bg = main_bg)

label_rno_u = Label(update_window, text="Enter Roll number\nto be updated", font=f_2, fg = main_fg, bg = main_bg)
label_name_u = Label(update_window, text="Enter Name", font=f_2, fg = main_fg, bg = main_bg)
label_marks_u = Label(update_window, text="Enter Marks", font=f_2, fg = main_fg, bg = main_bg)
entry_rno_u = Entry(update_window, font=f_1)
entry_name_u = Entry(update_window, font=f_1)
entry_marks_u = Entry(update_window, font=f_1)
save_btn_u = Button(update_window, text="Save", font=f_1, fg = button_fg, bg = button_bg, command=update_data)
add_back_btn_u = Button(update_window, text="Back", font=f_1, fg = button_fg, bg = button_bg, command=lambda:[to_main(update_window)])

label_rno_u.place(relx=0.275, rely=0.01, relwidth=0.45, relheight=0.08)
entry_rno_u.place(relx=0.275, rely=0.12, relwidth=0.45, relheight=0.06)
label_name_u.place(relx=0.275, rely=0.25, relwidth=0.45, relheight=0.06)
entry_name_u.place(relx=0.275, rely=0.35, relwidth=0.45, relheight=0.06)
label_marks_u.place(relx=0.275, rely=0.55, relwidth=0.45, relheight=0.06)
entry_marks_u.place(relx=0.275, rely=0.65, relwidth=0.45, relheight=0.06)
save_btn_u.place(relx=0.28, rely=0.78, relwidth=0.45, relheight=0.06)
add_back_btn_u.place(relx=0.28, rely=0.85, relwidth=0.45, relheight=0.06)

entry_rno_u.focus()
# Update Student

# Delete Student
delete_window = Toplevel(main_window)
delete_window.geometry("800x700+400+50")
delete_window.title("Delete Student")
delete_window.withdraw()
delete_window.config(bg = main_bg)

label_rno_d = Label(delete_window, text="Enter Roll number", font=f_2, fg = main_fg, bg = main_bg)
label_rno_d_2 = Label(delete_window, text="of Student\nto be deleted", font=f_2, fg = main_fg, bg = main_bg)
entry_rno_d = Entry(delete_window, font=f_1)
delete_btn_d = Button(delete_window, text="Delete", font=f_1, fg = button_fg, bg = button_bg, command=delete_data)
delete_back_btn_d = Button(delete_window, text="Back", font=f_1, fg = button_fg, bg = button_bg, command=lambda:[to_main(delete_window)])

label_rno_d.place(relx=0.275, rely=0.01, relwidth=0.45, relheight=0.06)
entry_rno_d.place(relx=0.275, rely=0.1, relwidth=0.45, relheight=0.06)
label_rno_d_2.place(relx=0.275, rely=0.25, relwidth=0.45, relheight=0.07)
delete_btn_d.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.06)
delete_back_btn_d.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.06)

entry_rno_d.focus()
# Delete Student

main_window.protocol("WM_DELETE_WINDOW", quit)

main_window.mainloop()
