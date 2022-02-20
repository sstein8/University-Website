
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, url_for, redirect, flash, send_file
import mysql.connector


app = Flask('app')
hostname = 'ec2-23-21-57-219.compute-1.amazonaws.com'
username = 'ubuntu'
password = 'seas'
database = 'final'

# hostname = 'ip-172-31-69-9.ec2.internal'
# username = 'user'
# password = 'seas'
# database = 'final'

app.debug = True

app.secret_key = 'mysecretkey'


conn = mysql.connector.connect(host = hostname, user = username, password = password, db = database)
@app.route("/", methods=["GET", "POST"])
# ----------------------------------------------------------Login Page
@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if request.method == 'POST':
        c = conn.cursor()
        uni_ID = request.form["uni_ID"]
        password = request.form["password"]
        session["uni_ID"] = uni_ID #create session variable

        c.execute("SELECT uni_ID, password FROM users WHERE uni_ID=%s AND password=%s", (uni_ID, password))
        results = c.fetchone()
        if results: # if the user's account exists
            return redirect("/home_page")
            # c.close()
        elif results is None: #incorrect login info
            return render_template("log_in.html", message="Username or Password incorrect")
            # c.close()
      

    return render_template("log_in.html")
    # c.close()

# ----------------------------------------------------------Student Can Create Account
@app.route("/home_page", methods=["GET", "POST"])
def home_page():
    if request.method == 'GET':
        return render_template("home_page.html")

# ----------------------------------------------------------Student Can Create Account
@app.route("/create_account_student", methods=["GET", "POST"])
def create_account_student():
    message = " "
    if request.method == "POST":
        #get the info from form
        fname = request.form['fname']
        lname = request.form['lname']
        uni_ID = request.form['uni_ID']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        #if a person checks a role, it will send a 1, if not it sends a 0
        role_GS_M = request.form.getlist("Grad Student Masters")
        print("Masters: "+ str(role_GS_M))
        if(role_GS_M == []):
            role_GS_M = 0
        else:
            role_GS_M = 1

        role_GS_P = request.form.getlist("Grad Student PHD")
        print("PHD: " +  str(role_GS_P))
        if(role_GS_P == []):
            role_GS_P = 0
        else:
            role_GS_P = 1
    
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE uni_ID=%s", (uni_ID,))
        results = c.fetchone()

        if results: #there already exists an account under that ID
            message = "An account already exists under this university ID"
        else: #account creation was successful
            c.execute("INSERT INTO users (uni_ID, fname, lname, address, password, email, role_GS_M, role_GS_P, role_GSec, role_F, role_SA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (uni_ID, fname, lname, address, password, email, role_GS_M, role_GS_P, 0, 0, 0))
            if role_GS_P==1:
              c.execute("INSERT INTO thesis (thesis, uni_ID, decision, is_submitted) VALUES (%s, %s, %s, %s)", (None, uni_ID, 0, 0))
            conn.commit()
            message = "Account Creation Complete"
            conn.commit()
            
    return render_template("create_account_student.html", message=message)
    # c.close()

# ----------------------------------------------------------Create Account Admin
@app.route("/create_account_admin", methods=["GET", "POST"])
def create_account_admin():
    message = " "
    if request.method == "POST":
        #get the info from form
        fname = request.form['fname']
        lname = request.form['lname']
        uni_ID = request.form['uni_ID']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
 
        #if a person checks a role, it will send a 1, if not it sends a 0
        role_GS_M = request.form.getlist("Grad Student Masters")
        print("Masters: "+ str(role_GS_M))
        if(role_GS_M == []):
            role_GS_M = 0
        else:
            role_GS_M = 1

        role_GS_P = request.form.getlist("Grad Student PHD")
        print("PHD: " +  str(role_GS_P))
        if(role_GS_P == []):
            role_GS_P = 0
        else:
            role_GS_P = 1

        role_GSec = request.form.getlist("Grad Secretary")
        print("Grad Sec: " +  str(role_GSec))
        if(role_GSec == []):
            role_GSec = 0
        else:
            role_GSec = 1

        role_F = request.form.getlist("Faculty")
        print("Faculty: " + str(role_F))
        if(role_F == []):
            role_F = 0
        else:
            role_F = 1    

        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE uni_ID=%s", (uni_ID,))
        results = c.fetchone()

        #check if an account exists under this ID
        if results: #there already exists an account under that ID
            message = "An account already exists under this university ID"
        else: #account creation was successful
            c.execute("INSERT INTO users (uni_ID, fname, lname, address, password, email, role_GS_M, role_GS_P, role_GSec, role_F, role_SA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (uni_ID, fname, lname, address, password, email, role_GS_M, role_GS_P, role_GSec, role_F, 0))
            if role_GS_P==1:
                c.execute("INSERT INTO thesis (thesis, uni_ID, decision, is_submitted) VALUES (%s, %s, %s, %s)", (None, uni_ID, 0, 0))
            conn.commit()
            message = "Account Creation Complete"
            conn.commit()
            c.execute("SELECT role_GS_M, role_GS_P, role_GSec, role_F FROM users WHERE uni_ID=%s", (uni_ID,))
            roles = c.fetchone()
            GS = roles[0]
            print("GS:"+str(GS))
            PHD = roles[1]
            print("PHD:"+str(PHD))
            GSec= roles[2]
            print("Gsec:"+str(GSec))
            Fac = roles[3]
            print("Fac:"+str(Fac))

    return render_template("create_account_admin.html", message=message)
    # c.close()



# ----------------------------------------------------------Click on button for registration
@app.route("/registration", methods = ["GET", "POST"])
def registration():
    if request.method == "GET":
        return redirect("/main_hub_registration")
        


# ----------------------------------------------------------Main Hub For Registration
@app.route("/main_hub_registration", methods=["GET", "POST"])
def main_hub_registration():
    role1=""
    uni_ID = session["uni_ID"]
 
    # c = conn.cursor()
    c = conn.cursor()
    #get role information assiciated with the uni ID
    c.execute("SELECT role_GS_M, role_GS_P, role_GSec, role_F, role_SA FROM users WHERE uni_ID=%s" %(uni_ID,))
    results = c.fetchone()

    #create session variables for the roles
    role_GS_M = results[0]
    session["role_GS_M"] = role_GS_M
    role_GS_P = results[1]
    session["role_GS_P"] = role_GS_P
    role_GSec = results[2]
    session["role_GSec"] = role_GSec
    role_F = results[3]
    session["role_D"] = role_F
    role_SA = results[4]
    session["role_SA"] = role_SA

    #check the roles and assign role names
    if(role_GS_M == 1 or role_GS_P):
        role1 = "Student"

    if(role_GSec == 1):
        role1 = "Grad Secretary"

    if(role_F == 1):
        role1 = "Faculty"

    if(role_SA == 1):
        role1 = "System Admin"

    return render_template("main_hub_registration.html",role1=role1)
    # c.close()

# ----------------------------------------------------------Display Course Catalog
@app.route("/course_catalog", methods=["GET", "POST"])
def course_catalog():
    if request.method == "GET":
        c = conn.cursor()
        #retreive all courses that the university offers
        c.execute("SELECT all_courses.dept_name, all_courses.course_num, all_courses.title, all_courses.credit_hrs, prerequisites.prereq_num1, prerequisites.prereq_num2, all_courses.course_info FROM all_courses LEFT JOIN prerequisites on all_courses.course_num = prerequisites.course_num AND all_courses.dept_name = prerequisites.department")
        course_data = c.fetchall()
        return render_template("course_catalog.html", table=enumerate(course_data))
        # c.close()

# ----------------------------------------------------------Admin Creates Course
@app.route("/admin_create_course", methods=["GET", "POST"])
def admin_create_coruse():
  if request.method == "POST":
    c = conn.cursor()
    error_msg=""
    title = request.form["title"]
    course_num = request.form["course_num"]
    course_num = int(course_num)
    course_ID = request.form["course_ID"]
    course_ID = int(course_ID)
    credit_hrs = request.form["credit_hrs"]
    credit_hrs = int(credit_hrs)
    dept_name = request.form["dept_name"]
    sec_ID = request.form["sec_ID"]
    sec_ID = int(sec_ID)
    faculty_ID = request.form["faculty_ID"]
    faculty_ID = int(faculty_ID)
    room_cap = request.form["room_cap"]
    room_cap = int(room_cap)
    year = request.form["year"]
    year = int(year)
    room_number = request.form["room_number"]
    building = request.form["Building"]
    semester = request.form["Semester"]
    day = request.form["Day"]
    time = request.form["Time"]
    course_info = request.form["course_info"]

    room_loc = building + " " + room_number

    #lookup if there is already a class in all courses with the same course ID
      #if not, check in active courses if that course num/title is already offered at same time

    print("title: "+title)
    print("course num: "+str(course_num))
    print("course_ID: "+str(course_ID))
    print("credit_hrs"+str(credit_hrs))
    print("dept: "+dept_name)
    print("section: "+str(sec_ID))
    print("faculty: "+str(faculty_ID))
    print("location: "+room_loc)
    print("seats: "+str(room_cap))
    print("year: "+str(year))
    print("sem: "+semester)
    print("day: "+day)
    print("time: "+str(time))

    #check if a course under this ID exists
    c.execute("SELECT course_ID FROM all_courses")
    IDS = c.fetchall()
    for row in IDS:
      if course_ID in row:
        error_msg = "A course with this ID already exists"
        return render_template("admin_create_course.html", error_msg=error_msg)

    #check if the facultyID is one in the database 
    #get all uni ID's of faculty
    # c.execute("SELECT uni_ID FROM users WHERE role_F = %s", (1,))
    # f_IDS = c.fetchall()
    # faculty_ID = (str(faculty_ID)+",")
    # for row in f_IDS:
    #   row = str(row)
    # if faculty_ID not in f_IDS:
    #     error_msg = "This University ID is not associated with any Faculty"
    #     return render_template("admin_create_course.html", error_msg=error_msg)

    
  

    c.execute("INSERT INTO all_courses (dept_name, course_num, title, credit_hrs, course_ID, course_info) VALUES (%s, %s, %s, %s, %s, %s)", (dept_name, course_num, title, credit_hrs, course_ID, course_info))
    #active courses
    c.execute("INSERT INTO active_courses (sec_ID, semester, year, day, time, course_num, faculty_ID, gsec_ID, student_ID, course_ID, room_cap, room_loc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sec_ID, semester, year, day, time, course_num, faculty_ID, 55555550, 00000000, course_ID, room_cap, room_loc))
    c.execute("INSERT INTO prerequisites (course_ID, course_num, prereq_num1, prereq_num2, department, prereq_ID1, prereq_ID2) VALUES (%s, %s, %s, %s, %s, %s, %s)", (course_ID, course_num, None, None, dept_name, "None", "None"))
    print("inserted into tables")
  return render_template("admin_create_course.html")
    
    


# ----------------------------------------------------------Course Registration
@app.route("/course_registration_page", methods=["GET", "POST"])
def course_registration_page():
    PHD_Error = " "
    reg_failed_msg = " "
    global course_reg_data
    global already_registered_for
    
    uni_ID = session["uni_ID"]
    if request.method == "GET":
        c = conn.cursor()

        #retreive all courses currently being taught
        c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_cap, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s and year=%s", (00000000,2021))
        course_reg_data = c.fetchall()

        #retreive all courses that a student is already registered for
        c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
        already_registered_for = c.fetchall()
        for row in already_registered_for:
          print(row)


        PHD_Error = " "
        reg_failed_msg = " "
        
        return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
        # c.close()

    if request.method == "POST":
    
        PHD_Error = " "
        reg_failed_msg = " "
        c = conn.cursor(buffered=True)
        #get the user's ID
        uni_ID = session["uni_ID"]
        #check if the user is a PHD student
        role_GS_P = session["role_GS_P"]
        #get the course they want to register for
        course_ID = request.form["course_ID"]
        print("Course ID: "+course_ID)
        session["course_ID"] = course_ID

        # #check that that course is being offered
        c.execute("SELECT course_ID FROM active_courses WHERE year=%s and student_ID=%s", (2021,00000000))

        check_CID = c.fetchall()

        c.execute("SELECT course_num FROM active_courses WHERE course_ID=%s and year=%s and student_ID=%s LIMIT 1", (course_ID,2021, 00000000))
        check_CID = c.fetchone()
        if(check_CID):
          course_num = check_CID[0]
        else:
          # if check_CID is None: #the course ID is not valid
            reg_failed_msg="Invalid Course ID"

            c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
            already_registered_for = c.fetchall()

            return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
              # c.close()

        #check if student is already registered for that course
        c.execute("SELECT student_ID FROM active_courses WHERE course_ID=%s AND student_ID=%s LIMIT 1", (course_ID, uni_ID))
        stud_ID = c.fetchone()
        if stud_ID:
            #student is already enrolled in this course
            reg_failed_msg="You have already registered for this course"

            c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
            already_registered_for = c.fetchall()

            return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
            # c.close()

        #Check that a student is not registering for 2 courses that happen on the same day time
        #get the date and time of the class that they want to register for
        c.execute("SELECT day, time FROM active_courses WHERE course_ID=%s AND student_ID=%s", (course_ID,00000000))
        day_time = c.fetchone()
        day = day_time[0]
        time = day_time[1]

        #Check the day and time of the classes they are already registered for
        c.execute("SELECT day, time FROM active_courses WHERE student_ID=%s", (uni_ID,))
        registered_for_day_time = c.fetchall()
        print("------PRINTING DAY/TIME---------")
        for i in range(len(registered_for_day_time)): #see if the time of the course you want to register is equal to the start time of a class you already registered for or has a time conflict
            if(str(day) == str(registered_for_day_time[i][0]) and (time in range (registered_for_day_time[i][1], registered_for_day_time[i][1]+300) or (time + 300 > registered_for_day_time[i][1]))):

                fail_MSG= "You are already registered for a course at the same day and time"

                c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
                already_registered_for = c.fetchall()
                return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=fail_MSG, PHD_Error=PHD_Error)
                # c.close()
        
        #check if the student has met the prerequisite requirements

        #retreive the prereqs for the class they want to register for
        c.execute("SELECT prereq_ID1, prereq_ID2 FROM prerequisites WHERE course_ID=%s", (course_ID,))
        prereqs = c.fetchone() #list of all of the prereqs for that class
        prereq1 = prereqs[0]
        prereq2 = prereqs[1]

        #only 1 prereq
        if (prereq2 == "None" and prereq1!= "None"):
            #see if they have taken that course
            c.execute("SELECT course_num FROM active_courses WHERE student_ID=%s and course_ID=%s", (uni_ID, prereq1))
            course = c.fetchone()
            if course is None:
                reg_failed_msg = "You have not taken all of the prerequisites to register for course ID: " + course_ID

                c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
                already_registered_for = c.fetchall()

                return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
                # c.close()
                
        if (prereq1!="None" and prereq2!="None"): #2 prereqs
            c.execute("SELECT course_num FROM active_courses WHERE student_ID=%s and course_ID=%s", (uni_ID, prereq1))
            course1 = c.fetchone()
            c.execute("SELECT course_num FROM active_courses WHERE student_ID=%s and course_ID=%s", (uni_ID, prereq2))
            course2 = c.fetchone()
            if(course1 is None or course2 is None):
                reg_failed_msg = "You have not taken all of the prerequisites to register for course ID: " + course_ID

                c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
                already_registered_for = c.fetchall()

                return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
                # c.close()

        #PHD students can only register for course nums 6000 and up
        course_num = check_CID[0]
        if(role_GS_P == 1 and course_num < 6000):
            PHD_Error = "Error: PHD students must only register for 6000 level courses"
            c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
            already_registered_for = c.fetchall()
            return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
            # c.close()

        #check if there are enough seats available in the class
        c.execute("SELECT room_cap FROM active_courses WHERE course_ID=%s and student_ID=%s", (course_ID, 00000000))
        seats_available = c.fetchone()[0]
        #not enough seats
        if(seats_available < 1):
          reg_failed_msg = "No available seats in the class"
          c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
          already_registered_for = c.fetchall()
          return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)


        #------------Successful Registration--------------------------------------

        else: #the course is being offered and it is good to be registered for
            print("course ID: " + str(course_ID))
            #get the basic info about the course that they chose
            c.execute("SELECT sec_ID, semester, year, day, time, faculty_ID, gsec_ID, course_num, room_cap, room_loc FROM active_courses WHERE course_ID=%s AND student_ID=%s", (course_ID, 00000000))

            results = c.fetchone()
            sec_ID = results[0]
            semester = results[1]
            year = results[2]
            day = results[3]
            time = results[4]
            faculty_ID = results[5]
            gsec_ID = results[6]
            course_num = results[7]
            room_cap = results[8]
            room_loc = results[9]
      
            if(role_GS_P == 1 and course_num < 6000):
                #PHD students can only register for course nums 6000 and up
                PHD_Error = "Error: PHD students must only register for 6000 level courses"
            
            else:
                PHD_Error = ""
                course_ID = session["course_ID"]
                #insert a new row into active courses with the student's ID
                c.execute("INSERT INTO active_courses (sec_ID, semester, year, day, time, course_num, faculty_ID, gsec_ID, student_ID, course_ID, room_cap, room_loc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (sec_ID, semester, year, day, time, course_num, faculty_ID, gsec_ID, uni_ID, course_ID, room_cap, room_loc))
                conn.commit()
                c.execute("INSERT INTO grade (letter_grade, uni_ID, course_num, sec_ID, course_ID) VALUES (%s, %s, %s, %s, %s)", ("IP", uni_ID, course_num, sec_ID, course_ID))
                conn.commit()
                #decrease the capacity/seats available
                #need to update the room cap in all of the places where the class is mentioned
                new_room_cap = room_cap - 1
                c.execute("UPDATE active_courses SET room_cap=%s WHERE course_ID=%s", (new_room_cap, course_ID))
                conn.commit()

                #get the updated table that displays active courses
                c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_cap, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s and year=%s", (00000000,2021))
                course_reg_data = c.fetchall()

                reg_failed_msg = "Registration for Course ID: " + course_ID + " Successful"

                #get the classes that the student registers for
                c.execute("SELECT sec_ID, semester, year, day, time, users.lname, room_loc, course_num, course_ID FROM active_courses LEFT JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE student_ID=%s", (uni_ID,))
                already_registered_for = c.fetchall()

                return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
                        
        return render_template("course_registration_page.html", table=course_reg_data, table2=already_registered_for, reg_failed_msg=reg_failed_msg, PHD_Error=PHD_Error)
        # c.close()


# ----------------------------------------------------------Drop Class
@app.route('/drop_class', methods=['GET','POST'])
def drop_class():
    if request.method == "POST":
        uni_ID = session["uni_ID"]
        course_ID = request.form["course_ID"]
        course_num = request.form["course_num"]

        c = conn.cursor(buffered=True)
        c.execute('DELETE FROM active_courses WHERE course_ID=%s and student_ID=%s', (course_ID, uni_ID))
        conn.commit()
        print("deleted course from active courses")

        #Must also delete class from transcript
        c.execute('DELETE FROM grade WHERE course_ID=%s and uni_ID=%s', (course_ID, uni_ID))
        conn.commit()

        #add one to the seats available
        c.execute("SELECT room_cap FROM active_courses WHERE course_ID=%s", (course_ID,))
        room_cap = c.fetchone()[0]
        new_room_cap = room_cap + 1
        print("room cap"+ str(room_cap))
        print("new room cap: "+str(new_room_cap))
        c.execute("UPDATE active_courses SET room_cap=%s WHERE course_ID=%s", (new_room_cap, course_ID))
        conn.commit()

        #get the updated rows
        c.execute("SELECT sec_ID, semester, year, day, time, course_num, course_ID, room_cap, room_loc FROM active_courses WHERE student_ID=%s", (uni_ID,))
        already_registered_for = c.fetchall()
        print("after deleting")
        for row in already_registered_for:
          print(row)

        return redirect("/course_registration_page")
        # c.close()

# ----------------------------------------------------------Students Can View Their Transcript
@app.route("/transcript", methods=["GET", "POST"])
def transcript():

    c = conn.cursor(buffered=True)
    uni_ID = session["uni_ID"]

    # declare strings
    name = ""
    avgGPA = ""
    totalCredits = ""
    msg = ""
    #conn.commit() 

    # get transcript info
    c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
    results = c.fetchall()
    for row in results:
      print(row)

    
    # get student's name
    c.execute('SELECT fname, lname FROM users WHERE uni_ID=%s', (uni_ID,)) 
    name = c.fetchall()

    # format student's name
    for row in name:
      name = " ".join(row)

    msg = "Viewing " + name + "'s Transcript"

    #get student's role
    role_GS_M = session["role_GS_M"]
    role_GS_P = session["role_GS_P"]
    if(role_GS_M == 1):
        program = "Master's Program"
    if(role_GS_P == 1):
        program = "PHD Program"

    # get average GPA
    # select all of the grades where the uni ID is the one in session
    c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (uni_ID, "IP"))
    letter_grades = c.fetchall()
    sum_points = 0
    num_classes = 0
    points = 0
    for [row] in letter_grades:
    #get point value of each grade
      #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
      print(row)
      if row == "A":
        points = 4.0
      if row == "A-":
        points = 3.7
      if row == "B+":
        points = 3.3
      if row == "B":
        points = 3.0
      if row == "B-":
        points = 2.7
      if row == "C+":
        points = 2.3
      if row == "C":
        points = 2.0
        print("grade is C")
      if row == "F":
        points = 0.0
      #add all together
      num_classes = num_classes + 1
      sum_points = sum_points + points
      if num_classes == 0 or None:
        avgGPA = "N/A"
      else:
        avgGPA = sum_points / num_classes
        avgGPA = str(round(avgGPA, 2))
        
      #calculate total amt of credits
      c.execute("SELECT SUM(all_courses.credit_hrs) FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s", (uni_ID,))
      # c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
      totalCredits = c.fetchone()
      totalCredits = str(totalCredits[0])
      print("total credits: "+ str(totalCredits[0]))
    
 

    return render_template('/student_transcript.html', results=results, msg=msg, avgGPA=avgGPA, totalCredits=totalCredits, uni_ID=uni_ID, program=program)

# ----------------------------------------------------------Faculty Can View Students' Transcript
@app.route("/students_transcript", methods=["GET", "POST"])
def students_transcript():
    c = conn.cursor(buffered=True)
    #get the Faculty's ID
    uni_ID = session["uni_ID"]
    #get the student's ID
    student_ID = request.form["student_ID"]


    # declare strings
    name = ""
    avgGPA = ""
    totalCredits = ""
    msg = ""
    #conn.commit() 

    # get transcript info
    c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (student_ID,)) 
    info = c.fetchall()
    for row in info:
      print(row)

  
    # get student's name
    c.execute('SELECT fname, lname FROM users WHERE uni_ID=%s', (student_ID,)) 
    name = c.fetchall()

    # format student's name
    for row in name:
      name = " ".join(row)

    msg = "Viewing " + name + "'s Transcript"

    #get student's program/role
    #get the role of the student
    c.execute("SELECT role_GS_M, role_GS_P, role_Alum FROM users WHERE uni_ID=%s", (student_ID,))
    results = c.fetchone()

    #create variables for the roles
    role_GS_M = results[0] 
    role_GS_P = results[1]
    role_Alum = results[2]
    if(role_GS_M == 1):
        program = "Master's Program"
    if(role_GS_P == 1):
        program = "PHD Program"
    if(role_Alum == 1):
        program = "Alumni"


    # get average GPA
    # select all of the grades where the uni ID is the one in session
    c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (student_ID, "IP"))
    #c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s ", (student_ID,))

    letter_grades = c.fetchall()
    sum_points = 0
    num_classes = 0
    points = 0
    for [row] in letter_grades:
      #get point value of each grade
        #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
      print(row)
      if row == "A":
        points = 4.0
      if row == "A-":
        points = 3.7
      if row == "B+":
        points = 3.3
      if row == "B":
        points = 3.0
      if row == "B-":
        points = 2.7
      if row == "C+":
        points = 2.3
      if row == "C":
        points = 2.0
        print("grade is C")
      if row == "F":
        points = 0.0
      
      #add all together
      num_classes = num_classes + 1
      sum_points = sum_points + points
      if num_classes == 0 or None:
        avgGPA = "N/A"
      else:
        avgGPA = sum_points / num_classes
        avgGPA = str(round(avgGPA, 2))
        
      #calculate total amt of credits
      c.execute("SELECT SUM(all_courses.credit_hrs) FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s", (student_ID,))
      # c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
      totalCredits = c.fetchone()
      totalCredits = str(totalCredits[0])
      print("total credits: "+ str(totalCredits[0]))
    
 

    # return render_template("transcript.html", fname=fname, lname=lname, program=program,uni_ID=student_ID, courseInfo=courseInfo)
    return render_template("/student_transcript.html", results=info, msg=msg, avgGPA=avgGPA, totalCredits=totalCredits, uni_ID=student_ID, program=program)

    # c.close()


# ----------------------------------------------------------Student Schedule
@app.route("/student_schedule", methods=["GET", "POST"])
def student_chedule():
    #Students can view all courses that they are taking

    if request.method == "GET":
        c = conn.cursor()
        uni_ID = session["uni_ID"]

        c.execute("SELECT all_courses.dept_name, all_courses.title, active_courses.course_num, all_courses.credit_hrs, active_courses.day, active_courses.time, all_courses.course_ID FROM active_courses JOIN all_courses on all_courses.course_ID = active_courses.course_ID WHERE active_courses.student_ID=%s", (uni_ID,))
        courses_data = c.fetchall()
        
    return render_template("student_schedule.html", table=courses_data)
    # c.close()

# ----------------------------------------------------------Faculty Teaching Schedule
@app.route("/active_courses", methods=["GET", "POST"])
def active_courses():
    #Professors can view all courses that they are teaching
    if request.method == "GET":
        c = conn.cursor()
        faculty_ID = session["uni_ID"]

        c.execute("SELECT all_courses.dept_name, all_courses.title, active_courses.course_num, all_courses.credit_hrs, active_courses.day, active_courses.time, all_courses.course_ID FROM active_courses JOIN all_courses on all_courses.course_ID = active_courses.course_ID WHERE active_courses.student_ID=%s AND active_courses.faculty_ID=%s", (00000000, faculty_ID,))
        courses_data = c.fetchall()
        
    return render_template("active_courses.html", table=courses_data)
    # c.close()

# ----------------------------------------------------------Grad Secretary Schedule
@app.route("/gs_schedule", methods=["GET", "POST"])
def gs_schedule():
    #Grad Secretaries can view all courses that they are teaching
    if request.method == "GET":
        c = conn.cursor()
        gsec_ID = session["uni_ID"]

        c.execute("SELECT all_courses.dept_name, all_courses.title, active_courses.course_num, all_courses.credit_hrs, active_courses.day, active_courses.time, all_courses.course_ID FROM active_courses JOIN all_courses on all_courses.course_ID = active_courses.course_ID WHERE active_courses.student_ID=%s AND active_courses.gsec_ID=%s", (00000000, gsec_ID,))
        courses_data = c.fetchall()
        
    return render_template("active_courses.html", table=courses_data)
    # c.close()

# ----------------------------------------------------------Update Account Info
@app.route("/update_account_info", methods=["GET", "POST"])
def update_account_info():
    password_message=""
    address_message=""
    email_message=""
    uni_ID = session["uni_ID"]
    if request.method == "GET":
        return render_template("update_account_info.html", password_message=password_message, address_message=address_message, email_message=email_message)
        # c.close()
    if request.method == "POST":
        #get the new info
        new_password = request.form["new_password"]
        new_address = request.form["new_address"]
        new_email = request.form["new_email"]
        #if the field is not blank, update the existing info
        print("new password: "+new_password)
        print("new address: "+new_address)
        print("new email: "+new_email)
        c = conn.cursor()
     
        if(new_password!=""): #password updated
            c.execute('UPDATE users SET password=%s where uni_ID=%s', (new_password, uni_ID))
            conn.commit()
            password_message="Password successfully updated"

        if(new_address!=""): #address updated
            c.execute('UPDATE users SET address=%s where uni_ID=%s', (new_address, uni_ID))
            conn.commit()
            address_message="Address successfully updated"
        if(new_email!=""): #email updated
            c.execute('UPDATE users SET email=%s where uni_ID=%s', (new_email, uni_ID))
            conn.commit()
            email_message="email successfully updated"
        return render_template("update_account_info.html", password_message=password_message, address_message=address_message, email_message=email_message)
        # c.close()

# ----------------------------------------------------------Admin View All Course History

@app.route('/admin_choose_year', methods=["GET", "POST"])
def admin_choose_year():
    global active_course_data
    if request.method == "GET":
        return render_template("admin_choose_year.html")
        # c.close()
    if request.method == "POST":
        select_year = request.form["select_year"]
        session["select_year"] = select_year
        print("Year: "+select_year)
        # session["select_year"] = select_year
        c = conn.cursor()
        c.execute("SELECT sec_ID, semester, year, day, time, users.lname, course_num, course_ID FROM active_courses INNER JOIN users ON users.uni_ID=active_courses.faculty_ID WHERE year=%s and student_ID=%s", (select_year, 00000000))
        active_course_data = c.fetchall()
        return render_template("admin_view_all_courses.html", table=active_course_data)
        # c.close()



# ----------------------------------------------------------Logout
@app.route('/logout')
def logout():
  LOmessage="Logged Out"
  session.clear()
  return render_template("log_in.html", message = LOmessage)
  c.close()

# ----------------------------------------------------------Faculty, admin, gsec view student info
@app.route("/student_info", methods=["GET", "POST"])
def student_info():
    
    c = conn.cursor(buffered=True)
    if request.method == "POST":
        uni_ID = session["uni_ID"] #get the ID of whoever is logged in
 
        course_ID = request.form["course_ID"]
        session["course_ID"] = course_ID
       
  
        #Check whether user is an admin
        c.execute("SELECT role_SA, role_F, role_gsec FROM users WHERE users.uni_ID=%s", (uni_ID,))
        result = c.fetchone()
        admin = result[0]
        faculty = result[1]
        gsec = result[2]
      
        if (faculty == 1): #user is a prof
            role = "faculty"
            session["role"] = role
            c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and faculty_ID=%s ", (course_ID, uni_ID))
            student_list = c.fetchall()
            return render_template("student_info.html", table=student_list)
            # c.close()
        if (gsec == 1): #user is a gsec
            role = "gsec"
            session["role"] = role
            c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and gsec_ID=%s ", (course_ID, uni_ID))
            student_list = c.fetchall()
            return render_template("student_info.html", table=student_list)   
            # c.close()  
        if(admin == 1): #user is an admin
            #grab the professor's  ID
            select_year = session["select_year"]
            role = "admin"
            session["role"] = role
            c.execute("SELECT active_courses.faculty_ID FROM active_courses WHERE active_courses.course_ID=%s", (course_ID,))
            result = c.fetchone()
            faculty_ID = result[0]
            c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and faculty_ID=%s and year=%s", (course_ID, faculty_ID, select_year))
            student_list = c.fetchall()
            return render_template("student_info.html", table=student_list) 
            # c.close()

# ----------------------------------------------------------Faculty, admin, gsec view Current Courses Info (roster, grades)
@app.route("/course_info", methods=["GET", "POST"])
def course_info():
    
    if request.method == "GET":
        c = conn.cursor()
        faculty_ID = session["uni_ID"]
        c.execute("SELECT all_courses.title, active_courses.course_num, active_courses.sec_ID, active_courses.course_ID FROM active_courses JOIN all_courses on all_courses.course_ID = active_courses.course_ID WHERE active_courses.student_ID=%s AND active_courses.faculty_ID=%s", (00000000, faculty_ID))
        course_data = c.fetchall()
    return render_template("course_info.html", table=course_data)
    # c.close()

@app.route("/course_info_gs", methods=["GET", "POST"])
def course_info_gs():
    
    if request.method == "GET":
        c = conn.cursor()
        gsec_ID = session["uni_ID"]

        c.execute("SELECT all_courses.title, active_courses.course_num, active_courses.sec_ID, active_courses.course_ID FROM active_courses JOIN all_courses on all_courses.course_ID = active_courses.course_ID WHERE active_courses.student_ID=%s AND active_courses.gsec_ID=%s", (00000000, gsec_ID,))

        course_data = c.fetchall()
    return render_template("course_info.html", table=course_data)
    # c.close()


# ----------------------------------------------------------Grading
@app.route('/grading', methods=['GET', 'POST'])
def grading():

    valid_grades = ["A", "A-", "B+", "B", "B-", "C+", "C", "F"] #list of valid grades
    message=""
    if request.method == 'POST':
        c = conn.cursor()
        grader_ID = session["uni_ID"] #uni_ID of the grader
        new_grade = request.form["grade"] #retreive the grade that the teacher entered
        course_ID = session["course_ID"] #course ID of the course to enter grades for
        role = session["role"] #get the role from student_info route
        stid = request.form['stid'] #get student's ID
    
        #check to see if a letter grade exists
        c.execute("SELECT letter_grade FROM grade WHERE grade.uni_ID=%s AND grade.course_ID=%s", (stid,course_ID,))
        gradeResult = c.fetchone()
        grade = gradeResult[0]

        if (role == "admin"): #admins can override any grade
            if(new_grade not in valid_grades):
                message = "ERROR: INVALID LETTER GRADE ENTERED"
                c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s", (course_ID,))
                student_list = c.fetchall()
                return render_template("student_info.html", table=student_list, message=message)
                # c.close()
            else:
                c.execute('UPDATE grade SET letter_grade=%s WHERE grade.uni_ID=%s AND grade.course_ID=%s', (new_grade,stid,course_ID))
                conn.commit()
                
                c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s", (course_ID,))
                student_list = c.fetchall()
                message = "ADMIN OVERRIDE: Grade successfully entered for "+stid
                return render_template("student_info.html", table=student_list, message=message)
                # c.close()

        
        if (grade == "IP" and role == "faculty"):
            #check if the grade they entered is valid
            if(new_grade not in valid_grades):
                message = "ERROR: INVALID LETTER GRADE ENTERED"
                c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and faculty_ID=%s", (course_ID, grader_ID))
                student_list = c.fetchall()
                return render_template("student_info.html", table=student_list, message=message)
                # c.close()
            else: #new grade is ok
                c.execute('UPDATE grade SET letter_grade=%s WHERE grade.uni_ID=%s AND grade.course_ID=%s', (new_grade,stid,course_ID))
                conn.commit()
                c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and faculty_ID=%s", (course_ID, grader_ID))
                student_list = c.fetchall()
                message = "Grade successfully entered for "+stid
                return render_template("student_info.html", table=student_list, message=message)
                # c.close()

        #a grade has already been entered, prof cannot enter a new grade
        elif (grade != "IP" and role == "faculty"): #If they are a professor but a grade is entered, they cannot update
            message = "ERROR  There is already a grade on file for "+stid
            c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and faculty_ID=%s", (course_ID, grader_ID))
            student_list = c.fetchall()
            return render_template("student_info.html", table=student_list, message=message)
            # c.close()
     
        ##If they aren't a professor and they've reached this point, they are a gsec
        if (grade != "IP" and role == "gsec"):
            #check if the grade they entered is valid
            if(new_grade not in valid_grades):
                message = "ERROR: INVALID LETTER GRADE ENTERED"
                c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and gsec_ID=%s", (course_ID, grader_ID))
                student_list = c.fetchall()
                return render_template("student_info.html", table=student_list, message=message)
                # c.close()

            else: #new grade is ok
                c.execute('UPDATE grade SET letter_grade=%s WHERE grade.uni_ID=%s AND grade.course_ID=%s', (new_grade,stid,course_ID))
                message = "Grade successfully entered for "+stid 
                conn.commit()
                c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and gsec_ID=%s", (course_ID, grader_ID))
                student_list = c.fetchall()
                return render_template("student_info.html", table=student_list, message=message)
                # c.close()

        elif (grade == "IP" and role == "gsec"):
            message = "ERROR! The professor has not yet entered a grade for this class " 
            c.execute("SELECT users.lname, users.fname, active_courses.student_ID FROM users JOIN active_courses on users.uni_ID = active_courses.student_ID WHERE course_ID=%s and gsec_ID=%s", (course_ID, grader_ID))
            student_list = c.fetchall()
            return render_template("student_info.html", table=student_list, message=message)
            # c.close()
#   ADVISING CODE BEING PUT IN HERE 

@app.route("/advising", methods = ["GET", "POST"])
def advising():
    if request.method == "GET":
        return redirect("/main_hub_advising")
# main hub for advising gets whatever value you are and returns the home page for that person
@app.route("/main_hub_advising", methods=["GET", "POST"])
def main_hub_advising():
    role1=""
    uni_ID = session["uni_ID"]
 
    # c = conn.cursor()
    c = conn.cursor()
    #get role information assiciated with the uni ID
    c.execute("SELECT role_GS_M, role_GS_P, role_GSec, role_F, role_SA, role_Alum FROM users WHERE uni_ID=%s" %(uni_ID,))
    results = c.fetchone()

    #create session variables for the roles
    role_GS_M = results[0]
    session["role_GS_M"] = role_GS_M
    role_GS_P = results[1]
    session["role_GS_P"] = role_GS_P
    role_GSec = results[2]
    session["role_GSec"] = role_GSec
    role_F = results[3]
    session["role_D"] = role_F
    role_SA = results[4]
    session["role_SA"] = role_SA
    role_Alum = results [5]
    session["role_Alum"] = role_Alum
    #check the roles and assign role names
    if(role_GS_M == 1 or role_GS_P):
        role1 = "Student"

    if(role_GSec == 1):
        role1 = "Grad Secretary"


    if(role_F == 1):
        role1 = "Faculty"

    if(role_SA == 1):
        role1 = "System Admin"

    if(role_Alum== 1):
        role1 = "Alumni"

    return render_template("main_hub_advising.html",role1=role1)


@app.route('/system_admin', methods = ['GET'])
def system_admin():
  #Sql Statements go here
  return render_template('/system_admin.html')

@app.route('/faculty_advisor', methods=['GET'])
def faculty_advisor():
  return render_template('/faculty_advisor.html')

@app.route('/grad_secretary', methods = ['GET'])
def grad_secretary():
#Sql statements go here
  return render_template('/grad_secretary.html')

@app.route('/grad_student', methods = ['GET'])
def grad_student():
  role1=""
  uni_ID = session["uni_ID"]
 
    # c = conn.cursor()
  c = conn.cursor()
    #get role information assiciated with the uni ID
  c.execute("SELECT role_GS_M, role_GS_P, role_GSec, role_F, role_SA, role_Alum FROM users WHERE uni_ID=%s" %(uni_ID,))
  results = c.fetchone()

    #create session variables for the roles
  role_GS_M = results[0]
  session["role_GS_M"] = role_GS_M
  role_GS_P = results[1]
  session["role_GS_P"] = role_GS_P

    #check the roles and assign role names
  if(role_GS_M == 1):
      role1 = "Master"

  if(role_GS_P == 1):
      role1 = "PHD"

  #Sql Statements go here
  return render_template('/grad_student.html',role1=role1)
  
@app.route('/form1', methods = ['GET', 'POST'])
def form1(): 
  c = conn.cursor(buffered = True)
  if request.method == 'POST':
    i = 1
    ID = request.form['ID']
    print(ID)
    for i in range(1, 13):
      # make sure currin is what you want
      currIN = "class" + str(i) + "name"
      courseName = request.form[currIN]
      print(courseName)
      #print(courseName)
      currINID = "class" + str(i) + "ID"
      courseID = request.form[currINID]
      if courseID == '':
        print("not a valid course")
        continue
      print(courseID)
      c.execute('SELECT course_num, title from all_courses where course_num = %s AND title = %s', (courseID, courseName))
      results = c.fetchall()
      if len(results) == 0:
        print("this is not a valid course")
        continue 

      if int(courseID) == 0: 
        print("not a valid course ID")
        continue
      insert_stmt = "INSERT INTO Form1 (ID, courseNumber, courseTitle )VALUES (%s, %s, %s)" 
      print(courseName)
      print(ID)
      print(courseID)
      data = (int(ID), int(courseID), courseName)
      c.execute(insert_stmt, data)
      conn.commit() 
    return render_template('form1.html')
  return render_template('form1.html')


# this route lists the names of advisees 
@app.route('/view_advisees', methods = ['GET'])
def view_advisees():
  c = conn.cursor()
  if 'uni_ID' in session:

    # find students where their assigned advisor is the same as the logged in advisor
    c.execute('SELECT fname, lname, uni_ID FROM users WHERE role_GS_M = 1 OR role_GS_P = 1  and advisor_ID = %s',(session['uni_ID'],))

    results = c.fetchall()
    return render_template('/view_advisees.html', results=results)

# this route displays a student's transcript info
@app.route('/view_transcript', methods = ['GET', 'POST'])
def view_transcript():

  if 'username' in session:
    if request.method == 'POST' and 'ID' in request.form:
      ID = request.form['ID']
      c = conn.cursor(buffered=True)
      # conn.commit() 
      print(ID)
      # get transcript info
      c.execute('SELECT department, courseNumber, courseTitle, creditHours, Grade FROM TRANSCRIPT WHERE studentID = "%s"', (int(uni_ID),))

      results = c.fetchall()
      conn.commit()

      # declare strings
      notFound = ""
      name = ""
      avgGPA = ""
      totalCredits = ""
      msg = ""

      # if results exist
      if results:
        # get student's name
        c.execute('SELECT fname, lname FROM users WHERE ID = "%s"', (int(uni_ID),))

        name = c.fetchall()
        conn.commit()

        # format student's name
        for row in name:
          name = " ".join(row)

        msg = "Viewing " + name + "'s Transcript"

        # get average GPA
        c.execute('SELECT FORMAT (AVG(GPA), 2) FROM TRANSCRIPT AS T WHERE T.studentID = "%s"', (int(uni_ID),))
        avgGPA = c.fetchone()
        conn.commit()

        # format GPA
        for r in avgGPA:
          avgGPA = "".join(r)

        # get total credits
        c.execute('SELECT FORMAT (SUM(earnedHours), 1) FROM TRANSCRIPT AS T WHERE T.studentID = "%s"', (int(uni_ID),))
        totalCredits = c.fetchone()
        conn.commit()

        # format total credits
        for r in totalCredits:
          totalCredits = "".join(r)
 
      if not results:
        notFound = "User not found"

      return render_template('/view_transcript.html', results=results, msg=msg, avgGPA=avgGPA, totalCredits=totalCredits, notFound=notFound)

  return render_template('/view_transcript.html')

# this route displays all the information from a student's form 1
@app.route('/view_form1', methods = ['GET','POST'])
def view_form1():
  # c = conn.cursor(buffered=True)
  if 'uni_ID' in session:
    if request.method == 'POST':
      ID = request.form['ID']

      c = conn.cursor(buffered=True)

      # get form 1 info
      c.execute('SELECT courseNumber, courseTitle FROM Form1 WHERE ID="%s"', (int(ID),))

      results = c.fetchall()
      conn.commit()
      print("----form 1-----")
      for row in results:
        print(results)

      # get student's name
      c.execute('SELECT fname, lname FROM users WHERE uni_ID = "%s"', (int(ID),))

      conn.commit()
      name = c.fetchall()

      for row in name:
        name = " ".join(row)

      return render_template('/view_form1.html', results=results, name=name)

    return render_template('/view_form1.html')


@app.route('/view_thesis', methods = ['GET','POST'])
def view_thesis():
  # c = conn.cursor(buffered=True)
  if 'uni_ID' in session:
    if request.method == 'POST':
      ID = request.form['ID']

      c = conn.cursor(buffered=True)

      # get form 1 info
      c.execute('SELECT thesis FROM thesis WHERE uni_ID="%s"', (int(ID),))

      results = c.fetchall()
      conn.commit()

      # get student's name
      c.execute('SELECT fname, lname FROM users WHERE uni_ID = "%s"', (int(ID),))

      conn.commit()
      name = c.fetchall()

      for row in name:
        name = " ".join(row)

      return render_template('/view_thesis.html', results=results, name=name)

    return render_template('/view_thesis.html')

@app.route('/approve_thesis', methods = ['GET' , 'POST'])
def approve_thesis():
  c = conn.cursor()
  if request.method == 'POST':
    ID = request.form['ID']
    decision = request.form['yn']
    if decision == 'yes':
      msg = "you have approved their thesis!"
      c.execute('UPDATE thesis set decision = 1 where uni_ID = %s', (int(ID),) )
      conn.commit()
    if decision == 'no':
      c.execute('UPDATE thesis set decision = 0 where uni_ID = %s', (int(ID),))
      conn.commit()
      msg = "your have NOT approved their thesis :("
    return render_template('/view_thesis.html', msg = msg)
  return render_template('/view_thesis.html')  

@app.route('/alumni')
def alumni():
    return render_template('alumni.html')

@app.route('/student_data', methods = ['GET', 'POST'])
def student_data():
  c = conn.cursor()
  results = None
  fname = ""
  lname =""
  if request.method == 'POST':
    uni_ID = request.form['ID']
    print(uni_ID)
    c = conn.cursor()
    c.execute('SELECT uni_ID,fname,lname FROM users WHERE uni_ID=%s',( uni_ID, ))
    results = c.fetchone()
    print(results)
    if results is None:
      return 'Student ID does not exist.'   
    return render_template('student_data.html',fname=results[1],lname=results[2], uni_ID = results[0])
  return render_template('student_data.html') 
#this route allows the graduate secretary to approve or decline students graduation

@app.route('/grad_approve', methods = ['GET', 'POST'])
def grad_approve():
  c = conn.cursor()
  results = None
  if request.method == 'POST':
    ID = request.form['ID']
    c = conn.cursor()
  

    c.execute('SELECT uni_ID,fname,lname,role_GS_M, role_GS_P FROM users WHERE uni_ID=%s',( ID,))
    results = c.fetchone() #fetching results for a student
    masters = results[3]
    phd = results[4]
    print(results)
    if(masters==0 and phd ==0): #checks if the user input exists
      msg = "this person is not a student "
      return render_template('grad_approve.html', msg = msg)
  
    choice = request.form["Yes/No"]
    if choice == 'Yes':
      role = 1
      #c.execute('UPDATE users SET role= Alumni WHERE role = Graduate Student',(Alumni, Graduate Student))
      c.execute('UPDATE users SET role_Alum=%s WHERE users.uni_ID=%s', (role,ID,)) #moves graduating students to the almuni table
      conn.commit()
      msg = "This student has been cleared to graduate" 
      return render_template('grad_approve.html', msg = msg)
    elif choice == 'No':
      msg =  'Student isnt cleared to graduate'
      return render_template('grad_approve.html', msg = msg)      

    
  return render_template('grad_approve.html' )   
#this route allows the grad secretary to assign advisors to students
@app.route('/advisors', methods = ['GET', 'POST'])
def advisors():
  c = conn.cursor()
  if request.method == 'POST':
  #   c.execute('SELECT uni_ID FROM users WHERE role_GS_P = 1  and advisor_ID is null') #pulling id's from user table
  #   phd = c.fetchone()
  #   c.execute('SELECT uni_ID FROM users WHERE role_GS_M = 1 and advisor_ID is null') #pulling id's from user table
  #   masters = c.fetchone()
  #  #fetches all stdent ID's
    

    advisorID = request.form['advisorID']
    ID = request.form['ID']

    print(ID)
    print(advisorID)

    c.execute('UPDATE users SET advisor_ID = %s WHERE uni_ID = %s', (advisorID, ID,)) 
     
    conn.commit() 
    return render_template('advisors.html')
  return render_template('advisors.html')

#check if graduate student is a phd or masters 
@app.route('/phd_or_ms', methods = ['GET','POST'])
def phd_or_ms():
    c = conn.cursor()
    uni_ID = session["uni_ID"]
    c.execute("SELECT role_GS_M, role_GS_P, role_GSec, role_F, role_SA FROM users WHERE uni_ID=%s", (uni_ID,))
    results = c.fetchone()
    role_GS_M = results[0]
    print(role_GS_M)
    session["role_GS_M"] = role_GS_M
    role_GS_P = results[1]
    print(role_GS_P)
    if(role_GS_M == 1):
        return redirect("/can_graduate_ms")
    if(role_GS_P == 1):
      return redirect("/can_graduate")
    return render_template('/phd_or_ms.html')

@app.route('/personal_info', methods = ['GET','POST'])
def personal_info():
  c = conn.cursor() 
  
  c.execute('SELECT fname, lname, email, address, uni_ID FROM users WHERE uni_ID = %s' , (session['uni_ID'],))
  results  = c.fetchone()
  # c.execute('SELECT email FROM users WHERE uni_ID = %s' , (session['uni_ID'],))
  
  # c.execute('SELECT address FROM users WHERE uni_ID = %s' , (session['uni_ID'],))
  # address = c.fetchall()
  # c.execute('SELECT uni_ID FROM users WHERE uni_ID = %s' , (session['uni_ID'],))
  # ID = c.fetchall()
  if results is None:
    return 'Student ID does not exist.'   
  return render_template('personal_info.html',fname=results[0],lname=results[1], email = results[2], address = results[3],uni_ID = results[4])
  # return render_template('personalinfo.html', name = name, email = email, address = address, ID = ID )
  # if results is None:
  #   msg = ("not working, we have no personal info")
  #   return render_template('notgood.html' ,msg= msg)
  return render_template('personal_info.html')

@app.route('/edit_pi', methods = ['GET','POST'])
def edit_pi():
  c = conn.cursor() 
  if request.method == 'POST':
    msg=""
    email = request.form['email']
    print(email)
    address = request.form['address']
    print(address)
    if address == "" and email == "":
      print("you havent changed your email")
    if address == "":
      c.execute('UPDATE users SET email = %s WHERE uni_ID = %s ' , (email, session['uni_ID'],))
      conn.commit()
      msg="Info successfully updated"
      return render_template('edit_pi.html', msg = msg)


    if email == "":
      c.execute('UPDATE users SET address = %s WHERE uni_ID = %s', (address, session['uni_ID'],))
      conn.commit()
      msg="Info successfully updated"
      return render_template('edit_pi.html', msg = msg)

    #if both are not null 
    if address != "" and email != "":
      print("this is where it should be")
      c.execute('UPDATE users SET email = %s , address = %s WHERE uni_ID = %s', (email, address, session['uni_ID'],))
      conn.commit()
      msg="Info successfully updated"
      return render_template('edit_pi.html', msg = msg)
  return render_template('edit_pi.html')

#seeing if a phd candidate can graduate
@app.route('/can_graduate', methods = ['GET','POST'])
def can_graduate():
  print("can graduate works we are in")
  c = conn.cursor() 
  # error checking in here? 
  c.execute('SELECT decision from thesis where uni_ID = %s', (session['uni_ID'],))
  thesis = c.fetchall()
  c.execute('select SUM(credit_hrs) from all_courses INNER JOIN active_courses where dept_name = "CSCI" AND  student_ID = %s', (session['uni_ID'],))
  cscredit = c.fetchall()
  print(cscredit)
  c.execute('SELECT count(letter_grade) from grade where letter_grade = "B-" OR letter_grade = "C+" OR letter_grade = "C" OR letter_grade = "F" AND uni_ID = %s', (session['uni_ID'],)) 
  count = c.fetchall()
  if count[0][0] > 1:
    msg = "you have 1 grade below a B, retake those courses, get better grades, then try again"
    return render_template('/cangraduatems.hmtl', msg = msg)
  if count[0][0] >= 3:
    msg = "you have at least 3 or more grades below a B, you have now been placed on academic suspension :("
    return render_template('/notgood.html', msg = msg)
    # select sum(credit_hrs) from all_courses INNER JOIN active_courses where studentID = %s
  c.execute ('select SUM(credit_hrs) from all_courses INNER JOIN active_courses where student_ID = %s',(session['uni_ID'],))
  hours = c.fetchall()
  # declare strings
  name = ""
  avgGPA = ""
  totalCredits = ""
  msg = ""
 # get average GPA
    # select all of the grades where the uni ID is the one in session
  c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (session['uni_ID'], "IP"))
  letter_grades = c.fetchall()
  sum_points = 0
  num_classes = 0
  points = 0
  for [row] in letter_grades:
    #get point value of each grade
      #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
    print(row)
    if row == "A":
      points = 4.0
    if row == "A-":
      points = 3.7
    if row == "B+":
      points = 3.3
    if row == "B":
      points = 3.0
    if row == "B-":
      points = 2.7
    if row == "C+":
      points = 2.3
    if row == "C":
      points = 2.0
      print("grade is C")
    if row == "F":
      points = 0.0
      #add all together
    num_classes = num_classes + 1
    sum_points = sum_points + points
    if num_classes == 0 or None:
      avgGPA = "N/A"
    else:
      avgGPA = sum_points / num_classes
      avgGPA = str(round(avgGPA, 2))
  #iterate through grade to count how many grades below a B 
  if hours[0][0] is None:
    msg = "you havent taken any courses yet! why are you trying to graduate?"
    return render_template('/can_graduate.html', msg = msg)
  if int(hours[0][0]) < 36: 
     msg = "you havent taken enough credits, take some more classes and try again :("
     return render_template('/can_graduate.html', msg = msg)
  if float(avgGPA) < 3.5:
    msg = "your gpa is too low, fix it and then try again :("
    return render_template('/can_graduate.html', msg = msg)
  if int(cscredit[0][0]) < 30: 
    msg = "you havent taken enough COMPUTER SCIENCE take some more :("
    return render_template('/can_graduate.html', msg = msg)
  # sql statement inserting the can graduate value 
  if int(thesis[0][0]) == 0: 
    msg = "your thesis has not been approved, you cant graduate"
    return render_template('/can_graduate.html', msg = msg)
  # if thesis == 1:
  #   msg = "you can graduate!"
  #   return render_template('/cangraduate.html', msg = msg)
  msg = "yeah you can! wait for Graduate Secretary Approval"
  return render_template('/can_graduate.html', msg=msg)

@app.route('/phd_thesis', methods = ['GET','POST'])
def phd_thesis():
  c = conn.cursor() 
  return render_template('phd_thesis.html')
@app.route('/submit_thesis', methods = ['GET', 'POST'])
def submit_thesis():
  c = conn.cursor()
  
  if request.method == 'POST': 
    # render template wasnt working for this so had to switch to redirect
    thesis = request.form['thesis']
    print("Thesis: "+thesis)
    #empty thesis
    if thesis == "":
      msg = "you submitted an empty thesis"
      return render_template('submit_thesis.html', msg = msg)
    #already submitted one
    c.execute("SELECT is_submitted FROM thesis WHERE uni_ID=%s",(session['uni_ID'],))
    result = c.fetchone()[0]
    if(result == 1):
      msg = "you have already submitted a thesis"
      return render_template('submit_thesis.html', msg = msg)
    #good to go
    c.execute("UPDATE thesis SET thesis=%s, is_submitted = %s WHERE uni_ID=%s", (thesis, 1, session['uni_ID']))
    conn.commit()
    msg = "Thesis successfully submitted"
    return render_template('/submit_thesis.html', msg = msg)
  return render_template('/submit_thesis.html')
#allows a phd candidate to apply for graduation
@app.route('/grad_app_phd.html', methods = ['GET', 'POST'])
def grad_app_phd():
  c = conn.cursor()
  if request.method == 'POST': 
    # render template wasnt working for this so had to switch to redirect
    return redirect(url_for('can_graduate'))
  return render_template('/gradappphd.html')

# allows a master student to apply for graduation
@app.route('/grad_app.html', methods = ['GET', 'POST'])
def grad_app():
  c = conn.cursor()
  if request.method == 'POST': 
    return redirect('can_graduate_ms')
  return render_template('/grad_app.html') 

# allows a master student to see if they qualify for graduation
@app.route('/can_graduate_ms', methods = ['GET', 'POST'])
def can_graduate_ms():
  c = conn.cursor() 
  # error checking in here
  c.execute('SELECT all_courses.dept_name, grade.course_num FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE all_courses.dept_name = "CSCI" AND active_courses.course_num = 6212 AND uni_ID=%s', (session["uni_ID"],))
  CSCI6212 = c.fetchall()
  if len(CSCI6212) == 0:
    msg = "you have not taken CSCI 6212, which is a required course, take it and do well then try again"
    return render_template('/can_graduate_ms.html', msg = msg)
  c.execute('SELECT all_courses.dept_name, grade.course_num FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE all_courses.dept_name = "CSCI" AND active_courses.course_num = 6221 AND uni_ID=%s', (session["uni_ID"],))
  CSCI6221 = c.fetchall()
  print("it gets here ")
  print(CSCI6221)
  if len(CSCI6221) ==0 :
    msg = "you have not taken CSCI 6221, which is a required course, take it and do well then try again"
    return render_template('/can_graduate_ms.html', msg = msg)
  c.execute('SELECT all_courses.dept_name, grade.course_num FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE all_courses.dept_name = "CSCI" AND active_courses.course_num = 6461 AND uni_ID=%s', (session["uni_ID"],))
  CSCI6461 = c.fetchall()
  if len(CSCI6461) == 0 :
    msg = "you have not taken CSCI 6461, which is a required course, take it and do well then try again"
    return render_template('/can_graduate_ms.html', msg = msg)
  c.execute ('select SUM(credit_hrs) from all_courses INNER JOIN active_courses where student_ID = %s',(session['uni_ID'],))
  # c.execute ('SELECT letter_grade, SUM(earnedHours) from grade join all_courses where uni_ID = %s',(session['uni_ID'],))
  person = c.fetchall()
  #iterate through grade to count how many grades below a B
  c.execute('SELECT count(letter_grade) from grade where letter_grade = "B-" OR letter_grade = "C+" OR letter_grade = "C" OR letter_grade = "F" AND uni_ID = %s', (session['uni_ID'],)) 
  count = c.fetchall()
  name = ""
  avgGPA = ""
  totalCredits = ""
  msg = ""
 # get average GPA
    # select all of the letter_grades where the uni ID is the one in session
  c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (session["uni_ID"], "IP"))
  letter_grades = c.fetchall()
  sum_points = 0
  num_classes = 0
  points = 0
  for [row] in letter_grades:
    #get point value of each grade
      #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
    print(row)
    if row == "A":
      points = 4.0
    if row == "A-":
      points = 3.7
    if row == "B+":
      points = 3.3
    if row == "B":
      points = 3.0
    if row == "B-":
      points = 2.7
    if row == "C+":
      points = 2.3
    if row == "C":
      points = 2.0
      print("grade is C")
    if row == "F":
      points = 0.0
      #add all together
    num_classes = num_classes + 1
    sum_points = sum_points + points
    if num_classes == 0 or None:
      avgGPA = "N/A"
    else:
      avgGPA = sum_points / num_classes
      avgGPA = str(round(avgGPA, 2))
  if count[0][0] > 2:
    msg = "you have two grades below a B, retake those courses, get better grades, then try again"
    return render_template('/can_graduate_ms.hmtl', msg = msg)
  if count[0][0] >= 3:
    msg = "you have at least 3 or more grades below a B, you have now been placed on academic suspension :("
    return render_template('/not_good.html', msg = msg)
  if int(person[0][0]) < 30: 
    msg = "you havent taken enough credits, take some more classes and try again :("
    return render_template('/can_graduate_ms.html',msg = msg)
  if float(avgGPA) < 3.0:
    msg = "your gpa is too low, fix it and then try again :("
    return render_template('/can_graduate_ms.html', msg = msg)
  msg = "yeah you can! wait for Graduate Secretary Approval"
  # sql statement inserting the can graduate value 
  return render_template('/can_graduate_ms.html', msg = msg)

# this route displays a student's transcript info
@app.route('/student_transcript', methods = ['GET', 'POST'])
def student_transcript():

    # if 'username' in session:
    c = conn.cursor(buffered=True)
    uni_ID = session["uni_ID"]

    # declare strings

    name = ""
    avgGPA = ""
    totalCredits = ""
    msg = ""
    #conn.commit() 

    # get transcript info
    c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
    results = c.fetchall()

    # if results exist
    if results:
      # get student's name
      c.execute('SELECT fname, lname FROM users WHERE uni_ID=%s', (uni_ID,)) 
      name = c.fetchall()

      # format student's name
      for row in name:
        name = " ".join(row)

      msg = "Viewing " + name + "'s Transcript"

      # get average GPA
      # select all of the grades where the uni ID is the one in session
      c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (uni_ID, "IP"))
      letter_grades = c.fetchall()
      sum_points = 0
      num_classes = 0
      points = 0
      for [row] in letter_grades:
        #get point value of each grade
          #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
        print(row)
        if row == "A":
          points = 4.0
        if row == "A-":
          points = 3.7
        if row == "B+":
          points = 3.3
        if row == "B":
          points = 3.0
        if row == "B-":
          points = 2.7
        if row == "C+":
          points = 2.3
        if row == "C":
          points = 2.0
          print("grade is C")
        if row == "F":
          points = 0.0
        #add all together
        num_classes = num_classes + 1
        sum_points = sum_points + points
      
      avgGPA = sum_points / num_classes
      avgGPA = str(round(avgGPA, 2))
        
      #calculate total amt of credits
      c.execute("SELECT SUM(all_courses.credit_hrs) FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s", (uni_ID,))
      # c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
      totalCredits = c.fetchone()
      totalCredits = str(totalCredits[0])
      print("total credits: "+ str(totalCredits[0]))
    
 

    return render_template('/student_transcript.html', results=results, msg=msg, avgGPA=avgGPA, totalCredits=totalCredits)



@app.route('/alum_edit_pi', methods = ['GET','POST'])
def alum_edit_pi():
  c = conn.cursor() 
  if request.method == 'POST':
    email = request.form['email']
    print(email)
    address = request.form['address']
    print(address, session['uni_ID'])
    if address == "" and email == "":
      print("you havent changed your email")
    if address == "":
      print("in here 1")
      c.execute('UPDATE users SET email = %s WHERE uni_ID= %s ' , (email, session['uni_ID'],))
      conn.commit()
    if email == "":
      print("in here 2")
      c.execute('UPDATE users SET address = %s WHERE uni_ID = %s', (address, session['uni_ID'],))
      conn.commit()
    #if both are not null 
    if address != "" and email != "":
      print("in here 3")
      c.execute('UPDATE users SET email = %s , address = %s WHERE uni_ID = %s', (email, address, session['uni_ID'],))
      conn.commit()
  return render_template('alum_edit_pi.html')

@app.route('/alum_pi', methods = ['GET','POST'])
def alum_pi():
  c = conn.cursor() 
  c.execute('SELECT fname, lname, email, address, uni_ID FROM users WHERE uni_ID = %s' , (session['uni_ID'],))
  results  = c.fetchone()
  if results is None:
    return 'Student ID does not exist.'   
  return render_template('alum_pi.html',fname=results[0],lname=results[1], email = results[2], address = results[3],uni_ID = results[4])
 
  return render_template('alum_pi.html')


@app.route('/advising_transcript', methods = ['GET', 'POST'])
def advising_transcript():
  c = conn.cursor(buffered=True)
    #get the Faculty's ID
  uni_ID = session["uni_ID"]
  if request.method == "POST":
    #get the student's ID
    student_ID = request.form["ID"]

    # declare strings
    name = ""
    avgGPA = ""
    totalCredits = ""
    msg = ""
    roles =""
    letter_grade = ""
    # grades""
    #conn.commit() 

    c.execute("SELECT role_GS_M,role_GS_P FROM users WHERE uni_ID=%s",(student_ID,))
    roles = c.fetchone()
    GS = roles[0]
    PHD = roles[1]
    print("M: "+ str(GS))
    print("P: "+str(PHD))
    if(GS==0 and PHD==0):
      msg="This individual is not a student"
      return render_template('/advising_transcript.html', results="", msg=msg,program = "", uni_ID = student_ID)


      

    # get transcript info
    c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (student_ID,)) 
    grades = c.fetchall()
    for row in grades:
      print(row)

  
    # get student's name
    c.execute('SELECT fname, lname FROM users WHERE uni_ID=%s', (student_ID,)) 
    name = c.fetchall()

    # format student's name
    for row in name:
      name = " ".join(row)

    msg = "Viewing " + name + "'s Transcript"

    #get student's program/role
    #get the role of the student
    c.execute("SELECT role_GS_M, role_GS_P FROM users WHERE uni_ID=%s", (student_ID,))
    roles = c.fetchone()

    #create variables for the roles
    role_GS_M = roles[0] 
    role_GS_P = roles[1]
    if(role_GS_M == 1):
        program = "Master's Program"
    if(role_GS_P == 1):
        program = "PHD Program"


    # get average GPA
    # select all of the grades where the uni ID is the one in session
    c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (student_ID, "IP"))
    letter_grades = c.fetchall()
    sum_points = 0
    num_classes = 0
    points = 0
    for [row] in letter_grades:
      #get point value of each grade
        #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
      print(row)
      if row == "A":
        points = 4.0
      if row == "A-":
        points = 3.7
      if row == "B+":
        points = 3.3
      if row == "B":
        points = 3.0
      if row == "B-":
        points = 2.7
      if row == "C+":
        points = 2.3
      if row == "C":
        points = 2.0
        print("grade is C")
      if row == "F":
        points = 0.0
      #add all together
      num_classes = num_classes + 1
      sum_points = sum_points + points
      if num_classes == 0 or None:
        avgGPA = "N/A"
      else:
        avgGPA = sum_points / num_classes
        avgGPA = str(round(avgGPA, 2))
        
      #calculate total amt of credits
      c.execute("SELECT SUM(all_courses.credit_hrs) FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s", (student_ID,))
      # c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
      totalCredits = c.fetchone()
      totalCredits = str(totalCredits[0])
      print("total credits: "+ str(totalCredits[0]))
    
    
    return render_template('/advising_transcript.html', results = grades, msg=msg, avgGPA=avgGPA, totalCredits=totalCredits, program = program, uni_ID = student_ID)
  
  return render_template('/advising_transcript.html')

@app.route("/advising_student_transcript", methods=["GET", "POST"])
def advising_student_transcript():
    c = conn.cursor(buffered=True)
    uni_ID = session["uni_ID"]

    # declare strings
    name = ""
    avgGPA = ""
    totalCredits = ""
    msg = ""
    #conn.commit() 

    # get transcript info
    c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
    results = c.fetchall()
    for row in results:
      print(row)

    
    # get student's name
    c.execute('SELECT fname, lname FROM users WHERE uni_ID=%s', (uni_ID,)) 
    name = c.fetchall()

    # format student's name
    for row in name:
      name = " ".join(row)

    msg = "Viewing " + name + "'s Transcript"

    #get student's role
    role_GS_M = session["role_GS_M"]
    role_GS_P = session["role_GS_P"]
    role_Alum = session["role_Alum"]
    if(role_GS_M == 1):
        program = "Master's Program"
    if(role_GS_P == 1):
        program = "PHD Program"
    if(role_Alum ==1):
      program = "Alumni"

    # get average GPA
    # select all of the grades where the uni ID is the one in session
    c.execute("SELECT letter_grade FROM grade WHERE uni_ID = %s and letter_grade <> %s", (uni_ID, "IP"))
    letter_grades = c.fetchall()
    sum_points = 0
    num_classes = 0
    points = 0
    for [row] in letter_grades:
    #get point value of each grade
      #A=4, A-=3.7, B+ = 3.3, B=3, B-=2.7, C+=2.3, C=2, F=0
      print(row)
      if row == "A":
        points = 4.0
      if row == "A-":
        points = 3.7
      if row == "B+":
        points = 3.3
      if row == "B":
        points = 3.0
      if row == "B-":
        points = 2.7
      if row == "C+":
        points = 2.3
      if row == "C":
        points = 2.0
        print("grade is C")
      if row == "F":
        points = 0.0
      #add all together
      num_classes = num_classes + 1
      sum_points = sum_points + points
      if num_classes == 0 or None:
        avgGPA = "N/A"
      else:
        avgGPA = sum_points / num_classes
        avgGPA = str(round(avgGPA, 2))
        
      #calculate total amt of credits
      c.execute("SELECT SUM(all_courses.credit_hrs) FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s", (uni_ID,))
      # c.execute('SELECT all_courses.dept_name, grade.course_num, all_courses.title, all_courses.credit_hrs, grade.letter_grade FROM all_courses INNER JOIN active_courses on active_courses.course_ID = all_courses.course_ID AND active_courses.student_ID INNER JOIN grade ON grade.uni_ID = active_courses.student_ID AND grade.course_num = all_courses.course_num WHERE uni_ID=%s', (uni_ID,)) 
      totalCredits = c.fetchone()
      totalCredits = str(totalCredits[0])
      print("total credits: "+ str(totalCredits[0]))
    

    return render_template('/advising_student_transcript.html', results=results, msg=msg, avgGPA=avgGPA, totalCredits=totalCredits, uni_ID=uni_ID, program=program)

app.run(host='0.0.0.0', port=8080)