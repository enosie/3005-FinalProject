-- Insert sample data into Users table
INSERT INTO Users (username, password, role) VALUES
('member1', 'password1', 'member'),
('member2', 'password2', 'member'),
('trainer1', 'password1', 'trainer'),
('trainer2', 'password2', 'trainer'),
('admin', 'admin', 'admin');

-- Insert sample data into Members table
INSERT INTO Members (username, full_name, email, phone_number, date_of_birth, fitness_goal, height, weight) VALUES
('member1', 'John Doe', 'john@example.com', '1234567890', '1990-01-01', 'Lose weight', 175.5, 75.0),
('member2', 'Jane Smith', 'jane@example.com', '9876543210', '1985-05-15', 'Gain muscle', 160.0, 60.0);

-- Insert sample data into Trainers table
INSERT INTO Trainers (username, full_name, email, phone_number, date_of_birth) VALUES
('trainer1', 'Michael Johnson', 'michael@example.com', '1112223333', '1980-10-20'),
('trainer2', 'Emily Davis', 'emily@example.com', '4445556666', '1995-03-12');

-- Insert sample data into PersonalTrainingSessions table
INSERT INTO PersonalTrainingSessions (member_id, trainer_id, session_date, session_time) VALUES
(1, 1, '2024-04-16', '10:00:00'),
(2, 2, '2024-04-18', '14:00:00');

-- Insert sample data into GroupFitnessClasses table
INSERT INTO GroupFitnessClasses (class_name, class_date, class_time) VALUES
('Yoga', '2024-04-15', '08:00:00'),
('Zumba', '2024-04-17', '18:30:00'),
('Pilates', '2024-04-19', '08:00:00'),
('Cycling', '2024-04-22', '17:30:00');

-- Insert sample data into RoomBookings table
INSERT INTO RoomBookings (room_name, booking_date, booking_time) VALUES
('Room 1', '2024-04-20', '10:00:00'),
('Room 2', '2024-04-21', '14:00:00'),
('Room 3', '2024-04-23', '09:00:00'),
('Room 4', '2024-04-24', '13:00:00');

-- Insert sample data into EquipmentMaintenance table
INSERT INTO EquipmentMaintenance (equipment_name, maintenance_date, maintenance_time) VALUES
('Treadmill', '2024-04-25', '09:00:00'),
('Elliptical', '2024-04-27', '11:00:00');

-- Insert sample data into Billing table
INSERT INTO Billing (member_id, amount, payment_status) VALUES
(1, 50.00, TRUE),
(2, 75.00, FALSE);
