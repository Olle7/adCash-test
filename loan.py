from flask import Flask, request, redirect, Response, render_template
from time import time
from sqlite3 import connect
app = Flask(__name__)

MAX_APPLICATIONS_IN_24_H=10

def get_all_arguments(request):
    args={}
    for key in request.form.keys():
        args[key]=request.form[key]
    for key in request.args.keys():
        if key in args:
            raise Exception("same parameter 2 times.")
        args[key]=request.args[key]
    return args

def denie_beacuase_of_too_many_applications(personal_ID):
    conn = connect('loan_applications.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM loan_database WHERE personal_id = ? AND time_of_recieving_application > ?;", (personal_ID,time()-60*60*24))
    rows = cursor.fetchall()
    count = len(rows)
    conn.close()
    #print("number of applications in last 60 seconds:", count)
    return count > MAX_APPLICATIONS_IN_24_H

def denie_beacuase_blacklisted(personal_ID):
    conn = connect('loan_applications.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM blacklisted_personal_IDs WHERE personal_id=?", (personal_ID,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def add_loan_application_to_database(amount,currency,term,name,personal_id,contact,type_of_contact,comment):
    # Connect to the SQLite database
    conn = connect('loan_applications.db')

    # Create a cursor object to execute SQL statements
    c = conn.cursor()

    # Insert a new loan application into the database
    timestamp = time()
    c.execute("INSERT INTO loan_database (amount,currency,term,name,personal_id,contact,type_of_contact,comment,time_of_recieving_application) VALUES (?, ?, ?, ?, ? , ?, ?, ?, ?)",
              (amount,currency,term,name,personal_id,contact,type_of_contact,comment,timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()




@app.route("/",methods=["GET","POST"])#this is the mainpage
def main_page():
    return render_template("main_page.html")



@app.route("/response_to_application",methods=["GET","POST"])
def response_to_application():
    args_of_request=get_all_arguments(request)
    if denie_beacuase_of_too_many_applications(args_of_request["personal_ID"]):
        return render_template("application deinied because too many applications.html")
    if denie_beacuase_blacklisted(args_of_request["personal_ID"]):
        return render_template("application denied because blacklisted.html")
    add_loan_application_to_database(args_of_request["amount"],args_of_request["currency"], args_of_request["term"],args_of_request["name"], args_of_request["personal_ID"],args_of_request["contact"],args_of_request["type_of_contact"],args_of_request["comment"])
    return render_template("Application recieved.html")

@app.route("/apply_for_a_loan_form",methods=["GET","POST"])
def apply_for_a_loan_page():
    return render_template("apply_for_a_loan_form.html")



@app.route("/table_of_loans_by_borrower",methods=["GET","POST"])
def table_of_loans_by_borrower():
    args_of_request=get_all_arguments(request)
    if "borrower" in args_of_request:
        pass
    else:
        pass
    return render_template("table_of_loans_by_borrower.html")

@app.route("/list_of_loans_by_borrower",methods=["GET","POST"])
def list_of_loans_by_borrower():
    args_of_request=get_all_arguments(request)
    conn=connect('loan_applications.db')
    c = conn.cursor()
    c.execute("SELECT * FROM loan_database WHERE personal_id = ?", (args_of_request["personal_ID"],))
    rows = c.fetchall()
    conn.close()
    print(type(rows))
    return rows



if __name__ == '__main__':
    app.run(debug=True)