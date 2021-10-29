import sqlite3
from patient import Patient

connection = sqlite3.connect('patient.db')

cursor = connection.cursor()

# Create patient table
#----------------------------------------------
#cursor.execute("""CREATE TABLE patients (
#     patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     fname TEXT,
#     lname TEXT,
#     dob TEXT )
#     """)
# connection.commit()
#----------------------------------------------

# Create exercise table
#----------------------------------------------
# cursor.execute("""CREATE TABLE exercises (
#     exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT
#     )""")
# connection.commit()
#----------------------------------------------

# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'SLR'))
# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'SAQ'))
# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'LAQ'))
# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'STS'))
# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'Pulleys'))
# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'Wrist Flextion'))
# cursor.execute('INSERT INTO exercises VALUES (?,?)', (None,'Rows'))
# connection.commit()
# Workout table
#----------------------------------------------

# cursor.execute("""CREATE TABLE program (
#      program_id INTEGER PRIMARY KEY AUTOINCREMENT,
#      patient_id INTEGER,
#      exercise_id INTEGER,
#      FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
#      FOREIGN KEY(exercise_id) REFERENCES exercises(exercise_id)
#      )""")
# connection.commit()
# #----------------------------------------------


# cursor.execute('DROP TABLE program')


def main():
    option = -1
    while option != 4:
        menu()
        option = int(input('What would you like to do? '))
        if option == 1:
            add_patient()

            
        elif option == 2:
            view_patient()
            
        elif option == 3:
            delete_patient()

# Menu for options
def menu():
    print('-------------------------')
    print('1) Add a Patient\n2) View a patient\n3) Delete a patient\n4) Exit')
    print('-------------------------')
    print()

# Adding patient to the db
def add_patient():
    f_name = input("What is the patient's first name?")
    l_name = input("What is the patient's last name?")
    dob = input("What is the patient's date (MM/YYYY)")

    patient = Patient(f_name, l_name, dob)

    

    cursor.execute("INSERT INTO patients VALUES (?,?,?,?)",(None,patient.fname,patient.lname,patient.dob))
    connection.commit()

def show_patients():
    cursor.execute("SELECT patient_id,fname,lname FROM patients")

    info = cursor.fetchall()

    for patient in info:

        print(f'ID: {patient[0]} -- {patient[1]} {patient[2]}')  

def view_patient():
    show_patients()

    p_id = input('Enter the id of the patient you want to work with:\n')

    cursor.execute(f"SELECT fname FROM patients WHERE patient_id == {p_id} ")
    name = cursor.fetchall()
    print()
    for n in name:
        print(n[0])
        print('______________')
    cursor.execute("""SELECT name
                FROM exercises
                JOIN program
                ON exercises.exercise_id == program.exercise_id
                JOIN patients
                ON program.patient_id == patients.patient_id
                WHERE patients.patient_id == ?
                """, p_id)
    exercises = cursor.fetchall()
    for exercise in exercises:
        print(exercise[0])
    
    add_exercise = input('Would you like to add exercises to the patients program? [yes/no]').lower()
    if add_exercise == 'yes':
        cursor.execute(f"SELECT * FROM exercises")
        exercises = cursor.fetchall()

        for exercise in exercises:
            print(f'{exercise[0]} -- {exercise[1]}')

        while add_exercise != 'done':
            add_exercise = input('Enter the id of the exercise you would like to add:\n')
            if add_exercise == 'done':
                break
            else:
                cursor.execute("INSERT INTO program VALUES (?,?,?)",(None,p_id,add_exercise))
                connection.commit()


    

def delete_patient():
    show_patients()  

    id = input('Enter the id of the patient you want to delete:\n ')
    
    cursor.execute(f"SELECT fname FROM patients WHERE patient_id == {id} ")
    deleted_name = cursor.fetchall()
    for name in deleted_name:
        print(f'{name[0]} has been deleted')

    cursor.execute(f'DELETE FROM patients WHERE patient_id = ?',(id))
    

   
    
    connection.commit()

main()