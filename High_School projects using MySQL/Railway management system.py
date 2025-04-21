import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='railway_system1',
            user='root',
            password='####'
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful!")
            return connection
        else:
            print("Failed to connect to MySQL DB.")
            return None
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def fetch_trains():
    connection = create_connection()
    if not connection:
        return
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM trains")
    trains = cursor.fetchall()
    cursor.close()
    connection.close()
    return trains

def view_trains():
    trains = fetch_trains()
    if trains:
        print("\nTrain ID | Train Name | Source | Destination | Departure Time | Arrival Time | Available Seats")
        for train in trains:
            print(f"{train[0]} | {train[1]} | {train[2]} | {train[3]} | {train[4]} | {train[5]} | {train[6]}")
    else:
        print("No trains available.")

def book_ticket():
    connection = create_connection()
    if not connection:
        return
    
    cursor = connection.cursor()

    customer_name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    phone = input("Enter customer phone number: ")
    
    cursor.execute("INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)", (customer_name, email, phone))
    customer_id = cursor.lastrowid

    print("\nAvailable Trains:")
    view_trains()

    train_id = int(input("Enter Train ID to book ticket: "))
    seats = int(input("Enter number of seats to book: "))
    
    cursor.execute("SELECT available_seats FROM trains WHERE train_id = %s", (train_id,))
    available_seats = cursor.fetchone()[0]
    
    if available_seats >= seats:
        cursor.execute("INSERT INTO bookings (customer_id, train_id, seats_booked, booking_date) VALUES (%s, %s, %s, CURDATE())", (customer_id, train_id, seats))
        cursor.execute("UPDATE trains SET available_seats = available_seats - %s WHERE train_id = %s", (seats, train_id))
        
        connection.commit()
        print(f"Booking successful! {seats} seat(s) booked.")
    else:
        print("Sorry, not enough seats available.")
    
    cursor.close()
    connection.close()

def view_bookings():
    connection = create_connection()
    if not connection:
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    print("\nBooking ID | Customer ID | Train ID | Seats Booked | Booking Date")
    for booking in bookings:
        print(f"{booking[0]} | {booking[1]} | {booking[2]} | {booking[3]} | {booking[4]}")

    cursor.close()
    connection.close()

def main():
    while True:
        print("\nRailway Management System")
        print("1. View All Trains")
        print("2. Book a Ticket")
        print("3. View All Bookings")
        print("4. Exit")
        
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            view_trains()
        elif choice == 2:
            book_ticket()
        elif choice == 3:
            view_bookings()
        elif choice == 4:
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
