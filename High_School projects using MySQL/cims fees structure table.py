import mysql.connector as sql
conn = sql.connect(host='localhost', user='root', password='####', database='cims')

if conn.is_connected():
    print("Successfully Connected")
c1 = conn.cursor()
c1.execute('''
    CREATE TABLE course_fees (
        course_name VARCHAR(50) PRIMARY KEY,
        monthly_fee DECIMAL(10, 2)
    )
    ''')

c1.execute("INSERT INTO course_fees (course_name, monthly_fee) VALUES ('Java', 1000.00)")
c1.execute("INSERT INTO course_fees (course_name, monthly_fee) VALUES ('Python', 1200.00)")
c1.execute("INSERT INTO course_fees (course_name, monthly_fee) VALUES ('C', 800.00)")
c1.execute("INSERT INTO course_fees (course_name, monthly_fee) VALUES ('QBasic', 600.00)")
c1.execute("INSERT INTO course_fees (course_name, monthly_fee) VALUES ('HTML', 700.00)")

conn.commit()
print("course_fees table created and sample data inserted")
c1.close()
conn.close()
