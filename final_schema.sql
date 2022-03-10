-- DROP TABLE IF EXISTS active_courses CASCADE; 
-- DROP TABLE IF EXISTS users CASCADE; 
-- DROP TABLE IF EXISTS all_courses CASCADE; 
-- DROP TABLE IF EXISTS prerequisites CASCADE; 
-- DROP TABLE IF EXISTS grade CASCADE; 
-- DROP TABLE IF EXISTS thesis CASCADE; 
-- DROP TABLE IF EXISTS form1 CASCADE; 
SET FOREIGN_KEY_CHECKS = 0; 
DROP TABLE IF EXISTS users; 
CREATE TABLE users (
    uni_ID   int(8)      not null,
    fname    varchar(30) not null,
    lname    varchar(30) not null,
    address  varchar(30),
    password varchar(30) not null,
    email    varchar(30),
    role_GS_M  int,
    role_GS_P  int,
    role_GSec  int,
    role_F     int,
    role_SA    int,
    role_Alum  int,
    advisor_ID int(15),
    primary key (uni_ID)
    -- CONSTRAINT users_key primary key (uni_ID, transcript_ID)
);
DROP TABLE IF EXISTS all_courses; 
CREATE TABLE all_courses(
    dept_name   varchar(30) not null,
    course_num  int(4)      not null,
    title       varchar(30) not null,
    credit_hrs  int(5)      not null,
    course_ID   int         not null,
    course_info varchar(1000),
    CONSTRAINT all_courses_key primary key (course_ID, course_num)

);
DROP TABLE IF EXISTS active_courses; 
CREATE TABLE active_courses(
    sec_ID	    int         not null,
    semester    varchar(6),
    year	    int(4),
    day		    varchar(9)  not null,
    time	    int(4)      not null,
    course_num	int(4)      not null,
    faculty_ID	int(8),
    gsec_ID	    int(8),
    student_ID	int(8),
    course_ID   int         not null,
    room_cap    int(3),     
    room_loc    varchar(20),
    CONSTRAINT active_courses_key primary key (course_ID, sec_ID, student_ID, semester, year)
   
);
DROP TABLE IF EXISTS prerequisites; 
CREATE TABLE prerequisites (
    course_ID       int,
    course_num      int(4) not null,
    prereq_num1     int(4),
    prereq_num2     int(4),
    department      char(20) not null,
    prereq_ID1      varchar(4),
    prereq_ID2      varchar(4),
    CONSTRAINT prereq_key primary key (course_ID, prereq_ID1, prereq_ID2, department)
    
);
DROP TABLE IF EXISTS grade;
CREATE TABLE grade (
    letter_grade    varchar(2),
    uni_ID          int(8)     not null,
    course_num      int(4)     not null,
    sec_ID          int        not null,
    course_ID       int        not null,
    primary key (uni_ID, course_ID)
);

DROP TABLE IF EXISTS thesis;
CREATE TABLE thesis(
  thesis text(1000000),
  uni_ID int(15),
  decision int (1), 
  is_submitted int(1),
  primary key (uni_ID),
  foreign key (uni_ID) references users(uni_ID)
);
DROP TABLE IF EXISTS Form1; 
CREATE TABLE Form1(
    ID int(15),
    courseNumber int(15), 
    courseTitle varchar(50) not null, 
    primary key(ID,courseNumber, courseTitle),
    foreign key(ID) references users(uni_ID)
); 
INSERT INTO users VALUES(10000000, "system", "admin", null, "seas", null, 0, 0, 0, 0, 1,0, 0);
INSERT INTO users VALUES(12345678, "grad", "student", null, "seas", null, 1, 0, 0, 0, 0,0, 2);
INSERT INTO users VALUES(23232323, "PHD", "Student", null, "seas", null, 0, 1, 0, 0, 0, 0, 3);
INSERT INTO users VALUES(55555550, "Grad", "Secretary", null, "seas", null, 0, 0, 1, 0, 0, 0, 0);

-- creating faculty
INSERT INTO users VALUES(44444441, "Joan", "Rivers", "123 North Street", "seas", "jr@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444442, "John", "Mayer", "55 South St", "seas", "jm@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444443, "Anthony", "Kiedis", "555 Maple", "seas", "ak@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444404, "John", "Frusciante", "32 Birch St", "seas", "jf@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444445, "Kanye", "West", "876 West St", "seas", "kw@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444446, "Neil", "Young", "65 City Dr", "seas", "ny@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444447, "Ryan", "Seacrest", "105 Park Ave", "seas", "rs@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444448, "Derek", "Jeter", "200 East 42 St", "seas", "dj@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(44444449, "Tony", "Hawk", "345 Oak St", "seas", "th@gmail.com", 0, 0, 0, 1, 0, 0, 0);

-- Masters Students For Testing
INSERT INTO users VALUES(88888888, "Billie", "Holiday", null, "seas", null, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO users VALUES(99999999, "Diana", "Krall", null, "seas", null, 1, 0, 0, 0, 0, 0, 0);
INSERT INTO users VALUES(55555555, "Paul", "McCartney", "Abbey Road", "seas", "pm@gmail.com", 1, 0, 0, 0, 0, 0, 98989898);
INSERT INTO users VALUES(66666666, "George", "Harrison", "Penny Lane", "seas", "GH@gmail.com", 1, 0, 0, 0, 0, 0, 91919191);
-- PHD Student for testing
INSERT INTO users VALUES(66667777, "Ringo", "Starr", "Blackbird St", "seas", "RS@gmail.com", 0, 1, 0, 0, 0, 0, 91919191);
-- Alumni For testing
INSERT INTO users VALUES(77777777, "Eric", "Clapton", "Guitar St", "seas", "EC@gmail.com", 0, 0, 0, 0, 0, 1, 0);

-- Faculty and Advisors
INSERT INTO users VALUES(98989898, "Bhagirath", "Narahari", "1234 Sesame St", "seas", "bnarahari@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(90909090, "Hyeong-Ah", "Choi", "166 Maple St", "seas", "hchoi@gmail.com", 0, 0, 0, 1, 0, 0, 0);
INSERT INTO users VALUES(91919191, "Gabe", "Parmer", "321 H St", "seas", "gparmer@gmail.com", 0, 0, 0, 1, 0, 0, 0);



INSERT INTO all_courses VALUES("CSCI", 6221, "SW Paradigms", 3, 1, "Object-oriented, procedural, functional, and concurrent software design paradigms; design patterns; software life cycle concepts; tadeoffs between compiled and interpreted languages; examples from Java, C, C++ and Perl. Restricted to graduate students.");
INSERT INTO all_courses VALUES("CSCI", 6461, "Computer Architecture", 3, 2, "Number representation, computer arithmetic, digital logic, and circuit design. Computer organization, micro-architecture and processor datapath, assembly and machine language programming. Introduction to memory organization and the hardware–software interface. Implementation of high-level language constructs.");
INSERT INTO all_courses VALUES("CSCI", 6212, "Algorithms", 3, 3, "Core concepts in design and analysis of algorithms, data structures, and problem-solving techniques. Hashing, heaps, trees. Graph algorithms, searching, sorting, graph algorithms, dynamic programming, greedy algorithms, divide and conquer, backtracking. Combinatorial optimization techniques. NP-completeness.");
INSERT INTO all_courses VALUES("CSCI", 6220, "Machine Learning", 3, 4, "Overview of core machine learning techniques: nearest-neighbor, regression, classification, perceptron, kernel methods, support vector machine (SVM), logistic regression, ensemble methods, hidden Markov models (HMM), non-parametrics, online learning, active learning, clustering, feature selection, parameter tuning, and cross-validation.");
INSERT INTO all_courses VALUES("CSCI", 6232, "Networks 1", 3, 5, "Higher-layer protocols and network applications on the Internet, such as session layer, presentation layer, data encryption, directory services and reliable transfer services, telnet, network management, network measurements, e-mail systems, and error reporting.");
INSERT INTO all_courses VALUES("CSCI", 6233, "Networks 2", 3, 6, "Computer networks and open system standards. Network configurations and signals, encoding and modulation, transmission media, connection interfaces, error detection and correction, signal compression, switching, link layer control, ISDN, X.25, frame relay, ATM, and Sonet. Bridges, routers, and routing algorithms. ");
INSERT INTO all_courses VALUES("CSCI", 6241, "Database 1", 3, 7, "Design of relational database systems, relational query languages, normal forms, and design of database applications. Team software development, integration, and testing. Professional code of ethics, intellectual property, privacy, and software copyrights.");
INSERT INTO all_courses VALUES("CSCI", 6242, "Database 2", 3, 8, "Design of relational database systems, relational query languages, normal forms, and design of database applications. Team software development, integration, and testing. Professional code of ethics, intellectual property, privacy, and software copyrights.");
INSERT INTO all_courses VALUES("CSCI", 6246, "Compilers", 3, 9, "This course introduces students to the design and implementation of compilers for programming languages. Specifically, students will learn how to systematically translate modern, high-level, programming languages into efficient, executable machine code.");
INSERT INTO all_courses VALUES("CSCI", 6260, "Multimedia", 3, 10, "This course introduces the basic concepts of programming for multimedia. Students will learn the principles of object-oriented programming and how to create scripts for the manipulation of graphics, audio and text to construct a web-based multimedia presentation.");
INSERT INTO all_courses VALUES("CSCI", 6251, "Cloud Computing", 3, 11, "Cloud application design guidelines and software patterns. Survey of cloud services for scalable secure cloud applications. Trade-offs in cloud application design, container vs virtual machine deployments, and monolithic vs microservice.");
INSERT INTO all_courses VALUES("CSCI", 6254, "SW Engineering", 3, 12, "Programming techniques and software development in one or more programming languages; application development with GUIs, database access, threads, web programming.");
INSERT INTO all_courses VALUES("CSCI", 6262, "Graphics 1", 3, 13, "Graphics primitives; 2D, 3D, and viewing transformations; hierarchical modeling and animation; illumination and shading; texture mapping; shaders; visibility and collision detection; sampling and anti-aliasing; global illumination; projects using OpenGL graphics API.");
INSERT INTO all_courses VALUES("CSCI", 6283, "Security 1", 3, 14, "Risk analysis, cryptography, operating system security, identification and authentication systems, database security.");  
INSERT INTO all_courses VALUES("CSCI", 6284, "Cryptography", 3, 15, "Algorithmic principles of cryptography from Julius Caesar to public key cryptography. Key management problems and solutions. Cryptographic systems and applications.");
INSERT INTO all_courses VALUES("CSCI", 6286, "Network Security", 3, 16, "Security protocols and applications in local, global, and wireless networks; IPSec and packet-level communication security systems; network authentication and key-exchange protocols; intrusion detection systems and firewalls; secure network applications; network worms and denial-of-service attacks.");
INSERT INTO all_courses VALUES("CSCI", 6325, "Algorithms 2", 3, 17, "This course covers the essential information that every serious programmer needs to know about algorithms and data structures, with emphasis on applications and scientific performance analysis of Java implementations. Part I covers elementary data structures, sorting, and searching algorithms. Part II focuses on graph and string processing algorithms.");
INSERT INTO all_courses VALUES("CSCI", 6339, "Embedded Systems", 3, 18, "Development of software for real-time control of physical systems; reliability and fault tolerance, exceptions and exception handling, reliability and concurrent processes, timeouts, deadline scheduling, shared-memory and message-based device drivers.");
INSERT INTO all_courses VALUES("CSCI", 6384, "Cryptography 2", 3, 19, "This course is a continuation of Crypto I and explains the inner workings of public-key systems and cryptographic protocols. Students will learn how to reason about the security of cryptographic constructions and how to apply this knowledge to real-world applications.");
INSERT INTO all_courses VALUES("ECE", 6241, "Communication Theory", 3, 20, "This course presents a top-down approach to communications system design. The course will cover communication theory, algorithms and implementation architectures for essential blocks in modern physical-layer communication systems (coders and decoders, filters, multi-tone modulation, synchronization sub-systems).");
INSERT INTO all_courses VALUES("ECE", 6242, "Information Theory", 2, 21, "Roles, issues, and impacts of computer-based information systems in national and international arenas, focusing on privacy, equity, freedom of speech, intellectual property, and access to personal and governmental information. Professional responsibilities, ethics, and common and best practices in information use.");
INSERT INTO all_courses VALUES("MATH", 6210, "Logic", 2, 22, "This course introduces several formal logics, differing in their expressive power and focus, and discusses some of their uses in computer science. Main themes are how to represent knowledge in these logics, what constitutes a valid argument, and how to prove or disprove, possibly automatically, the validity of a logical statement.");

INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1500, 6221, 44444441, 55555550, 00000000, 1, 50, "Jeter Hall 102");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6461, 98989898, 55555550, 00000000, 2, 75, "Ruth Hall 203");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6212, 90909090, 55555550, 00000000, 3, 75, "Gehrig Hall 504");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6232, 44444446, 55555550, 00000000, 5, 25, "DiMaggio Hall 305");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6233, 44444441, 55555550, 00000000, 6, 100, "Torre Hall 106");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1800, 6242, 44444442, 55555550, 00000000, 8, 75, "Berra Hall 308");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6246, 44444404, 55555550, 00000000, 9, 100, "Posada Hall 420");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6251, 44444449, 55555550, 00000000, 11, 60, "Ruth Hall 510");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1530, 6254, 44444443, 55555550, 00000000, 12, 30, "River Hall 114");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1800, 6260, 44444445, 55555550, 00000000, 10, 50, "Jeter Hall 609");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1800, 6262, 44444449, 55555550, 00000000, 13, 25, "Posada Hall 608");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6283, 44444447, 55555550, 00000000, 14, 80, "Mantle Hall 509");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6284, 44444448, 55555550, 00000000, 15, 40, "Gehrig Hall 116");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1800, 6286, 44444443, 55555550, 00000000, 16, 75, "Ruth Hall 424");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6384, 44444446, 55555550, 00000000, 19, 100, "DiMaggio Hall 810");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6241, 44444404, 55555550, 00000000, 20, 50, "Rivera Hall 708");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6242, 44444448, 55555550, 00000000, 21, 45, "Robinson Hall 318");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1800, 6210, 44444404, 55555550, 00000000, 22, 25, "Berra Hall 516");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1600, 6339, 44444449, 55555550, 00000000, 18, 30, "Posada Hall 810");
-- Course Data for 2014
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Monday", 1500, 6221, 44444441, 55555550, 00000000, 1, 50, "Jeter Hall 102");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Wednesday", 1500, 6212, 90909090, 55555550, 00000000, 3, 75, "Gehrig Hall 504");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Tuesday", 1500, 6461, 98989898, 55555550, 00000000, 2, 75, "Ruth Hall 203");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Monday", 1800, 6232, 44444446, 55555550, 00000000, 5, 25, "DiMaggio Hall 305");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Tuesday", 1800, 6233, 44444441, 55555550, 00000000, 6, 100, "Torre Hall 106");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Monday", 1800, 6241, 44444404, 55555550, 00000000, 20, 50, "Rivera Hall 708");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Thursday", 1800, 6242, 44444442, 55555550, 00000000, 8, 75, "Berra Hall 308");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Tuesday", 1800, 6283, 44444447, 55555550, 00000000, 14, 80, "Mantle Hall 509");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Monday", 1800, 6284, 44444448, 55555550, 00000000, 15, 40, "Gehrig Hall 116");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Wednesday", 1800, 6286, 44444443, 55555550, 00000000, 16, 75, "Ruth Hall 424");

-- Billie Holiday
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6461, 98989898, 55555550, 88888888, 2, 70, "Jeter Hall 512");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6212, 90909090, 55555550, 88888888, 3, 60, "Matingly Hall 623");
-- Paul McCartney (A's)
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1500, 6221, 44444441, 55555550, 55555555, 1, 50, "Jeter Hall 102");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6212, 90909090, 55555550, 55555555, 3, 75, "Gehrig Hall 504");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6461, 98989898, 55555550, 55555555, 2, 75, "Ruth Hall 203");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6232, 44444446, 55555550, 55555555, 5, 25, "DiMaggio Hall 305");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6233, 44444441, 55555550, 55555555, 6, 100, "Torre Hall 106");
-- Paul McCartney (B's)
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1800, 6241, 44444447, 55555550, 55555555, 7, 40, "Mantle Hall 707");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6246, 44444404, 55555550, 55555555, 9, 100, "Posada Hall 420");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1800, 6262, 44444449, 55555550, 55555555, 13, 25, "Posada Hall 608");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6283, 44444447, 55555550, 55555555, 14, 80, "Mantle Hall 509");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1800, 6242, 44444442, 55555550, 55555555, 8, 75, "Berra Hall 308");

-- George Harrison 
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6242, 44444448, 55555550, 66666666, 21, 45, "Robinson Hall 318");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1500, 6221, 44444441, 55555550, 66666666, 1, 50, "Jeter Hall 102");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6461, 98989898, 55555550, 66666666, 2, 75, "Ruth Hall 203");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6212, 90909090, 55555550, 66666666, 3, 75, "Gehrig Hall 504");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6232, 44444446, 55555550, 66666666, 5, 25, "DiMaggio Hall 305");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6233, 44444441, 55555550, 66666666, 6, 100, "Torre Hall 106");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6241, 44444404, 55555550, 66666666, 20, 50, "Rivera Hall 708");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1800, 6242, 44444442, 55555550, 66666666, 8, 75, "Berra Hall 308");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6283, 44444447, 55555550, 66666666, 14, 80, "Mantle Hall 509");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6284, 44444448, 55555550, 66666666, 15, 40, "Gehrig Hall 116");

-- Ringo Starr
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1500, 6221, 44444441, 55555550, 66667777, 1, 50, "Jeter Hall 102");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6461, 98989898, 55555550, 66667777, 2, 75, "Ruth Hall 203");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6212, 90909090, 55555550, 66667777, 3, 75, "Gehrig Hall 504");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6232, 44444446, 55555550, 66667777, 5, 25, "DiMaggio Hall 305");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1800, 6233, 44444441, 55555550, 66667777, 6, 100, "Torre Hall 106");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1800, 6242, 44444442, 55555550, 66667777, 8, 75, "Berra Hall 308");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Tuesday", 1500, 6246, 44444404, 55555550, 66667777, 9, 100, "Posada Hall 420");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1800, 6251, 44444449, 55555550, 66667777, 11, 60, "Ruth Hall 510");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Monday", 1530, 6254, 44444443, 55555550, 66667777, 12, 30, "River Hall 114");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Thursday", 1800, 6260, 44444445, 55555550, 66667777, 10, 50, "Jeter Hall 609");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1800, 6262, 44444449, 55555550, 66667777, 13, 25, "Posada Hall 608");
INSERT INTO active_courses VALUES(1, "Fall", 2021, "Wednesday", 1500, 6384, 44444446, 55555550, 66667777, 19, 100, "DiMaggio Hall 810");

-- Eric Clapton (Alumni) (B's)
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Monday", 1500, 6221, 44444441, 55555550, 77777777, 1, 50, "Jeter Hall 102");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Wednesday", 1500, 6212, 90909090, 55555550, 77777777, 3, 75, "Gehrig Hall 504");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Tuesday", 1500, 6461, 98989898, 55555550, 77777777, 2, 75, "Ruth Hall 203");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Monday", 1800, 6232, 44444446, 55555550, 77777777, 5, 25, "DiMaggio Hall 305");
INSERT INTO active_courses VALUES(1, "Fall", 2014, "Tuesday", 1800, 6233, 44444441, 55555550, 77777777, 6, 100, "Torre Hall 106");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Monday", 1800, 6241, 44444404, 55555550, 77777777, 20, 50, "Rivera Hall 708");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Thursday", 1800, 6242, 44444442, 55555550, 77777777, 8, 75, "Berra Hall 308");
-- Eric Clapton (Alumni) (A's)
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Tuesday", 1800, 6283, 44444447, 55555550, 77777777, 14, 80, "Mantle Hall 509");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Monday", 1800, 6284, 44444448, 55555550, 77777777, 15, 40, "Gehrig Hall 116");
INSERT INTO active_courses VALUES(1, "Spring", 2014, "Wednesday", 1800, 6286, 44444443, 55555550, 77777777, 16, 75, "Ruth Hall 424");



INSERT INTO prerequisites VALUES(6, 6233, 6232, null, "CSCI", 5, "None");
INSERT INTO prerequisites VALUES(12, 6254, 6221, null, "CSCI", 1, "None");
INSERT INTO prerequisites VALUES(14, 6283, 6212, null, "CSCI", 3, "None");
INSERT INTO prerequisites VALUES(15, 6284, 6212, null, "CSCI", 3, "None");
INSERT INTO prerequisites VALUES(16, 6286, 6283, 6232, "CSCI", 14, 5);
INSERT INTO prerequisites VALUES(17, 6325, 6212, null, "CSCI", 3, "None");
INSERT INTO prerequisites VALUES(18, 6339, 6461, 6212, "CSCI", 2, 3);
INSERT INTO prerequisites VALUES(19, 6384, 6284, null, "CSCI", 15, "None");
INSERT INTO prerequisites VALUES(8, 6242, 6241, null, "CSCI", 7, "None");
INSERT INTO prerequisites VALUES(9, 6246, 6461, 6212, "CSCI", 2, 3);
INSERT INTO prerequisites VALUES(11, 6251, 6461, null, "CSCI", 2, "None");

INSERT INTO prerequisites VALUES(1, 6221, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(2, 6461, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(3, 6212, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(4, 6220, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(5, 6232, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(7, 6241, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(10, 6260, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(13, 6262, null, null, "CSCI", "None", "None");
INSERT INTO prerequisites VALUES(20, 6241, null, null, "ECE", "None", "None");
INSERT INTO prerequisites VALUES(21, 6242, null, null, "ECE", "None", "None");
INSERT INTO prerequisites VALUES(22, 6210, null, null, "MATH", "None", "None");

-- Billie Holiday Grades
INSERT INTO grade VALUES("IP", 88888888, 6461, 1, 2);
INSERT INTO grade VALUES("IP", 88888888, 6212, 1, 3);
-- Paul McCartney Grades
INSERT INTO grade VALUES("A", 55555555, 6221, 1, 1);
INSERT INTO grade VALUES("A", 55555555, 6212, 1, 3);
INSERT INTO grade VALUES("A", 55555555, 6461, 1, 2);
INSERT INTO grade VALUES("A", 55555555, 6232, 1, 5);
INSERT INTO grade VALUES("A", 55555555, 6233, 1, 6);

INSERT INTO grade VALUES("B", 55555555, 6241, 1, 7);
INSERT INTO grade VALUES("B", 55555555, 6246, 1, 9);
INSERT INTO grade VALUES("B", 55555555, 6262, 1, 13);
INSERT INTO grade VALUES("B", 55555555, 6283, 1, 14);
INSERT INTO grade VALUES("B", 55555555, 6242, 1, 8);
-- George Harrison Grades
INSERT INTO grade VALUES("C", 66666666, 6242, 1, 21);
INSERT INTO grade VALUES("B", 66666666, 6221, 1, 1);
INSERT INTO grade VALUES("B", 66666666, 6461, 1, 2);
INSERT INTO grade VALUES("B", 66666666, 6212, 1, 3);
INSERT INTO grade VALUES("B", 66666666, 6232, 1, 5);
INSERT INTO grade VALUES("B", 66666666, 6233, 1, 6);
INSERT INTO grade VALUES("B", 66666666, 6241, 1, 20);
INSERT INTO grade VALUES("B", 66666666, 6242, 1, 8);
INSERT INTO grade VALUES("B", 66666666, 6283, 1, 14);
INSERT INTO grade VALUES("B", 66666666, 6284, 1, 15);
-- Ringo Starr Grades
INSERT INTO grade VALUES("A", 66667777, 6221, 1, 1);
INSERT INTO grade VALUES("A", 66667777, 6461, 1, 2);
INSERT INTO grade VALUES("A", 66667777, 6212, 1, 3);
INSERT INTO grade VALUES("A", 66667777, 6232, 1, 5);
INSERT INTO grade VALUES("A", 66667777, 6233, 1, 6);
INSERT INTO grade VALUES("A", 66667777, 6242, 1, 8);
INSERT INTO grade VALUES("A", 66667777, 6246, 1, 9);
INSERT INTO grade VALUES("A", 66667777, 6251, 1, 11);
INSERT INTO grade VALUES("A", 66667777, 6254, 1, 12);
INSERT INTO grade VALUES("A", 66667777, 6260, 1, 10);
INSERT INTO grade VALUES("A", 66667777, 6262, 1, 13);
INSERT INTO grade VALUES("A", 66667777, 6384, 1, 19);
-- Eric Clapton Grades
INSERT INTO grade VALUES("B", 77777777, 6221, 1, 1);
INSERT INTO grade VALUES("B", 77777777, 6212, 1, 3);
INSERT INTO grade VALUES("B", 77777777, 6461, 1, 2);
INSERT INTO grade VALUES("B", 77777777, 6232, 1, 5);
INSERT INTO grade VALUES("B", 77777777, 6233, 1, 6);
INSERT INTO grade VALUES("B", 77777777, 6241, 1, 20);
INSERT INTO grade VALUES("B", 77777777, 6242, 1, 21);
INSERT INTO grade VALUES("A", 77777777, 6284, 1, 15);
INSERT INTO grade VALUES("A", 77777777, 6283, 1, 14);
INSERT INTO grade VALUES("A", 77777777, 6286, 1, 16);

-- Thesis
INSERT INTO thesis VALUES(null, 66667777, 0, 0);
INSERT INTO thesis VALUES(null, 23232323, 0, 0);







