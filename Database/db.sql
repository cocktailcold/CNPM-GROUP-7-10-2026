
CREATE TABLE Users (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    userName VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    role TEXT CHECK(role IN('Student', 'Admin')),
    sex VARCHAR(10),
    createdDate DATE,
    status TEXT CHECK(status IN('Active', 'Inactive'))
);

CREATE TABLE Admin (
    adminID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INT,
    name VARCHAR(50),
    phone VARCHAR(20),
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

CREATE TABLE Student (
    studentID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INT,
    studentName VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(50) UNIQUE,
    birthdate DATE,
    FOREIGN KEY (userID) REFERENCES Users(userID)
);

CREATE TABLE Teacher (
    teacherID INTEGER PRIMARY KEY AUTOINCREMENT,
    teacherName VARCHAR(50) NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE Courses (
    courseID INTEGER PRIMARY KEY AUTOINCREMENT,
    courseName VARCHAR(50),
    credit INT,
    semester VARCHAR(10),
    status VARCHAR(20), 
    fee DECIMAL(10,2)
);

CREATE TABLE hasPrerequisite (
    courseID INT,
    prerequisiteID INT,
    PRIMARY KEY (courseID, prerequisiteID),
    FOREIGN KEY (courseID) REFERENCES Courses(courseID),
    FOREIGN KEY (prerequisiteID) REFERENCES Courses(courseID)
);

CREATE TABLE coursesClass (
    courseClassID INTEGER PRIMARY KEY AUTOINCREMENT,
    courseID INT,
    teacherID int, 
    maxEnroll INT,
    currentEnroll INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'Open',
    FOREIGN KEY (courseID) REFERENCES Courses(courseID),
    FOREIGN KEY (teacherID) REFERENCES Teacher(teacherID)
);

CREATE TABLE Enrollment (
    enrollID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INT,
    courseClassID INT,
    enrollDate DATE,
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (courseClassID) REFERENCES coursesClass(courseClassID),
    UNIQUE (studentID, courseClassID)
);

CREATE TABLE Building (
    buildingID INTEGER PRIMARY KEY AUTOINCREMENT,
    buildingName VARCHAR(50)
);

CREATE TABLE Room (
    roomCode INTEGER PRIMARY KEY AUTOINCREMENT,
    buildingID INT,
    roomName VARCHAR(10), 
    FOREIGN KEY (buildingID) REFERENCES Building(buildingID)
);

CREATE TABLE Schedule (
    scheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    courseClassID INT,
    roomCode INT,
    startDate DATE,
    endDate DATE,
    session VARCHAR(50), 
    FOREIGN KEY (courseClassID) REFERENCES coursesClass(courseClassID),
    FOREIGN KEY (roomCode) REFERENCES room(roomCode)
);

CREATE TABLE studentResult (
    resultID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INT NOT NULL,
    courseID INT NOT NULL,
    gpa DECIMAL(3,2),
    status TEXT CHECK(status IN ('Pass','Fail')),
    FOREIGN KEY (studentID) REFERENCES Student(studentID),
    FOREIGN KEY (courseID) REFERENCES Courses(courseID),
    UNIQUE (studentID, courseID)
);
