import tkinter as tk
from tkinter import ttk,messagebox
import mysql.connector
from tkcalendar import DateEntry

# DATABASE CONNECTION
db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="attendance_db"
)

cursor=db.cursor()

# ---------------- STUDENT WINDOW ---------------- #

def student_window():

    win=tk.Toplevel(root)
    win.title("Student Attendance")
    win.geometry("520x350")

    tk.Label(win,text="Department").grid(row=0,column=0)

    cursor.execute("SELECT dept_name FROM department")
    dept=ttk.Combobox(win,values=[d[0] for d in cursor.fetchall()])
    dept.grid(row=0,column=1)

    tk.Label(win,text="Semester").grid(row=1,column=0)

    cursor.execute("SELECT sem_no FROM semester")
    sem=ttk.Combobox(win,values=[s[0] for s in cursor.fetchall()])
    sem.grid(row=1,column=1)

    tk.Label(win,text="Division").grid(row=2,column=0)
    div=ttk.Combobox(win)
    div.grid(row=2,column=1)

    def load_divisions(event=None):

        cursor.execute("""
        SELECT DISTINCT di.div_name
        FROM student s
        JOIN department d ON s.dept_id=d.dept_id
        JOIN semester se ON s.sem_id=se.sem_id
        JOIN division di ON s.div_id=di.div_id
        WHERE d.dept_name=%s AND se.sem_no=%s
        """,(dept.get(),sem.get()))

        div['values']=[d[0] for d in cursor.fetchall()]

    dept.bind("<<ComboboxSelected>>",load_divisions)
    sem.bind("<<ComboboxSelected>>",load_divisions)

    tk.Label(win,text="Register No").grid(row=3,column=0)
    reg_entry=tk.Entry(win)
    reg_entry.grid(row=3,column=1)

    msg=tk.Label(win,text="",fg="red")
    msg.grid(row=5,column=1)

    def check():

        reg=reg_entry.get()

        cursor.execute("SELECT name FROM student WHERE reg_no=%s",(reg,))
        student=cursor.fetchone()

        if not student:
            msg.config(text="Invalid Register Number")
            return

        name=student[0]

        query="""
        SELECT subject.name,faculty.name,
        (SUM(CASE WHEN attendance.status='present' THEN 1 ELSE 0 END)
/COUNT(attendance.status))*100
        FROM attendance
        JOIN subject ON attendance.sub_id=subject.sub_id
        JOIN faculty ON subject.fac_id=faculty.fac_id
        WHERE attendance.reg_no=%s
        GROUP BY subject.sub_id
        """

        cursor.execute(query,(reg,))
        rows=cursor.fetchall()

        result=tk.Toplevel(win)
        result.title("Attendance Result")
        result.geometry("600x320")

        tk.Label(result,text=f"Student : {name}",
        font=("Arial",12,"bold")).pack()

        tk.Label(result,text=f"Register No : {reg}").pack()

        cols=("Subject","Faculty","Percentage","Status")

        table=ttk.Treeview(result,columns=cols,show="headings")

        for c in cols:
            table.heading(c,text=c)

        table.pack(fill="both",expand=True)

        table.tag_configure("under",background="lightcoral")

        for r in rows:

            percent=float(r[2])

            if percent<75:
                table.insert("",tk.END,
                values=(r[0],r[1],str(round(percent,2))+"%","UNDER"),
                tags=("under",))
            else:
                table.insert("",tk.END,
                values=(r[0],r[1],str(round(percent,2))+"%","OK"))

    tk.Button(win,text="Check Attendance",command=check).grid(row=4,column=1,pady=10)


# ---------------- FACULTY LOGIN ---------------- #

def faculty_login():

    win = tk.Toplevel(root)
    win.title("Faculty Login")
    win.geometry("400x250")

    tk.Label(win,text="Faculty Login",
    font=("Arial",16,"bold")).pack(pady=20)

    tk.Label(win,text="Faculty ID").pack()

    fid_entry=tk.Entry(win)
    fid_entry.pack()

    msg=tk.Label(win,text="",fg="red")
    msg.pack()

    def check():

        fid=fid_entry.get()

        cursor.execute("SELECT * FROM faculty WHERE fac_id=%s",(fid,))
        if cursor.fetchone():
            win.destroy()
            faculty_menu(fid)
        else:
            msg.config(text="Invalid Faculty ID")

    tk.Button(win,text="Login",command=check).pack(pady=10)


# ---------------- FACULTY MENU ---------------- #

def faculty_menu(fid):

    menu=tk.Toplevel(root)
    menu.title("Faculty Panel")
    menu.geometry("300x200")

    tk.Label(menu,text="Faculty Panel",
    font=("Arial",14,"bold")).pack(pady=20)

    tk.Button(menu,text="Update Attendance",
    width=20,
    command=lambda: faculty_window(fid)).pack(pady=10)

    tk.Button(menu,text="View Attendance %",
    width=20,
    command=lambda: faculty_report(fid)).pack(pady=10)


# ---------------- FACULTY WINDOW ---------------- #

def faculty_window(fid):

    win=tk.Toplevel(root)
    win.title("Attendance Panel")
    win.geometry("750x520")

    tk.Label(win,text="Subject").grid(row=0,column=0)

    cursor.execute("SELECT name FROM subject WHERE fac_id=%s",(fid,))
    sub=ttk.Combobox(win,values=[s[0] for s in cursor.fetchall()])
    sub.grid(row=0,column=1)

    tk.Label(win,text="Date").grid(row=1,column=0)

    date_picker=DateEntry(win,date_pattern="yyyy-mm-dd")
    date_picker.grid(row=1,column=1)

    table=ttk.Treeview(win,columns=("RegNo","Name","Status"),show="headings")
    table.heading("RegNo",text="Reg No")
    table.heading("Name",text="Name")
    table.heading("Status",text="Status")
    table.place(x=50,y=150,width=650,height=250)

    status_dict={}

    def load_students():

        table.delete(*table.get_children())

        cursor.execute("SELECT reg_no,name FROM student")
        rows=cursor.fetchall()

        for r in rows:
            table.insert("",tk.END,values=(r[0],r[1],"present"))
            status_dict[r[0]]="present"

    tk.Button(win,text="Load Students",
    command=load_students).grid(row=2,column=1,pady=10)

    def toggle(event):

        item=table.selection()[0]
        reg=table.item(item)["values"][0]

        status_dict[reg]="absent" if status_dict[reg]=="present" else "present"

        table.item(item,values=(reg,
        table.item(item)["values"][1],
        status_dict[reg]))

    table.bind("<Double-1>",toggle)

    def submit():

        subject=sub.get()

        if subject=="":
            messagebox.showerror("Error","Select Subject")
            return

        cursor.execute("SELECT sub_id FROM subject WHERE name=%s",(subject,))
        data=cursor.fetchone()

        if not data:
            messagebox.showerror("Error","Invalid Subject")
            return

        sub_id=data[0]
        date=date_picker.get()

        for reg in status_dict:
            cursor.execute(
            "INSERT INTO attendance (sub_id,reg_no,attendance_date,status) VALUES(%s,%s,%s,%s)",
            (sub_id,reg,date,status_dict[reg]))

        db.commit()

        messagebox.showinfo("Success","Attendance Saved Successfully")

    tk.Button(win,text="Submit Attendance",
    command=submit).place(x=300,y=430)


# ---------------- FACULTY REPORT ---------------- #

def faculty_report(fid):

    win=tk.Toplevel(root)
    win.title("Attendance Report")
    win.geometry("650x400")

    tk.Label(win,text="Subject").grid(row=0,column=0)

    cursor.execute("SELECT name FROM subject WHERE fac_id=%s",(fid,))
    sub=ttk.Combobox(win,values=[s[0] for s in cursor.fetchall()])
    sub.grid(row=0,column=1)

    table=ttk.Treeview(win,
    columns=("RegNo","Name","Percentage"),
    show="headings")

    table.heading("RegNo",text="Reg No")
    table.heading("Name",text="Name")
    table.heading("Percentage",text="%")

    table.place(x=40,y=150,width=550,height=200)

    def load():

        subject=sub.get()

        cursor.execute("""
        SELECT s.reg_no,s.name,
        (SUM(CASE WHEN a.status='present' THEN 1 ELSE 0 END)/COUNT(a.status))*100
        FROM attendance a
        JOIN student s ON a.reg_no=s.reg_no
        JOIN subject su ON a.sub_id=su.sub_id
        WHERE su.name=%s
        GROUP BY s.reg_no
        """,(subject,))

        table.delete(*table.get_children())

        for r in cursor.fetchall():
            table.insert("",tk.END,
            values=(r[0],r[1],str(round(r[2],2))+"%"))

    tk.Button(win,text="Show Report",command=load).grid(row=1,column=1,pady=10)


# ---------------- MAIN ---------------- #

def login():

    if user.get()=="student":
        student_window()
    elif user.get()=="faculty":
        faculty_login()


root=tk.Tk()
root.title("Attendance System")
root.geometry("400x300")

tk.Label(root,text="ATTENDANCE SYSTEM",
font=("Arial",14,"bold")).pack(pady=20)

user=ttk.Combobox(root,values=["student","faculty"])
user.pack()

tk.Button(root,text="Login",command=login).pack(pady=10)

root.mainloop()