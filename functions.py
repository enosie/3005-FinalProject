import psycopg2
from getpass import getpass

def connect_to_db():
    try:
        conn = psycopg2.connect(host = "localhost", dbname="club_management_system", user="postgres", password ="141203", port = 5432)
        return conn
    except psycopg2.Error as e:
        print("Error connecting to database:", e)

def login_user():
    # Get user input
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Retrieve password from the database
            cursor.execute("""
                SELECT password, role
                FROM Users
                WHERE username = %s
            """, (username,))
            stored_data = cursor.fetchone()
            if stored_data:
                # Compare passwords
                if password == stored_data[0]:
                    print("Login successful.")
                    return username, stored_data[1]
                else:
                    print("Invalid username or password.")
                    return None, None
            else:
                print("User not found.")
                return None, None
        except psycopg2.Error as e:
            print("Error logging in:", e)
        finally:
            cursor.close()
            conn.close()


def register_user():
    # Get user input
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    full_name = input("Enter full name: ")
    email = input("Enter email: ")
    phone_number = input("Enter phone number: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
    fitness_goal = input("Enter fitness goal: ")
    height = float(input("Enter height in cm: "))
    weight = float(input("Enter weight in kg: "))
    role = input("Enter role (member/trainer): ")

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Insert into Users table
            cursor.execute("""
                INSERT INTO Users (username, password, role)
                VALUES (%s, %s, %s)
            """, (username, password, role))
            # Insert into Members or Trainers table based on role
            if role == "member":
                cursor.execute("""
                    INSERT INTO Members (username, full_name, email, phone_number, date_of_birth, fitness_goal, height, weight)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (username, full_name, email, phone_number, date_of_birth, fitness_goal, height, weight))
            elif role == "trainer":
                cursor.execute("""
                    INSERT INTO Trainers (username, full_name, email, phone_number, date_of_birth)
                    VALUES (%s, %s, %s, %s, %s)
                """, (username, full_name, email, phone_number, date_of_birth))
            conn.commit()
            print("User registered successfully.")
        except psycopg2.Error as e:
            print("Error registering user:", e)
        finally:
            cursor.close()
            conn.close()

# Profile management
def update_profile():
    username = input("Enter username: ")

    full_name = input("Enter updated full name: ")
    email = input("Enter updated email: ")
    phone_number = input("Enter updated phone number: ")
    fitness_goal = input("Enter updated fitness goal: ")
    height = float(input("Enter updated height in cm: "))
    weight = float(input("Enter updated weight in kg: "))

    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Members
                SET full_name = %s, email = %s, phone_number = %s, fitness_goal = %s, height = %s, weight = %s
                WHERE username = %s
            """, (full_name, email, phone_number, fitness_goal, height, weight, username))
            conn.commit()
            print("Profile updated successfully.")
        except psycopg2.Error as e:
            print("Error updating profile:", e)
        finally:
            cursor.close()
            conn.close()

# Display user dashboard
def display_dashboard(username):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT full_name, email, phone_number, date_of_birth, fitness_goal, height, weight
                FROM Members
                WHERE username = %s
            """, (username,))
            user_data = cursor.fetchone()
            if user_data:
                print("\n     User Dashboard:")
                print("     Full Name:", user_data[0])
                print("     Email:", user_data[1])
                print("     Phone Number:", user_data[2])
                print("     Date of Birth:", user_data[3])
                print("     Fitness Goal:", user_data[4])
                print("     Height:", user_data[5], "cm")
                print("     Weight:", user_data[6], "kg")
            else:
                print("User not found.")
        except psycopg2.Error as e:
            print("Error retrieving user data:", e)
        finally:
            cursor.close()
            conn.close()

# Scheduling personal training sessions
def schedule_personal_training(username):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT session_id, trainer_id, session_date, session_time
                FROM PersonalTrainingSessions
                WHERE member_id = (SELECT member_id FROM Members WHERE username = %s)
            """, (username,))
            sessions_data = cursor.fetchall()
            print("\nYour Scheduled Personal Training Sessions:")
            for row in sessions_data:
                print("Session ID:", row[0])
                print("Trainer ID:", row[1])
                print("Date:", row[2])
                print("Time:", row[3])
                print()
            
            if sessions_data:
                option = input("Do you want to (R)eschedule or (C)ancel a session? (R/C): ").upper()
                if option == 'R':
                    session_id = int(input("Enter Session ID to reschedule: "))
                    new_date = input("Enter new session date (YYYY-MM-DD): ")
                    new_time = input("Enter new session time (HH:MM): ")
                    cursor.execute("""
                        UPDATE PersonalTrainingSessions
                        SET session_date = %s, session_time = %s
                        WHERE session_id = %s
                    """, (new_date, new_time, session_id))
                    conn.commit()
                    print("Personal training session rescheduled successfully.")
                elif option == 'C':
                    session_id = int(input("Enter Session ID to cancel: "))
                    cursor.execute("""
                        DELETE FROM PersonalTrainingSessions
                        WHERE session_id = %s
                    """, (session_id,))
                    conn.commit()
                    print("Personal training session canceled successfully.")
                else:
                    print("Invalid option.")
            else:
                print("You have no scheduled personal training sessions.")
        except psycopg2.Error as e:
            print("Error scheduling personal training session:", e)
        finally:
            cursor.close()
            conn.close()


# Scheduling group fitness classes
def schedule_group_fitness(username):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT class_id, class_name, class_date, class_time
                FROM GroupFitnessClasses
            """)
            class_data = cursor.fetchall()
            print("\nAvailable Group Fitness Classes:")
            for row in class_data:
                print("Class ID:", row[0])
                print("Class Name:", row[1])
                print("Date:", row[2])
                print("Time:", row[3])
                print()
            
            class_id = int(input("Enter Class ID: "))
            cursor.execute("""
                INSERT INTO PersonalTrainingSessions (member_id, class_id, session_date, session_time)
                VALUES ((SELECT member_id FROM Members WHERE username = %s), %s, CURRENT_DATE, CURRENT_TIME)
            """, (username, class_id))
            conn.commit()
            print("Group fitness class scheduled successfully.")
        except psycopg2.Error as e:
            print("Error scheduling group fitness class:", e)
        finally:
            cursor.close()
            conn.close()

# Administrative staff to manage room bookings
def manage_room_bookings():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT booking_id, room_name, booking_date, booking_time
                FROM RoomBookings
            """)
            bookings_data = cursor.fetchall()
            print("\nRoom Bookings:")
            for row in bookings_data:
                print("Booking ID:", row[0])
                print("Room Name:", row[1])
                print("Date:", row[2])
                print("Time:", row[3])
                print()
            
            option = input("Do you want to (A)dd or (R)emove a room booking? (A/R): ").upper()
            if option == 'A':
                room_name = input("Enter room name: ")
                booking_date = input("Enter booking date (YYYY-MM-DD): ")
                booking_time = input("Enter booking time (HH:MM): ")
                cursor.execute("""
                    INSERT INTO RoomBookings (room_name, booking_date, booking_time)
                    VALUES (%s, %s, %s)
                """, (room_name, booking_date, booking_time))
                conn.commit()
                print("Room booking added successfully.")
            elif option == 'R':
                booking_id = int(input("Enter Booking ID to remove: "))
                cursor.execute("""
                    DELETE FROM RoomBookings
                    WHERE booking_id = %s
                """, (booking_id,))
                conn.commit()
                print("Room booking removed successfully.")
            else:
                print("Invalid option.")
        except psycopg2.Error as e:
            print("Error managing room bookings:", e)
        finally:
            cursor.close()
            conn.close()


# Administrative staff to monitor equipment maintenance
def monitor_equipment_maintenance():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT maintenance_id, equipment_name, maintenance_date, maintenance_time
                FROM EquipmentMaintenance
            """)
            maintenance_data = cursor.fetchall()
            print("\nEquipment Maintenance Records:")
            for row in maintenance_data:
                print("Maintenance ID:", row[0])
                print("Equipment Name:", row[1])
                print("Maintenance Date:", row[2])
                print("Maintenance Time:", row[3])
                print()
        except psycopg2.Error as e:
            print("Error retrieving equipment maintenance records:", e)
        finally:
            cursor.close()
            conn.close()

# Administrative staff to update class schedules
def update_class_schedule():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT class_id, class_name, class_date, class_time
                FROM GroupFitnessClasses
            """)
            class_data = cursor.fetchall()
            print("\nCurrent Group Fitness Class Schedule:")
            for row in class_data:
                print("Class ID:", row[0])
                print("Class Name:", row[1])
                print("Date:", row[2])
                print("Time:", row[3])
                print()
            
            option = input("Do you want to (A)dd or (R)emove a class from the schedule? (A/R): ").upper()
            if option == 'A':
                class_name = input("Enter class name: ")
                class_date = input("Enter class date (YYYY-MM-DD): ")
                class_time = input("Enter class time (HH:MM): ")
                cursor.execute("""
                    INSERT INTO GroupFitnessClasses (class_name, class_date, class_time)
                    VALUES (%s, %s, %s)
                """, (class_name, class_date, class_time))
                conn.commit()
                print("Class added to schedule successfully.")
            elif option == 'R':
                class_id = int(input("Enter Class ID to remove: "))
                cursor.execute("""
                    DELETE FROM GroupFitnessClasses
                    WHERE class_id = %s
                """, (class_id,))
                conn.commit()
                print("Class removed from schedule successfully.")
            else:
                print("Invalid option.")
        except psycopg2.Error as e:
            print("Error updating group fitness class schedule:", e)
        finally:
            cursor.close()
            conn.close()


# Billing and payment processing
def process_billing(username):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT bill_id, amount, payment_status
                FROM Billing
                WHERE member_id = (SELECT member_id FROM Members WHERE username = %s)
            """, (username,))
            billing_data = cursor.fetchall()
            print("\nBilling Information:")
            for row in billing_data:
                print("Bill ID:", row[0])
                print("Amount:", row[1])
                print("Payment Status:", "Paid" if row[2] else "Unpaid")
                print()

            # Prompt for updating payment status
            payment_status = input("Enter payment status (Paid/Unpaid): ").capitalize()
            if payment_status in ['Paid', 'Unpaid']:
                cursor.execute("""
                    UPDATE Billing
                    SET payment_status = %s
                    WHERE member_id = (SELECT member_id FROM Members WHERE username = %s)
                """, (payment_status == 'Paid', username))
                conn.commit()
                print("Payment status updated successfully.")
            else:
                print("Invalid payment status. Please enter 'Paid' or 'Unpaid'.")
        except psycopg2.Error as e:
            print("Error retrieving or updating billing information:", e)
        finally:
            cursor.close()
            conn.close()


# Trainers to manage their schedules
def manage_trainer_schedule(trainer_username):
    # Connect to database
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT session_id, session_date, session_time
                FROM PersonalTrainingSessions
                WHERE trainer_id = (SELECT trainer_id FROM Trainers WHERE username = %s)
            """, (trainer_username,))
            sessions_data = cursor.fetchall()
            print("\nTrainer's Schedule:")
            for row in sessions_data:
                print("Session ID:", row[0])
                print("Date:", row[1])
                print("Time:", row[2])
                print()
        except psycopg2.Error as e:
            print("Error retrieving trainer's schedule:", e)
        finally:
            cursor.close()
            conn.close()

# Trainers to view member profiles
def view_member_profile(member_username):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT full_name, email, phone_number, date_of_birth, fitness_goal, height, weight
                FROM Members
                WHERE username = %s
            """, (member_username,))
            member_data = cursor.fetchone()
            if member_data:
                print("\nMember Profile:")
                print("Full Name:", member_data[0])
                print("Email:", member_data[1])
                print("Phone Number:", member_data[2])
                print("Date of Birth:", member_data[3])
                print("Fitness Goal:", member_data[4])
                print("Height:", member_data[5], "cm")
                print("Weight:", member_data[6], "kg")
            else:
                print("Member not found.")
        except psycopg2.Error as e:
            print("Error retrieving member profile:", e)
        finally:
            cursor.close()
            conn.close()


def main():
    print("Welcome to the Health and Fitness Club Management System!")

    while True:
        # Login or register
        username, role = login_user()
        if not username or not role:
            register_option = input("No existing account found. Do you want to register? (yes/no): ")
            if register_option.lower() == "yes":
                register_user()
            continue  # Retry login or registration if credentials are invalid or registration was declined

        print(f"Welcome, {username}!")

        # Present options based on user role
        if role == "member":
            while True:
                print("\nMember Options:")
                print("1. Update Profile")
                print("2. Display Dashboard")
                print("3. Schedule Personal Training Session")
                print("4. Schedule Group Fitness Class")
                print("5. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":
                    update_profile()
                elif choice == "2":
                    display_dashboard(username)
                elif choice == "3":
                    schedule_personal_training(username)
                elif choice == "4":
                    schedule_group_fitness(username)
                elif choice == "5":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif role == "trainer":
            while True:
                print("\nTrainer Options:")
                print("1. Manage Schedule")
                print("2. View Member Profile")
                print("3. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":
                    manage_trainer_schedule(username)
                elif choice == "2":
                    member_username = input("Enter member's username: ")
                    view_member_profile(member_username)
                elif choice == "3":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif role == "admin":
            while True:
                print("\nAdministrative Assistant Options:")
                print("1. Manage Room Bookings")
                print("2. Monitor Equipment Maintenance")
                print("3. Update Class Schedule")
                print("4. Process Billing")
                print("5. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":
                    manage_room_bookings()
                elif choice == "2":
                    monitor_equipment_maintenance()
                elif choice == "3":
                    update_class_schedule()
                elif choice == "4":
                    username = input("Enter member's username: ")
                    process_billing(username)
                elif choice == "5":
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()