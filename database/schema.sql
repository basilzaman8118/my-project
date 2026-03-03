-- Create database
CREATE DATABASE IF NOT EXISTS hospital_db;
USE hospital_db;

-- Table: departments
CREATE TABLE departments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  location VARCHAR(100)
);

INSERT INTO departments (name, location) VALUES
('Cardiology', 'Building A - 2nd Floor'),
('Neurology', 'Building A - 3rd Floor'),
('Orthopedics', 'Building B - 1st Floor'),
('Pediatrics', 'Building C - Ground Floor'),
('Emergency', 'Building A - Ground Floor'),
('Dentist', 'Building C - Ground Floor');


-- Table: doctors
CREATE TABLE doctors (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  specialization VARCHAR(100),
  department_id INT,
  contact VARCHAR(50),
  email VARCHAR(100),
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

INSERT INTO doctors (name, specialization, department_id, contact, email) VALUES
('Dr. Sarah Lee', 'Cardiologist', 1, '+966500000001', 'sarah.lee@hospital.com'),
('Dr. Ahmed Khan', 'Neurologist', 2, '+966500000002', 'ahmed.khan@hospital.com'),
('Dr. Priya Mehta', 'Orthopedic Surgeon', 3, '+966500000003', 'priya.mehta@hospital.com'),
('Dr. John Smith', 'Pediatrician', 4, '+966500000004', 'john.smith@hospital.com'),
('Dr. Fatima Noor', 'Emergency Physician', 5, '+966500000005', 'fatima.noor@hospital.com'),
('Dr. Basil Zaman', 'Dentist', 6, '+966500000006', 'basil.zaman@hospital.com');

-- Table: patients
CREATE TABLE patients (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age INT,
  gender ENUM('Male', 'Female', 'Other'),
  contact VARCHAR(50),
  address VARCHAR(255),
  admitted_date DATE,
  department_id INT,
  FOREIGN KEY (department_id) REFERENCES departments(id)
);

INSERT INTO patients (name, age, gender, contact, address, admitted_date, department_id) VALUES
('Ali Hassan', 45, 'Male', '+966511223344', 'Riyadh', '2025-10-10', 1),
('Maryam Abdullah', 32, 'Female', '+966522334455', 'Jeddah', '2025-10-12', 2),
('Omar Saleh', 60, 'Male', '+966533445566', 'Dammam', '2025-09-28', 3),
('Sara Ibrahim', 8, 'Female', '+966544556677', 'Medina', '2025-10-01', 4),
('Yusuf Ali', 25, 'Male', '+966555667788', 'Riyadh', '2025-10-20', 5);

-- Table: appointments
CREATE TABLE appointments (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT,
  doctor_id INT,
  appointment_date DATE,
  status ENUM('Scheduled', 'Completed', 'Cancelled'),
  FOREIGN KEY (patient_id) REFERENCES patients(id),
  FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES
(1, 1, '2025-10-11', 'Completed'),
(2, 2, '2025-10-13', 'Scheduled'),
(3, 3, '2025-09-29', 'Completed'),
(4, 4, '2025-10-02', 'Completed'),
(5, 5, '2025-10-21', 'Scheduled');

-- Table: medicines
CREATE TABLE medicines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  quantity INT,
  expiry_date DATE
);

INSERT INTO medicines (name, quantity, expiry_date) VALUES
('Paracetamol', 120, '2026-05-10'),
('Amoxicillin', 80, '2025-12-01'),
('Ibuprofen', 100, '2026-02-20'),
('Insulin', 50, '2025-11-15'),
('Cough Syrup', 40, '2026-03-30');

-- Table: faq
CREATE TABLE faq (
  id INT AUTO_INCREMENT PRIMARY KEY,
  question VARCHAR(255),
  answer TEXT
);

INSERT INTO faq (question, answer) VALUES
('what are visiting hours', 'Visiting hours are from 10 AM to 10 PM daily.'),
('how can I book an appointment', 'You can book an appointment by calling +966500000000 or visiting our reception.'),
('where is the cardiology department', 'The cardiology department is located in Building A, 2nd Floor.'),
('how to contact emergency', 'Call +966500000999 or visit the Emergency department, Building A, Ground Floor.');
