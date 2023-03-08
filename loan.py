from flask import Flask, request, redirect, Response, render_template
from time import time
from sqlite3 import connect
app = Flask(__name__)

def denie_beacuase_of_too_many_applications(personal_ID):
    return True
def denie_beacuase_blacklisted(personal_ID):
    conn = connect('loan_applications.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM blacklisted_personal_IDs WHERE personal_id=?", (personal_ID,))
    count = cursor.fetchone()[0]

    conn.close()

    return count > 0

@app.route("/",methods=["GET","POST"])#this is the mainpage
def main_page():
    return render_template("main_page.html")

@app.route("/application_denied_because_too_many_applications",methods=["GET","POST"])#this is the mainpage
def application_denied_because_too_many_applications_page():
    return render_template("application deinied because too many applications.html")

@app.route("/response_to_application",methods=["GET","POST"])
def response_to_application():
    args_of_request={**dict(request.args),**dict(request.form)}
    add_loan_application_to_database(args_of_request["amount"],args_of_request["currency"], args_of_request["term"],args_of_request["name"], args_of_request["personal_ID"],args_of_request["contact"],args_of_request["type_of_contact"],args_of_request["comment"])
    if denie_beacuase_of_too_many_applications(args_of_request["personal_ID"]):
        return redirect("/application_denied_because_too_many_applications")
    if denie_beacuase_blacklisted(args_of_request["personal_ID"]):
        return redirect("/application_denied_because_blacklisted")
    return render_template("Application recieved.html")

@app.route("/apply_for_a_loan",methods=["GET","POST"])
def apply_for_a_loan_page():
    return render_template("apply_for_a_loan_form.html")

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

if __name__ == '__main__':
    app.run(debug=True)