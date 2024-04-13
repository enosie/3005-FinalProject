-- Create Users table
CREATE TABLE Users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Create Members table
CREATE TABLE Members (
    member_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE,
    fitness_goal VARCHAR(100),
    height FLOAT,
    weight FLOAT
);

-- Create Trainers table
CREATE TABLE Trainers (
    trainer_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE
);

-- Create PersonalTrainingSessions table
CREATE TABLE PersonalTrainingSessions (
    session_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    trainer_id INT REFERENCES Trainers(trainer_id),
    session_date DATE,
    session_time TIME
);

-- Create GroupFitnessClasses table
CREATE TABLE GroupFitnessClasses (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100),
    class_date DATE,
    class_time TIME
);

-- Create RoomBookings table
CREATE TABLE RoomBookings (
    booking_id SERIAL PRIMARY KEY,
    room_name VARCHAR(100),
    booking_date DATE,
    booking_time TIME
);

-- Create EquipmentMaintenance table
CREATE TABLE EquipmentMaintenance (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100),
    maintenance_date DATE,
    maintenance_time TIME
);

-- Create Billing table
CREATE TABLE Billing (
    bill_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Members(member_id),
    amount DECIMAL(10, 2),
    payment_status BOOLEAN
);
