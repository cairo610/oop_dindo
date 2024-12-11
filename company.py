from tkinter import *
import sqlite3

# Function called when edit existing record button is pressed
def edit():
    # Another window is opened
    editor = Tk()
    editor.title('Update Employee Record')
    editor.geometry("500x500")
    editor.config(bg="lightpink")
    
    conn = sqlite3.connect("E:\Final_Dindo\employee.db")
    c = conn.cursor()

    record_id = delete_box.get()  # Get the ID of the record to edit

    # Validate that the ID is a number
    if not record_id.isdigit():
        error_label = Label(editor, text="Please enter a valid ID number.", bg="lightpink", font=("Arial", 12, "bold"))
        error_label.grid(row=0, column=0, columnspan=2)
        return

    # Fetch the record from the database
    c.execute("SELECT * FROM employee WHERE oid=?", (record_id,))
    record = c.fetchone()

    if not record:
        error_label = Label(editor, text="Record not found!", bg="lightpink", font=("Arial", 12, "bold"))
        error_label.grid(row=0, column=0, columnspan=2)
        return

    # Labels and Entry for Edit Record
    Employee_Name_editor = Entry(editor, width=30)
    Employee_Name_editor.grid(row=0, column=1, pady=(10, 0))
    Employee_Name_editor.insert(0, record[0])  # Employee Name

    Employee_Name_label = Label(editor, text="Employee Name", bg="lightpink", font=("Arial", 12, "bold"))
    Employee_Name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")

    # Repeat for other fields...
    Email_editor = Entry(editor, width=30)
    Email_editor.grid(row=1, column=1, pady=(10, 0))
    Email_editor.insert(0, record[1])  # Email
    
    Email_label = Label(editor, text="Email", bg="lightpink", font=("Arial", 12, "bold"))
    Email_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

    Employer_editor = Entry(editor, width=30)
    Employer_editor.grid(row=2, column=1, pady=(10, 0))
    Employer_editor.insert(0, record[2])  # Employer
    
    Employer_label = Label(editor, text="Employer", bg="lightpink", font=("Arial", 12, "bold"))
    Employer_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")

    # Similarly for Age, Position, Contact_number
    Age_editor = Entry(editor, width=30)
    Age_editor.grid(row=3, column=1, pady=(10, 0))
    Age_editor.insert(0, record[3])  # Age
    
    Age_label = Label(editor, text="Age", bg="lightpink", font=("Arial", 12, "bold"))
    Age_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")

    Position_editor = Entry(editor, width=30)
    Position_editor.grid(row=4, column=1, pady=(10, 0))
    Position_editor.insert(0, record[4])  # Position
    
    Position_label = Label(editor, text="Position", bg="lightpink", font=("Arial", 12, "bold"))
    Position_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="e")

    # Labels and Entry for Edit Record
    Contact_number_editor = Entry(editor, width=30)
    Contact_number_editor.grid(row=5, column=1, pady=(10, 0))
    Contact_number_editor.insert(0, record[5])  # Employee Name

    Contact_number_label = Label(editor, text="Contact Number", bg="lightpink", font=("Arial", 12, "bold"))
    Contact_number_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="e")

    
    # Function called when save changes button is pressed
    def save_update():
        updated_Employee_Name = Employee_Name_editor.get()
        updated_Email = Email_editor.get()
        updated_Employer = Employer_editor.get()
        updated_Age = Age_editor.get()
        updated_Position = Position_editor.get()
        updated_Contact_number = Contact_number_editor.get()

        # Execute the update query using the record ID
        c.execute('''UPDATE employee SET
                        Employee_Name = ?, Email = ?, Employer = ?, Age = ?, Position = ?, Contact_number = ?  
                        WHERE oid = ?''', 
                  (updated_Employee_Name, updated_Email, updated_Employer, updated_Age, updated_Position, updated_Contact_number, record_id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Close the editor window after update
        editor.destroy()

        # Refresh the main window to show updated data
        query()

    # Button for save changes
    save_btn = Button(editor, text="Save Changes", command=save_update, bg="lightblue", font=("Arial", 12, "bold"))
    save_btn.grid(row=6, column=0, columnspan=2, pady=20, padx=10, ipadx=104)

    editor.mainloop()


# Function called when add record button is pressed    
def submit():
    conn = sqlite3.connect("E:\Final_Dindo\employee.db")
    c = conn.cursor()

    c.execute("INSERT INTO employee VALUES (:Employee_Name, :Email, :Employer, :Age, :Position, :Contact_number)",
              {
                'Employee_Name': Employee_Name.get(),
                'Email': Email.get(),
                'Employer': Employer.get(),
                'Age': Age.get(),
                'Position': Position.get(),
                'Contact_number': Contact_number.get(),
              })
    
    conn.commit()
    conn.close()

    # Clear the text boxes
    Employee_Name.delete(0, END)
    Email.delete(0, END)
    Employer.delete(0, END)
    Age.delete(0, END)
    Position.delete(0, END)
    Contact_number.delete(0, END)

# Function called when show record button is pressed
def query():
    conn = sqlite3.connect("E:\Final_Dindo\employee.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM employee")
    records = c.fetchall()
    conn.close()

    # Remove previous query display (if any)
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) >= 12:
            widget.grid_forget()

    # Create a Text widget to display the records
    query_text = Text(root, height=20, width=40, wrap=WORD, bg="lightyellow", font=("Arial", 10), state=DISABLED)
    query_text.grid(row=12, column=0, columnspan=2, padx=20, pady=10)

    # Insert records into the Text widget
    query_text.config(state=NORMAL)  # Enable editing temporarily to insert text
    print_records = ""
    for record in records:
        print_records += f"Employee Name: {record[0]}\nEmail: {record[1]}\nEmployer: {record[2]}\nAge: {record[3]}\nPosition: {record[4]}\nContact number: {record[5]}\nEmployee ID: {record[6]}\n\n"
    query_text.insert(END, print_records)
    query_text.config(state=DISABLED)  # Disable editing to make it read-only

# Function called when delete record button is pressed
def delete():
    conn = sqlite3.connect("E:\Final_Dindo\employee.db")
    c = conn.cursor()
    c.execute("DELETE FROM employee WHERE oid=?", (delete_box.get(),))
    conn.commit()

    delete_box.delete(0, END)

    conn.close()

    query()

# Main Window when program is run
root = Tk() 
root.title('Company Database')
root.geometry("400x900")
root.config(bg="lightpink")

# Entry
Employee_Name = Entry(root, width=30)
Employee_Name.grid(row=0, column=1, padx=20)

Email = Entry(root, width=30)
Email.grid(row=1, column=1, padx=20)

Employer = Entry(root, width=30)
Employer.grid(row=2, column=1, padx=20)

Age = Entry(root, width=30)
Age.grid(row=3, column=1, padx=20)

Position = Entry(root, width=30)
Position.grid(row=4, column=1, padx=20)

Contact_number = Entry(root, width=30)
Contact_number.grid(row=5, column=1, padx=20)

# Labels
Employee_Name_label = Label(root, text="Employee Name", bg="lightpink", font=("Arial", 12, "bold"))
Employee_Name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="e")

Email_label = Label(root, text="Email", bg="lightpink", font=("Arial", 12, "bold"))
Email_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="e")

Employer_label = Label(root, text="Employer", bg="lightpink", font=("Arial", 12, "bold"))
Employer_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="e")

Age_label = Label(root, text="Age", bg="lightpink", font=("Arial", 12, "bold"))
Age_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="e")

Position_label = Label(root, text="Position", bg="lightpink", font=("Arial", 12, "bold"))
Position_label.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="e")

Contact_number_label = Label(root, text="Contact Number", bg="lightpink", font=("Arial", 12, "bold"))
Contact_number_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="e")

# Entry and Label for Select ID no. for delete
delete_box = Entry(root, width=30)
delete_box.grid(row=8, column=1, padx=30)

delete_box_label = Label(root, text="Select ID", bg="lightpink", font=("Arial", 12, "bold"))
delete_box_label.grid(row=8, column=0, padx=10, pady=10, sticky="e")

# Buttons for Add Record, Show Record, Delete Record, and Edit Existing Record
submit_btn = Button(root, text="Add Employee", command=submit, bg="lightblue", font=("Arial", 12, "bold"))
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=20)

query_btn = Button(root, text="Show Employee Records", command=query, bg="lightblue", font=("Arial", 12, "bold"))
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=20)

delete_btn = Button(root, text="Delete Employee", command=delete, bg="lightblue", font=("Arial", 12, "bold"))
delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=20)

update_btn = Button(root, text="Edit Employee Record", command=edit, bg="lightblue", font=("Arial", 12, "bold"))
update_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=20)

root.mainloop()
