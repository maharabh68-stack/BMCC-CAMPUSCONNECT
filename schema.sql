PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS RSVP;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Organization;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS EventCategory;

CREATE TABLE Student (
    studentID INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    BMCCemail TEXT NOT NULL UNIQUE,
    major TEXT,
    yearLevel TEXT
);

CREATE TABLE Organization (
    orgID INTEGER PRIMARY KEY AUTOINCREMENT,
    orgName TEXT NOT NULL,
    orgType TEXT NOT NULL,
    category TEXT,
    contactEmail TEXT,
    description TEXT
);

CREATE TABLE EventCategory (
    categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE Event (
    eventID INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    eventDate TEXT NOT NULL,
    startTime TEXT,
    location TEXT,
    category TEXT,
    description TEXT,
    capacity INTEGER CHECK (capacity >= 0),
    orgID INTEGER NOT NULL,
    FOREIGN KEY (orgID) REFERENCES Organization(orgID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (category) REFERENCES EventCategory(categoryName) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE RSVP (
    rsvpID INTEGER PRIMARY KEY AUTOINCREMENT,
    studentID INTEGER NOT NULL,
    eventID INTEGER NOT NULL,
    rsvpDate TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Confirmed', 'Waitlisted', 'Cancelled')),
    FOREIGN KEY (studentID) REFERENCES Student(studentID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (eventID) REFERENCES Event(eventID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE(studentID, eventID)
);

INSERT INTO EventCategory (categoryName, description) VALUES
('Club', 'Student club and organization events.'),
('STEM / AI', 'Technology, science, artificial intelligence, and innovation events.'),
('Career', 'Career readiness, resume, internship, and networking events.'),
('Mentorship', 'Mentor matching and peer support events.'),
('Wellness', 'Mental health, physical health, and wellness activities.'),
('Food / Basic Needs', 'Food pantry and student support resource events.'),
('Academic Support', 'Tutoring, advising, study groups, and academic planning events.'),
('Community / Inclusion', 'Diversity, inclusion, and community building events.'),
('Sustainability', 'Environmental awareness and sustainability events.'),
('Leadership', 'Student leadership and government events.');

INSERT INTO Student (firstName, lastName, BMCCemail, major, yearLevel) VALUES
('Amina', 'Rahman', 'amina.rahman@stu.bmcc.cuny.edu', 'Computer Science', 'Freshman'),
('Jason', 'Lee', 'jason.lee@stu.bmcc.cuny.edu', 'Business Administration', 'Sophomore'),
('Maria', 'Gonzalez', 'maria.gonzalez@stu.bmcc.cuny.edu', 'Nursing', 'Freshman'),
('Daniel', 'Chen', 'daniel.chen@stu.bmcc.cuny.edu', 'Data Analytics', 'Sophomore'),
('Fatima', 'Ahmed', 'fatima.ahmed@stu.bmcc.cuny.edu', 'Liberal Arts', 'Freshman'),
('Kevin', 'Brown', 'kevin.brown@stu.bmcc.cuny.edu', 'Cybersecurity', 'Sophomore'),
('Nadia', 'Khan', 'nadia.khan@stu.bmcc.cuny.edu', 'Computer Science', 'Freshman'),
('Omar', 'Santos', 'omar.santos@stu.bmcc.cuny.edu', 'Engineering Science', 'Sophomore'),
('Grace', 'Kim', 'grace.kim@stu.bmcc.cuny.edu', 'Psychology', 'Freshman'),
('Mohammed', 'Hossain', 'mohammed.hossain@stu.bmcc.cuny.edu', 'Computer Information Systems', 'Sophomore'),
('Emily', 'Rivera', 'emily.rivera@stu.bmcc.cuny.edu', 'Criminal Justice', 'Freshman'),
('Ryan', 'Patel', 'ryan.patel@stu.bmcc.cuny.edu', 'Accounting', 'Sophomore'),
('Sara', 'Ali', 'sara.ali@stu.bmcc.cuny.edu', 'Health Education', 'Freshman'),
('Luis', 'Martinez', 'luis.martinez@stu.bmcc.cuny.edu', 'Computer Science', 'Sophomore'),
('Hannah', 'Wilson', 'hannah.wilson@stu.bmcc.cuny.edu', 'Human Services', 'Freshman');

INSERT INTO Organization (orgName, orgType, category, contactEmail, description) VALUES
('Student Government Association (SGA)', 'Student Organization', 'Leadership', 'sga@bmcc.cuny.edu', 'Student leadership group that represents student voices and supports campus activities.'),
('Office of Student Activities (OSA)', 'Campus Office', 'Club', 'studentactivities@bmcc.cuny.edu', 'Office that supports student clubs, events, and campus engagement.'),
('Center for Career Development', 'Campus Office', 'Career', 'career@bmcc.cuny.edu', 'Resource center for resumes, internships, career planning, and professional development.'),
('Panther Pantry', 'Campus Resource', 'Food / Basic Needs', 'pantherpantry@bmcc.cuny.edu', 'Resource supporting students with food and basic needs.'),
('Counseling Center', 'Campus Office', 'Wellness', 'counselingcenter@bmcc.cuny.edu', 'Confidential support for mental health, stress, adjustment, and wellness.'),
('Office of Accessibility', 'Campus Office', 'Academic Support', 'accessibility@bmcc.cuny.edu', 'Office supporting students with documented disabilities and accommodations.'),
('Panther Partners', 'Mentorship Program', 'Mentorship', 'pantherpartners@bmcc.cuny.edu', 'Peer support and campus connection program for students.'),
('Urban Male Leadership Academy (UMLA)', 'Mentorship Program', 'Mentorship', 'umla@bmcc.cuny.edu', 'Mentorship and leadership support program focused on student success.'),
('BMCC STEM Community', 'Academic Community', 'STEM / AI', 'stem@bmcc.cuny.edu', 'Community for students interested in science, technology, engineering, and math.'),
('BMCC Tech & Innovation Hub', 'Academic Resource', 'STEM / AI', 'techhub@bmcc.cuny.edu', 'Prototype resource for innovation, AI, technology, and project-based learning.'),
('Computer Science Club', 'Student Club', 'STEM / AI', 'csclub@stu.bmcc.cuny.edu', 'Club for students interested in programming, software projects, and computer science careers.'),
('Data Analytics Club', 'Student Club', 'STEM / AI', 'dataanalytics@stu.bmcc.cuny.edu', 'Club for students interested in data visualization, analytics, and database skills.'),
('Cybersecurity Club', 'Student Club', 'STEM / AI', 'cybersecurity@stu.bmcc.cuny.edu', 'Club for students interested in cyber safety, networks, and digital security.'),
('Women in STEM Club', 'Student Club', 'STEM / AI', 'womeninstem@stu.bmcc.cuny.edu', 'Student community supporting women and underrepresented students in STEM fields.'),
('International Student Club', 'Student Club', 'Community / Inclusion', 'internationalclub@stu.bmcc.cuny.edu', 'Club that helps international students build community and share cultures.'),
('Muslim Student Association', 'Student Club', 'Community / Inclusion', 'msa@stu.bmcc.cuny.edu', 'Student club focused on community, faith, service, and student support.'),
('Business and Entrepreneurship Club', 'Student Club', 'Career', 'businessclub@stu.bmcc.cuny.edu', 'Club for business, entrepreneurship, networking, and idea development.'),
('Debate Club', 'Student Club', 'Leadership', 'debateclub@stu.bmcc.cuny.edu', 'Club for public speaking, debate, argumentation, and communication skills.'),
('Health and Wellness Club', 'Student Club', 'Wellness', 'wellnessclub@stu.bmcc.cuny.edu', 'Club focused on healthy habits, student wellbeing, and campus wellness awareness.'),
('IMPACT Club', 'Student Club', 'Community / Inclusion', 'impactclub@stu.bmcc.cuny.edu', 'Student club focused on service, advocacy, and positive campus impact.'),
('Volunteer and Service Club', 'Student Club', 'Community / Inclusion', 'volunteerclub@stu.bmcc.cuny.edu', 'Club connecting students with service and volunteer opportunities.'),
('Transfer Student Success Group', 'Student Support Group', 'Academic Support', 'transfer@bmcc.cuny.edu', 'Group helping students prepare for transfer applications and four-year colleges.'),
('Peer Mentoring Program', 'Mentorship Program', 'Mentorship', 'peermentoring@bmcc.cuny.edu', 'Program connecting students with peer mentors for support and guidance.'),
('Academic Advisement Center', 'Campus Office', 'Academic Support', 'advisement@bmcc.cuny.edu', 'Advising resource for course planning, degree progress, and academic questions.'),
('Student Resource Center', 'Campus Resource', 'Food / Basic Needs', 'resourcecenter@bmcc.cuny.edu', 'Resource hub for students seeking support with campus services and basic needs.');

INSERT INTO Event (title, eventDate, startTime, location, category, description, capacity, orgID) VALUES
('New Student Welcome Meetup', '2026-05-15', '12:00', 'Richard Harris Terrace', 'Community / Inclusion', 'A welcoming event for new students to meet peers and learn about campus resources.', 80, 2),
('Club Discovery Day', '2026-05-16', '13:00', 'Student Cafeteria', 'Club', 'Students can explore clubs and organizations across campus.', 120, 2),
('Student Government Open House', '2026-05-17', '14:00', 'Main Building S-350', 'Leadership', 'Meet student leaders and learn how student government works.', 60, 1),
('Resume Building Workshop', '2026-05-18', '15:00', 'Career Center', 'Career', 'A practical workshop on building a strong resume.', 35, 3),
('Career Fair Preparation Session', '2026-05-19', '16:00', 'Fiterman Hall F-1000', 'Career', 'Prepare for career fairs, networking, and employer conversations.', 40, 3),
('STEM Networking Night', '2026-05-20', '17:30', 'Fiterman Hall', 'STEM / AI', 'Networking event for STEM students, mentors, and campus innovators.', 100, 9),
('CUNY AI Innovation Challenge', '2026-05-21', '10:00', 'Fiterman Hall, BMCC', 'STEM / AI', 'Student teams use AI and technology to solve social good challenges.', 150, 10),
('AI Hackathon for Social Good', '2026-05-22', '09:30', 'Fiterman Hall Computer Lab', 'STEM / AI', 'A prototype hackathon where students design AI tools for community impact.', 80, 10),
('BMCC Tech for Change Workshop', '2026-05-23', '13:30', 'Fiterman Hall F-905', 'STEM / AI', 'Hands-on workshop about technology solutions for student and community challenges.', 45, 10),
('Intro to Python Study Jam', '2026-05-24', '14:00', 'Computer Lab', 'Academic Support', 'Beginner-friendly Python practice session for students.', 35, 11),
('Cybersecurity Awareness Session', '2026-05-25', '15:00', 'Fiterman Hall F-710', 'STEM / AI', 'Learn password safety, phishing awareness, and cybersecurity basics.', 50, 13),
('Data Analytics Career Panel', '2026-05-26', '16:00', 'Fiterman Hall F-1001', 'Career', 'Panel discussion about data analytics careers and student preparation.', 70, 12),
('Women in STEM Mentorship Night', '2026-05-27', '17:00', 'Richard Harris Terrace', 'Mentorship', 'Mentorship event for women and underrepresented students in STEM.', 70, 14),
('International Student Welcome Session', '2026-05-28', '12:30', 'Main Building S-341', 'Community / Inclusion', 'A welcome and resource session for international students.', 50, 15),
('Panther Pantry Resource Session', '2026-05-29', '11:00', 'Panther Pantry', 'Food / Basic Needs', 'Learn about food and basic needs resources available to students.', 40, 4),
('Mental Health Awareness Workshop', '2026-05-30', '13:00', 'Counseling Center', 'Wellness', 'Workshop about stress, mental health awareness, and support resources.', 35, 5),
('Stress Management and Finals Prep', '2026-06-01', '14:00', 'Counseling Center', 'Wellness', 'Strategies for managing stress and preparing for finals.', 40, 5),
('Accessibility Resource Info Session', '2026-06-02', '15:00', 'Office of Accessibility', 'Academic Support', 'Information session about accessibility services and student accommodations.', 30, 6),
('Transfer Planning Workshop', '2026-06-03', '16:00', 'Academic Advisement Center', 'Academic Support', 'Learn how to plan transfer timelines and prepare applications.', 45, 22),
('Peer Mentor Connection Night', '2026-06-04', '17:00', 'Student Commons', 'Mentorship', 'Meet peer mentors and learn how mentoring can support your success.', 60, 23),
('Entrepreneurship Idea Pitch Night', '2026-06-05', '17:30', 'Fiterman Hall', 'Career', 'Students pitch business ideas and receive feedback.', 70, 17),
('Sustainability Campus Challenge', '2026-06-06', '12:00', 'Main Campus Lobby', 'Sustainability', 'Campus challenge focused on sustainability and reducing waste.', 65, 21),
('Volunteer Service Day', '2026-06-07', '10:00', 'Main Building Lobby', 'Community / Inclusion', 'Students connect with service opportunities and volunteer projects.', 80, 21),
('Public Speaking and Debate Workshop', '2026-06-08', '15:30', 'Speech Lab', 'Leadership', 'Practice public speaking, argument structure, and debate skills.', 40, 18),
('Academic Advising Q&A', '2026-06-09', '13:00', 'Academic Advisement Center', 'Academic Support', 'Ask questions about degree planning, course selection, and graduation requirements.', 60, 24),
('First Generation Student Meetup', '2026-06-10', '14:00', 'Student Resource Center', 'Community / Inclusion', 'A meetup for first-generation students to build support and community.', 50, 25),
('Scholarship and Internship Search Workshop', '2026-06-11', '16:00', 'Career Center', 'Career', 'Learn how to search for scholarships, internships, and application opportunities.', 55, 3),
('LinkedIn Profile Building Session', '2026-06-12', '15:00', 'Career Center', 'Career', 'Hands-on support for creating or improving a LinkedIn profile.', 35, 3),
('Student Leadership Training', '2026-06-13', '12:00', 'Main Building S-350', 'Leadership', 'Training for students interested in club leadership and campus involvement.', 50, 1),
('Community Inclusion Roundtable', '2026-06-14', '13:30', 'Richard Harris Terrace', 'Community / Inclusion', 'Student discussion about inclusion, belonging, and campus community.', 60, 20);

INSERT INTO RSVP (studentID, eventID, rsvpDate, status) VALUES
(1, 1, '2026-05-08', 'Confirmed'),
(2, 1, '2026-05-08', 'Confirmed'),
(3, 2, '2026-05-08', 'Confirmed'),
(4, 2, '2026-05-08', 'Waitlisted'),
(5, 3, '2026-05-09', 'Confirmed'),
(6, 4, '2026-05-09', 'Confirmed'),
(7, 5, '2026-05-09', 'Confirmed'),
(8, 6, '2026-05-09', 'Confirmed'),
(9, 7, '2026-05-10', 'Confirmed'),
(10, 7, '2026-05-10', 'Confirmed'),
(11, 8, '2026-05-10', 'Waitlisted'),
(12, 8, '2026-05-10', 'Confirmed'),
(13, 9, '2026-05-10', 'Confirmed'),
(14, 10, '2026-05-11', 'Confirmed'),
(15, 11, '2026-05-11', 'Cancelled'),
(1, 12, '2026-05-11', 'Confirmed'),
(2, 13, '2026-05-11', 'Confirmed'),
(3, 14, '2026-05-11', 'Confirmed'),
(4, 15, '2026-05-12', 'Confirmed'),
(5, 16, '2026-05-12', 'Confirmed'),
(6, 17, '2026-05-12', 'Waitlisted'),
(7, 18, '2026-05-12', 'Confirmed'),
(8, 19, '2026-05-12', 'Confirmed'),
(9, 20, '2026-05-13', 'Confirmed'),
(10, 21, '2026-05-13', 'Confirmed'),
(11, 22, '2026-05-13', 'Confirmed'),
(12, 23, '2026-05-13', 'Cancelled'),
(13, 24, '2026-05-13', 'Confirmed'),
(14, 25, '2026-05-14', 'Confirmed'),
(15, 26, '2026-05-14', 'Confirmed'),
(1, 27, '2026-05-14', 'Confirmed'),
(2, 28, '2026-05-14', 'Confirmed'),
(3, 29, '2026-05-14', 'Waitlisted'),
(4, 30, '2026-05-14', 'Confirmed'),
(5, 7, '2026-05-14', 'Confirmed'),
(6, 8, '2026-05-14', 'Confirmed');
