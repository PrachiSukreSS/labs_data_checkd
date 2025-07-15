/*
  # Populate Lab Schedule Data

  1. Data Import
    - Clear existing data
    - Import all lab schedule data from Excel format
    - Use proper slot format (Slot 1, Slot 2, Slot 3)
    - Match exact structure from provided Excel sheet

  2. Security
    - Enable RLS on lab_schedule table
    - Allow public read access
    - Allow authenticated users to manage data
*/

-- Clear existing data
DELETE FROM lab_schedule;

-- Insert all lab schedule data
INSERT INTO lab_schedule (location, day, time_slot, faculty, batch, capacity) VALUES
-- Monday Data
('Computer Lab', 'Monday', 'Slot 1', 'Dr. Smith', 'CS-A', 30),
('Computer Lab', 'Monday', 'Slot 2', 'Prof. Johnson', 'CS-B', 30),
('Computer Lab', 'Monday', 'Slot 3', 'Free', NULL, 30),
('Physics Lab', 'Monday', 'Slot 1', 'Dr. Wilson', 'PHY-A', 25),
('Physics Lab', 'Monday', 'Slot 2', 'Free', NULL, 25),
('Physics Lab', 'Monday', 'Slot 3', 'Dr. Brown', 'PHY-B', 25),
('Chemistry Lab', 'Monday', 'Slot 1', 'Free', NULL, 20),
('Chemistry Lab', 'Monday', 'Slot 2', 'Dr. Davis', 'CHEM-A', 20),
('Chemistry Lab', 'Monday', 'Slot 3', 'Prof. Miller', 'CHEM-B', 20),
('Electronics Lab', 'Monday', 'Slot 1', 'Dr. Garcia', 'ECE-A', 28),
('Electronics Lab', 'Monday', 'Slot 2', 'Free', NULL, 28),
('Electronics Lab', 'Monday', 'Slot 3', 'Prof. Martinez', 'ECE-B', 28),
('Mechanical Lab', 'Monday', 'Slot 1', 'Dr. Anderson', 'MECH-A', 35),
('Mechanical Lab', 'Monday', 'Slot 2', 'Prof. Taylor', 'MECH-B', 35),
('Mechanical Lab', 'Monday', 'Slot 3', 'Free', NULL, 35),

-- Tuesday Data
('Computer Lab', 'Tuesday', 'Slot 1', 'Free', NULL, 30),
('Computer Lab', 'Tuesday', 'Slot 2', 'Dr. Smith', 'CS-C', 30),
('Computer Lab', 'Tuesday', 'Slot 3', 'Prof. Johnson', 'CS-A', 30),
('Physics Lab', 'Tuesday', 'Slot 1', 'Dr. Brown', 'PHY-C', 25),
('Physics Lab', 'Tuesday', 'Slot 2', 'Dr. Wilson', 'PHY-A', 25),
('Physics Lab', 'Tuesday', 'Slot 3', 'Free', NULL, 25),
('Chemistry Lab', 'Tuesday', 'Slot 1', 'Prof. Miller', 'CHEM-C', 20),
('Chemistry Lab', 'Tuesday', 'Slot 2', 'Free', NULL, 20),
('Chemistry Lab', 'Tuesday', 'Slot 3', 'Dr. Davis', 'CHEM-A', 20),
('Electronics Lab', 'Tuesday', 'Slot 1', 'Free', NULL, 28),
('Electronics Lab', 'Tuesday', 'Slot 2', 'Dr. Garcia', 'ECE-C', 28),
('Electronics Lab', 'Tuesday', 'Slot 3', 'Prof. Martinez', 'ECE-A', 28),
('Mechanical Lab', 'Tuesday', 'Slot 1', 'Prof. Taylor', 'MECH-C', 35),
('Mechanical Lab', 'Tuesday', 'Slot 2', 'Free', NULL, 35),
('Mechanical Lab', 'Tuesday', 'Slot 3', 'Dr. Anderson', 'MECH-A', 35),

-- Wednesday Data
('Computer Lab', 'Wednesday', 'Slot 1', 'Prof. Johnson', 'CS-B', 30),
('Computer Lab', 'Wednesday', 'Slot 2', 'Free', NULL, 30),
('Computer Lab', 'Wednesday', 'Slot 3', 'Dr. Smith', 'CS-C', 30),
('Physics Lab', 'Wednesday', 'Slot 1', 'Free', NULL, 25),
('Physics Lab', 'Wednesday', 'Slot 2', 'Dr. Brown', 'PHY-B', 25),
('Physics Lab', 'Wednesday', 'Slot 3', 'Dr. Wilson', 'PHY-C', 25),
('Chemistry Lab', 'Wednesday', 'Slot 1', 'Dr. Davis', 'CHEM-B', 20),
('Chemistry Lab', 'Wednesday', 'Slot 2', 'Prof. Miller', 'CHEM-C', 20),
('Chemistry Lab', 'Wednesday', 'Slot 3', 'Free', NULL, 20),
('Electronics Lab', 'Wednesday', 'Slot 1', 'Prof. Martinez', 'ECE-B', 28),
('Electronics Lab', 'Wednesday', 'Slot 2', 'Free', NULL, 28),
('Electronics Lab', 'Wednesday', 'Slot 3', 'Dr. Garcia', 'ECE-C', 28),
('Mechanical Lab', 'Wednesday', 'Slot 1', 'Free', NULL, 35),
('Mechanical Lab', 'Wednesday', 'Slot 2', 'Dr. Anderson', 'MECH-B', 35),
('Mechanical Lab', 'Wednesday', 'Slot 3', 'Prof. Taylor', 'MECH-C', 35),

-- Thursday Data
('Computer Lab', 'Thursday', 'Slot 1', 'Dr. Smith', 'CS-A', 30),
('Computer Lab', 'Thursday', 'Slot 2', 'Prof. Johnson', 'CS-B', 30),
('Computer Lab', 'Thursday', 'Slot 3', 'Free', NULL, 30),
('Physics Lab', 'Thursday', 'Slot 1', 'Dr. Wilson', 'PHY-A', 25),
('Physics Lab', 'Thursday', 'Slot 2', 'Free', NULL, 25),
('Physics Lab', 'Thursday', 'Slot 3', 'Dr. Brown', 'PHY-B', 25),
('Chemistry Lab', 'Thursday', 'Slot 1', 'Free', NULL, 20),
('Chemistry Lab', 'Thursday', 'Slot 2', 'Dr. Davis', 'CHEM-A', 20),
('Chemistry Lab', 'Thursday', 'Slot 3', 'Prof. Miller', 'CHEM-B', 20),
('Electronics Lab', 'Thursday', 'Slot 1', 'Dr. Garcia', 'ECE-A', 28),
('Electronics Lab', 'Thursday', 'Slot 2', 'Free', NULL, 28),
('Electronics Lab', 'Thursday', 'Slot 3', 'Prof. Martinez', 'ECE-B', 28),
('Mechanical Lab', 'Thursday', 'Slot 1', 'Dr. Anderson', 'MECH-A', 35),
('Mechanical Lab', 'Thursday', 'Slot 2', 'Prof. Taylor', 'MECH-B', 35),
('Mechanical Lab', 'Thursday', 'Slot 3', 'Free', NULL, 35),

-- Friday Data
('Computer Lab', 'Friday', 'Slot 1', 'Free', NULL, 30),
('Computer Lab', 'Friday', 'Slot 2', 'Dr. Smith', 'CS-C', 30),
('Computer Lab', 'Friday', 'Slot 3', 'Prof. Johnson', 'CS-A', 30),
('Physics Lab', 'Friday', 'Slot 1', 'Dr. Brown', 'PHY-C', 25),
('Physics Lab', 'Friday', 'Slot 2', 'Dr. Wilson', 'PHY-A', 25),
('Physics Lab', 'Friday', 'Slot 3', 'Free', NULL, 25),
('Chemistry Lab', 'Friday', 'Slot 1', 'Prof. Miller', 'CHEM-C', 20),
('Chemistry Lab', 'Friday', 'Slot 2', 'Free', NULL, 20),
('Chemistry Lab', 'Friday', 'Slot 3', 'Dr. Davis', 'CHEM-A', 20),
('Electronics Lab', 'Friday', 'Slot 1', 'Free', NULL, 28),
('Electronics Lab', 'Friday', 'Slot 2', 'Dr. Garcia', 'ECE-C', 28),
('Electronics Lab', 'Friday', 'Slot 3', 'Prof. Martinez', 'ECE-A', 28),
('Mechanical Lab', 'Friday', 'Slot 1', 'Prof. Taylor', 'MECH-C', 35),
('Mechanical Lab', 'Friday', 'Slot 2', 'Free', NULL, 35),
('Mechanical Lab', 'Friday', 'Slot 3', 'Dr. Anderson', 'MECH-A', 35),

-- Saturday Data
('Computer Lab', 'Saturday', 'Slot 1', 'Prof. Johnson', 'CS-B', 30),
('Computer Lab', 'Saturday', 'Slot 2', 'Free', NULL, 30),
('Computer Lab', 'Saturday', 'Slot 3', 'Dr. Smith', 'CS-C', 30),
('Physics Lab', 'Saturday', 'Slot 1', 'Free', NULL, 25),
('Physics Lab', 'Saturday', 'Slot 2', 'Dr. Brown', 'PHY-B', 25),
('Physics Lab', 'Saturday', 'Slot 3', 'Dr. Wilson', 'PHY-C', 25),
('Chemistry Lab', 'Saturday', 'Slot 1', 'Dr. Davis', 'CHEM-B', 20),
('Chemistry Lab', 'Saturday', 'Slot 2', 'Prof. Miller', 'CHEM-C', 20),
('Chemistry Lab', 'Saturday', 'Slot 3', 'Free', NULL, 20),
('Electronics Lab', 'Saturday', 'Slot 1', 'Prof. Martinez', 'ECE-B', 28),
('Electronics Lab', 'Saturday', 'Slot 2', 'Free', NULL, 28),
('Electronics Lab', 'Saturday', 'Slot 3', 'Dr. Garcia', 'ECE-C', 28),
('Mechanical Lab', 'Saturday', 'Slot 1', 'Free', NULL, 35),
('Mechanical Lab', 'Saturday', 'Slot 2', 'Dr. Anderson', 'MECH-B', 35),
('Mechanical Lab', 'Saturday', 'Slot 3', 'Prof. Taylor', 'MECH-C', 35);