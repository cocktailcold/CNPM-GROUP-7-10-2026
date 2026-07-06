INSERT INTO Users (userName, password, role, sex, createdDate, status) 
VALUES
('IT00000001', 'Anh1001@', 'Student', 'Male', DATE('now'), 'Active'), -- userID: 1
('IT00000002', 'Linh1002#', 'Student', 'Female', DATE('now'), 'Active'), -- userID: 2
('IT00000003', 'Hung2020&', 'Student', 'Male', DATE('now'), 'Active'), -- userID: 3
('IT00000004', 'Oanh2021%', 'Student', 'Female', DATE('now'), 'Active'), -- userID: 4
('IT00000005', 'Hien&2022!', 'Student', 'Male', DATE('now'), 'Active'), -- userID: 5
('IT00000006', 'Han2023^', 'Student', 'Female', DATE('now'), 'Active'), -- userID: 6
('IT00000007', 'Kien$2024', 'Student', 'Male', DATE('now'), 'Active'), -- userID: 7
('IT00000008', 'Uyen2025@!', 'Student', 'Female', DATE('now'), 'Active'), -- userID: 8
('IT00000009', 'Trung@1010', 'Student', 'Male', DATE('now'), 'Active'), -- userID: 9
('IT00000010', 'Van*1020', 'Student', 'Female', DATE('now'), 'Active'), -- userID: 10
('Admin1', '123456', 'Admin', 'Male', DATE('now'), 'Active');          -- userID: 11

INSERT INTO Admin (userID, name, phone) 
VALUES
(11, 'Admin1', '0123456789'); 

INSERT INTO Student (userID, studentName, phone, email, birthdate) 
VALUES
(1, 'Nguyễn Hoàng Anh', '0987000001', 'anhhn1001@edu.com', '2006-08-12'),
(2, 'Nguyễn Thùy Linh', '0987000002', 'linhth1002@edu.com', '2006-01-21'),
(3, 'Lê Anh Hùng', '0987000003', 'hungal1003@edu.com', '2005-7-10'),
(4, 'Trần Thị Oanh', '0987000004', 'oanhtt1004@edu.com', '2005-09-05'),
(5, 'Nguyễn Đức Hiển', '0987000005', 'hiendn1005@edu.com', '2004-11-01'),
(6, 'Nguyễn Ngọc Hân', '0987000006', 'hannnb1006@edu.com', '2006-02-20'),
(7, 'Đặng Đức Kiên', '0987000007', 'kiendd1007@edu.com', '2006-04-18'),
(8, 'Đỗ Phương Uyên', '0987000008', 'uyenpd1008@edu.com', '2006-08-22'),
(9, 'Bùi Đức Trung', '0987000009', 'trungb1009@edu.com', '2004-06-30'),
(10, 'Ngô Thanh Văn', '0987000010', 'vantn1010@edu.com', '2006-09-17');

INSERT INTO Teacher (teacherName, phone) 
VALUES 
('TS. Nguyễn Hoàng Anh', '0912345689'),   -- teacherID: 1
('ThS. Lê Văn Nhã', '0912345670'),     -- teacherID: 2
('TS. Phạm Thị Huệ', '0912345677'),     -- teacherID: 3
('ThS. Phạm Văn Toàn', '0912345681');  -- teacherID: 4

INSERT INTO Courses (courseName, credit, semester, status, fee) 
VALUES
('Introduction to Programming', 3, '1', 'Active', 4500000.00),     -- courseID: 1
('Data Structures and Algorithms', 3, '2', 'Active', 4800000.00),  -- courseID: 2
('Database Systems', 3, '3', 'Active', 5000000.00),                -- courseID: 3
('Operating Systems', 3, '4', 'Active', 4800000.00),               -- courseID: 4
('Computer Networks', 3, '4', 'Active', 4700000.00),               -- courseID: 5
('Software Engineering', 3, '5', 'Active', 5200000.00);           -- courseID: 6

INSERT INTO hasPrerequisite (courseID, prerequisiteID) 
VALUES
(2, 1), -- DSA <- Intro Program
(3, 2), -- Database <- DSA
(6, 3); -- Software Engineering <- Database

INSERT INTO coursesClass (courseID, teacherID, maxEnroll, currentEnroll) 
VALUES
-- Môn 1 (Intro to Programming) -> 3 lớp
(1, 1, 60, 25),  -- courseClassID: 1 (Lớp 01)
(1, 2, 60, 10),  -- courseClassID: 2 (Lớp 02)
(1, 4, 50, 0),  -- courseClassID: 3 (Lớp 03)

-- Môn 2 (Data Structures and Algorithms) -> 2 lớp
(2, 2, 55, 38),  -- courseClassID: 4 (Lớp 01)
(2, 3, 55, 0),  -- courseClassID: 5 (Lớp 02)

-- Môn 3 (Database Systems) -> 2 lớp
(3, 3, 50, 1),  -- courseClassID: 6 (Lớp 01)
(3, 1, 50, 10),  -- courseClassID: 7 (Lớp 02)

-- Môn 4 (Operating Systems) -> 2 lớp
(4, 4, 40, 27),  -- courseClassID: 8 (Lớp 01)
(4, 2, 40, 19),  -- courseClassID: 9 (Lớp 02)

-- Môn 5 (Computer Networks) -> 2 lớp
(5, 1, 50, 1),  -- courseClassID: 10 (Lớp 01)
(5, 3, 50, 0),  -- courseClassID: 11 (Lớp 02)

-- Môn 6 (Software Engineering) -> 2 lớp
(6, 2, 40, 0),  -- courseClassID: 12 (Lớp 01)
(6, 4, 40, 0);  -- courseClassID: 13 (Lớp 02)

INSERT INTO Enrollment (studentID, courseClassID, enrollDate) 
VALUES
-- MÔN 1: Introduction to Programming 
(1, 1, DATE('now')), -- Sinh viên 1 đăng ký Lớp 1
(2, 1, DATE('now')), -- Sinh viên 2 đăng ký Lớp 1
(3, 2, DATE('now')), -- Sinh viên 3 đăng ký Lớp 2
(4, 2, DATE('now')), -- Sinh viên 4 đăng ký Lớp 2

-- MÔN 2: Data Structures and Algorithms 
(1, 4, DATE('now')), -- Sinh viên 1 đăng ký Lớp 4
(2, 4, DATE('now')), -- Sinh viên 2 đăng ký Lớp 4

-- MÔN 3: Database Systems 
(3, 6, DATE('now')), -- Sinh viên 3 đăng ký Lớp 6
(5, 7, DATE('now')), -- Sinh viên 5 đăng ký Lớp 7

-- MÔN 4: Operating Systems 
(1, 8, DATE('now')), -- Sinh viên 1 đăng ký Lớp 8

-- MÔN 5: Computer Networks 
(2, 10, DATE('now')); -- Sinh viên 2 đăng ký Lớp 10

INSERT INTO Building (buildingName) 
VALUES
('Toa B'), -- buildingID: 1
('Toa C'), -- buildingID: 2
('Toa E'), -- buildingID: 3
('Toa F'); -- buildingID: 4

INSERT INTO Room (buildingID, roomName) 
VALUES
(1, 'B203'), -- roomCode: 1
(3, 'E202'), -- roomCode: 2
(4, 'F302'), -- roomCode: 3
(2, 'C102'), -- roomCode: 4
(2, 'C001'); -- roomCode: 5

INSERT INTO Schedule (courseClassID, roomCode, startDate, endDate, session)
 VALUES
-- Môn 1 (Lớp 1, 2) -> Học Thứ 2
(1, NULL, '2026-03-02', '2026-05-18', 'Thứ 2 (07h00 - 09h30)'), 
(2, NULL, '2026-03-02', '2026-05-18', 'Thứ 2 (09h45 - 12h15)'),

-- Môn 2 (Lớp 3, 4) -> Tách ra Thứ 4 và Thứ 6 khác nhau hoàn toàn
(3, NULL, '2026-03-04', '2026-05-20', 'Thứ 4 (07h00 - 09h30)'), -- Lớp 3 học Thứ 4 (Khai giảng 04/03)
(4, NULL, '2026-03-06', '2026-05-22', 'Thứ 6 (14h00 - 16h30)'), -- Lớp 4 học Thứ 6 (Khai giảng 06/03)

-- Môn 3 (Lớp 5, 6) -> Học Thứ 5
(5, NULL, '2026-03-05', '2026-05-21', 'Thứ 5 (08h00 - 10h30)'), 
(6, NULL, '2026-03-05', '2026-05-21', 'Thứ 5 (14h00 - 16h30)'),

-- Môn 4 (Lớp 7, 8) -> Học Thứ 6
(7, NULL, '2026-04-03', '2026-06-19', 'Thứ 6 (07h00 - 09h30)'), 
(8, NULL, '2026-04-03', '2026-06-19', 'Thứ 6 (09h45 - 12h15)'),

-- Môn 5 (Lớp 9, 10) -> Học Thứ 3 và Thứ 5
(9, NULL, '2026-04-07', '2026-06-23', 'Thứ 3 (07h00 - 09h30)'),  
(10, NULL, '2026-04-02', '2026-06-18', 'Thứ 5 (09h45 - 12h15)'), 

-- Môn 6 (Lớp 11, 12) -> Học Thứ 2 và Thứ 3
(11, NULL, '2026-04-06', '2026-06-22', 'Thứ 2 (14h00 - 16h30)'), 
(12, NULL, '2026-04-07', '2026-06-23', 'Thứ 3 (14h00 - 16h30)');

INSERT INTO studentResult (studentID, courseID, gpa, status) 
VALUES
-- Sinh viên 1
(1, 1, 3.2, 'Pass'),
(1, 2, 3.0, 'Pass'),
-- Sinh viên 2
(2, 1, 3.5, 'Pass'),
(2, 2, 2.9, 'Pass'),
-- Sinh viên 3
(3, 1, 2.8, 'Pass'),
(3, 2, 3.6, 'Pass'),
(3, 3, 2.4, 'Pass'),
(3, 4, 3.2, 'Pass'),
(3, 5, 3.0, 'Pass'),
-- Sinh viên 4
(4, 1, 3.6, 'Pass'),
(4, 2, 3.4, 'Pass'),
(4, 3, 2.7, 'Pass');
