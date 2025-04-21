import mysql.connector as sql
conn = sql.connect(host='localhost', user='root', passwd='titu12@#', database='cims')

if conn.is_connected():
    print("Successfully Connected")

c1 = conn.cursor()
print("                                          :::::::Computer Institute Management System:::::::")

while True:
    print(" ")
    print("1. Enrolling For A Course")
    print("2. Edit Enrollments (as admin)")
    print("3. Display Details")
    print("4. Exit")

    choice = int(input("Enter the Choice - "))

    if choice == 1:
        try:
            c1.execute("SELECT * FROM course_fees")
            courses = c1.fetchall()
            print("\n                Available Courses and Fees:")
            for course in courses:
                print(f"Course: {course[0]} | Monthly Fee: {course[1]}")

            admno = int(input("Enter the Admission Number: "))
            candidatename = str(input("Enter your name: "))
            course = str(input("Enter the Course: "))

            course_found = False
            for c in courses:
                if c[0].lower() == course.lower():
                    course = c[0]
                    course_found = True
                    fee = c[1]
                    break

            if not course_found:
                print("Course not available, please choose from the listed courses.")
                continue

            SQL_insert = f"insert into cand_details values({admno},'{candidatename}','{course}')"
            c1.execute(SQL_insert)

            months = int(input("Enter the number of months for the course: "))
            total_fee = fee * months
            print(f"\n                                         Total Fee for {months} months: {total_fee} (Monthly Fee: {fee})")

            conn.commit()
            print(" ")
            print(f"                                          You are Enrolled Mr. {candidatename}, Congrats!!!")
            print(f"                                        Your enrollment for {course} course is successful!!!")

        except:
            print("Error occurred: Either name or admission number is invalid. Please re-enter.")

    elif choice == 2:
        try:
            uname = input("Enter Username: ")
            passwd = input("Enter Password: ")
            u_name = 'titu'
            pass_rd = 'ad@8k'

            if (uname == u_name) and (passwd == pass_rd):
                print("                                                      Password Accepted")
                print("1. Delete An Enrollment")
                print("2. Edit Name")
                print("3. Edit Course")
                print(" ")

                option = int(input("Which of the above options would you like to choose? "))

                if option == 1:
                    admno = int(input("Enter the admission number of the candidate to be removed: "))
                    SQL_insert = f"delete from cand_details where adm_no = {admno}"
                    c1.execute(SQL_insert)
                    print("Successfully removed")
                    conn.commit()

                elif option == 2:
                    admno = int(input("Enter the admission number of the candidate whose name is to be changed: "))
                    name = str(input("Enter the desired name: "))
                    SQL_insert = f"update cand_details set candidate_name = '{name}' where adm_no = {admno}"
                    c1.execute(SQL_insert)
                    print("Successfully edited")
                    conn.commit()

                elif option == 3:
                    admno = int(input("Enter the admission number of the candidate whose course is to be changed: "))

                    c1.execute("SELECT course_name FROM course_fees")
                    courses = c1.fetchall()

                    print("\n                Available Courses:")
                    for course in courses:
                        print(f"Course: {course[0]}")

                    course = int(input("\nEnter the new Course: "))
                    course_found = False
                    for c in courses:
                        if c[0].lower() == course.lower():
                            course = c[0]
                            course_found = True
                            break

                    if not course_found:
                        print("Invalid course selected. Please choose from the listed courses.")

                    SQL_insert = f"UPDATE cand_details SET course_select = '{course}' WHERE adm_no = {admno}"
                    c1.execute(SQL_insert)
                    print("Successfully modified")
                    conn.commit()


            else:
                print("                                                 Wrong Username or Password")

        except :
            print("Error occurred: Please re-enter correct details.")

    elif choice == 3:
        try:
            c1.execute("Select * from cand_details ")
            data = c1.fetchall()
            for i in data:
                print("                                                            Candidates Details ")
                print(f"                                                      Admission Number : {i[0]}")
                print(f"                                                      Candidate Name   : {i[1]}")
                print(f"                                                      Course Selected  : {i[2]}")
                print(" ")
                print(" ")

        except :
            print("Error occurred while fetching details.")

    elif choice == 4:
        print('                                                           ~~~Thank You~~~')
        break

c1.close()
conn.close()
