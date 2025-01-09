import os
import shutil
import threading
from tkinter import *
from tkinter import filedialog, messagebox
import csv
import pandas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

BACKGROUND_COLOR = "#B1DDC6"

def save_info():
    teacher_name = teacher_entry.get()
    sender_mail = teacher_email_entry.get()
    sender_password = teacher_password_entry.get()
    class_of_study = class_entry.get()
    department = department_entry.get()
    user_info = {
        "teacher_name": teacher_name,
        "sender_mail": sender_mail,
        "sender_password": sender_password,
        "class_of_study": class_of_study,
        "department": department
    }
    try:
        with open("user_info.csv", mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=user_info.keys())
            writer.writeheader()
            writer.writerow(user_info)
        messagebox.showinfo("Saved", "Information saved successfully to CSV!")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving information: {e}")

def upload_excel():
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel Files", "*.xlsx *.xls")]
    )
    if file_path:
        try:
            destination_path = "./uploaded_file.xlsx"
            shutil.copy(file_path, destination_path)
            file_excel_data = pandas.read_excel(destination_path)
            file_excel_data.to_csv("file_csv_data.csv", index=False)
            messagebox.showinfo("Success", "Excel file uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading Excel file: {e}")

def send_email_background():
    try:
        user_data = pandas.read_csv("user_info.csv")
        sender_email = user_data["sender_mail"].iloc[0]
        sender_password = user_data["sender_password"].iloc[0]
        teacher_name = user_data["teacher_name"].iloc[0]
        department = user_data["department"].iloc[0]

        student_data = pandas.read_csv("file_csv_data.csv")

        with open("email_prompt.txt", "r") as file:
            email_body_template = file.read()

        server = smtplib.SMTP("smtp.gmail.com", port=587)
        server.starttls()
        server.login(sender_email, sender_password)

        for _, row in student_data.iterrows():
            student_name = row["Student_Name"]
            parent_name = row["Parents_Name"]
            parent_email = row["Email"]
            attendance = row["Attendance"]
            roll_no = row["Roll_No"]
            start_date = row["Attendance_Start_Date"]
            end_date = row["Attendance_End_Date"]

            email_body = email_body_template.format(
                parent_name=parent_name,
                student_name=student_name,
                department=department,
                roll_no=roll_no,
                attendance=attendance,
                start_date=start_date,
                end_date=end_date,
                teacher_name=teacher_name
            )

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = parent_email
            msg['Subject'] = "Attendance Report"
            msg.attach(MIMEText(email_body, 'plain'))

            server.sendmail(sender_email, parent_email, msg.as_string())

        server.quit()
        messagebox.showinfo("Success", "Emails sent successfully!")
        os.remove("user_info.csv")
        os.remove("uploaded_file.xlsx")
        os.remove("file_csv_data.csv")

    except FileNotFoundError as fnfe:
        messagebox.showerror("Error", f"File not found: {fnfe}")

    except Exception as e:
        messagebox.showerror("Error", f"Error sending emails: {e}")

def send_email_thread():
    threading.Thread(target=send_email_background).start()

window = Tk()
window.title("Email Sender")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

Label(text="Email Sender", font=("Ariel", 30, "italic"), bg=BACKGROUND_COLOR).grid(row=0, column=1, columnspan=2)
Label(text="Teacher's Name: ", bg=BACKGROUND_COLOR).grid(row=1, column=0)
Label(text="Teacher's Email ID: ", bg=BACKGROUND_COLOR).grid(row=2, column=0)
Label(text="Password: ", bg=BACKGROUND_COLOR).grid(row=3, column=0)
Label(text="Class: ", bg=BACKGROUND_COLOR).grid(row=4, column=0)
Label(text="Department: ", bg=BACKGROUND_COLOR).grid(row=5, column=0)
Label(text="Upload Excel Sheet: ", bg=BACKGROUND_COLOR).grid(row=7, column=0)
Label(text="(Note: The Excel sheet must include Roll_No, Student_Name, Parents_Name, Email, Attendance, Attendance_Start_Date, Attendance_End_Date)",
      bg=BACKGROUND_COLOR).grid(row=7, column=2)

teacher_entry = Entry(width=31)
teacher_entry.grid(row=1, column=1)
teacher_email_entry = Entry(width=31)
teacher_email_entry.grid(row=2, column=1)
teacher_password_entry = Entry(width=31, show="*")
teacher_password_entry.grid(row=3, column=1)
class_entry = Entry(width=31)
class_entry.grid(row=4, column=1)
department_entry = Entry(width=31)
department_entry.grid(row=5, column=1)

Button(text="All above information is correct!", command=save_info).grid(row=6, column=1)
Button(text="Upload File", command=upload_excel).grid(row=7, column=1)
Button(padx=10, pady=10, text="Send All Emails", command=send_email_thread).grid(row=8, column=0, columnspan=3)

window.mainloop()
