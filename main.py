from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from django import db
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


app = Flask(__name__)
app.secret_key = "super secret key"


# Homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")


# Register
@app.route("/index/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if request.form["userid"] != "" and request.form["emailid"] != "" and request.form["password"] != "" and \
                request.form["firstname"] != "" and request.form["lastname"] != "" and request.form["status"] != "" and \
                request.form["types"] != "" and request.form["doj"] != "" and request.form["phonenumber"] != "":
            userid = request.form["userid"]
            emailid = request.form["emailid"]
            password = request.form["password"]
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            status = request.form["status"]
            types = request.form["types"]
            doj = request.form["doj"]
            phonenumber = request.form["phonenumber"]
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO user_login VALUES('" + userid + "', '" + emailid + "' , '" + password + "', '" + firstname + "', '" + lastname + "', '" + status + "', '" + types + "',  '" + doj + "',  '" + phonenumber + "')")
            conn.commit()
            conn.close()

    return render_template("index.html")


# Login
@app.route("/index/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        userid = request.form["userid"]
        emailid = request.form["emailid"]
        password = request.form["password"]
        conn = sqlite3.connect("project.db")
        c = conn.cursor()
        c.execute(
            "SELECT userid, emailid, password FROM user_login WHERE userid = '" + userid + "' and emailid = '" + emailid + "' and password = '" + password + "'")
        r = c.fetchall()
        for i in r:
            if userid == i[0] and emailid == i[1] and password == i[2]:
                session["logedin"] = True
                session["userid"] = userid
                return redirect(url_for("after_login"))
    return render_template("index.html")


# After login
@app.route("/after_login")
def after_login():
    return render_template("after_login.html")




# Customer Details
@app.route("/customer_details", methods=["GET", "POST"])
def details():
    msg = ""
    if request.method == "POST":
        if request.form["firstname"] != "" and request.form["middlename"] != "" and request.form["lastname"] != "" and \
                request.form["cpf_no"] != "" and request.form["DOB"] != "" and request.form["phonenumber"] != "" and \
                request.form["emailid"] != "" and request.form["DOJ"] != "" and request.form["DOE"] != "":
            firstname = request.form["firstname"]
            middlename = request.form["middlename"]
            lastname = request.form["lastname"]
            cpf_no = request.form["cpf_no"]
            DOB = request.form["DOB"]
            phonenumber = request.form["phonenumber"]
            emailid = request.form["emailid"]
            DOJ = request.form["DOJ"]
            DOE = request.form["DOE"]
            total_st_amt = '0'
            total_lt_amt = '0'
            total_share_amt = '0'
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO customer_details VALUES('" + firstname + "', '" + middlename + "' , '" + lastname + "', '" + cpf_no + "', '" + DOB + "',  '" + phonenumber + "', '" + emailid + "', '" + DOJ + "',  '" + DOE + "', '" + total_st_amt+ "', '" + total_lt_amt + "',  '" + total_share_amt + "')")
            msg = "Your account is created"
            conn.commit()
            conn.close()

    return render_template("customer_details.html", msg=msg)


# customer search
@app.route("/customer_details/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cpf_no = request.form["cpf_no"]
        conn = sqlite3.connect("project.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select cpf_no from customer_details WHERE cpf_no = '" + cpf_no + "'")
        rows = c.fetchall()
        for r in rows:
            for i in r:
                print(i)
        c.execute(
            "SELECT l.loan_amt FROM loan_details l INNER JOIN customer_details c ON l.cpf_no=c.cpf_no WHERE l.loan_type='st' and c.cpf_no = '"+cpf_no+"' ")
        st_loan_amt = (c.fetchall())
        total_st_amt = 0
        total_share_amt = 0
        for i in st_loan_amt:
            for j in range(len(i)):
                total_share_amt += i[j]*0.2
                total_st_amt += i[j]
        print(total_st_amt)
        c.execute(
            "SELECT l.loan_amt FROM loan_details l INNER JOIN customer_details c ON l.cpf_no=c.cpf_no WHERE l.loan_type='lt' and c.cpf_no = '" + cpf_no + "' ")
        lt_loan_amt = (c.fetchall())
        total_lt_amt = 0
        for i in lt_loan_amt:
            for j in range(len(i)):
                total_share_amt += i[j]*0.2
                total_lt_amt += i[j]
        print(total_lt_amt)
        print(total_share_amt)
        c.execute("UPDATE customer_details SET total_st_amt = '" +str(total_st_amt)+"', total_lt_amt = '" +str(total_lt_amt)+"', total_share_amt = '" +str(total_share_amt)+"' WHERE cpf_no = '" + cpf_no + "' ")
        c.execute("select * from customer_details WHERE cpf_no = '" + cpf_no + "'")
        rows = c.fetchall()
        for r in rows:
            for i in r:
                print(i)
        conn.commit()
        c.close()
        return render_template("customer_details.html", rows=rows)


# New short term loan
@app.route("/new_loan/shortLoan", methods=["GET", "POST"])
def shortLoan():
    msg = ""
    v = ""
    if request.method == "POST":
        if request.form["cpf_no"] != "" and request.form["loan_amt"] != ""  and request.form["int_rate"] != "" and request.form["no_int"] != "" and request.form["principal_amt"] != "" and request.form["out_loan_amt"] != "" and request.form["loan_disb_date"] != "":
            cpf_no = request.form["cpf_no"]
            loan_amt = request.form["loan_amt"]
            int_rate = request.form["int_rate"]
            no_int = request.form["no_int"]
            principal_amt = request.form["principal_amt"]
            out_loan_amt = request.form["out_loan_amt"]
            loan_disb_date = request.form["loan_disb_date"]
            loan_type = "st"
            from_date = request.form["loan_disb_date"]
            days = date.today() + timedelta(days=+30)
            due_date = str(days)
            future_date = date.today() + relativedelta(months=+10)
            to_date = str(future_date)
            r = float(int_rate) / 12 / 100
            x = int((int(loan_amt) * r * (1 + r) ** int(no_int)) / (((1 + r) ** int(no_int)) - 1))
            y = int(r * int(loan_amt))
            emi = str(x)
            int_amt = str(y)
            loan_id = str(cpf_no) + str(loan_type) + "".join(str(loan_disb_date).split("-"))
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute("""SELECT cpf_no FROM customer_details WHERE cpf_no=?""", (cpf_no,))
            result = c.fetchone()
            if result:
                c.execute(
                    "INSERT INTO loan_details VALUES('" + cpf_no + "' , '" + loan_amt + "' ,'" + int_rate + "','" + no_int + "' , '" + principal_amt + "' ,'" + out_loan_amt + "' , '" + loan_disb_date + "','" + loan_type + "','"+loan_id+"')")
                c.execute(
                    "INSERT INTO generate_emi VALUES('" + loan_id + "','" + cpf_no + "'  , '" + principal_amt + "','" + int_amt + "' ,'" + out_loan_amt + "' , '" + from_date + "','" + to_date + "','" + emi + "','" + no_int + "','"+due_date+"')")
                v = "valid"
            else:
                v = "invalid"
            conn.commit()
            conn.close()

    return render_template("new_loan.html", v=v)


# New long term loan
@app.route("/new_loan/longLoan", methods=["GET", "POST"])
def longLoan():
    msg = ""
    if request.method == "POST":
        if request.form["cpf_no"] != "" and request.form["loan_amt"] != ""  and request.form["int_rate"] != "" and request.form["no_int"] != "" and request.form["principal_amt"] != "" and request.form["out_loan_amt"] != "" and request.form["loan_disb_date"] != "":
            cpf_no = request.form["cpf_no"]
            loan_amt = request.form["loan_amt"]
            int_rate = request.form["int_rate"]
            no_int = request.form["no_int"]
            principal_amt = request.form["principal_amt"]
            out_loan_amt = request.form["out_loan_amt"]
            loan_disb_date = request.form["loan_disb_date"]
            from_date = request.form["loan_disb_date"]
            days = date.today() + timedelta(days=+30)
            due_date = str(days)
            future_date = date.today() + relativedelta(months=+int(no_int))
            to_date = str(future_date)
            loan_type = "lt"
            loan_id = str(cpf_no) + str(loan_type) + "".join(str(loan_disb_date).split("-"))
            r = float(int_rate)/12/100
            x = int((int(loan_amt) * r * (1 + r) ** int(no_int)) / (((1 + r) ** int(no_int)) - 1))
            y = int(r * int(loan_amt))
            emi = str(x)
            int_amt = str(y)
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute("""SELECT cpf_no FROM customer_details WHERE cpf_no=?""", (cpf_no,))
            result = c.fetchone()
            if result:
                c.execute(
                    "INSERT INTO loan_details VALUES('" + cpf_no + "' , '" + loan_amt + "' ,'" + int_rate + "','" + no_int + "' , '" + principal_amt + "' ,'" + out_loan_amt + "' , '" + loan_disb_date + "','" + loan_type + "','"+loan_id+"')")
                c.execute(
                    "INSERT INTO generate_emi VALUES('" + loan_id + "','" + cpf_no + "'  , '" + principal_amt + "','"+int_amt+"' ,'" + out_loan_amt + "' , '" + from_date + "','" + to_date + "','"+emi+"','" + no_int + "','"+due_date+"')")
                msg = "valid"
            else:
                msg = "invalid"
            conn.commit()
            conn.close()

    return render_template("new_loan.html", msg=msg)


@app.route("/get_emi",methods = ["GET","POST"])
def get_emi():
    rows = []
    conn = sqlite3.connect("project.db")
    c = conn.cursor()
    c.execute("SELECT g.cpf_no,g.loan_id,c.firstname,c.lastname,g.due_date,g.emi,c.emailid,c.phonenumber FROM generate_emi g INNER JOIN customer_details c ON g.cpf_no=c.cpf_no ")
    rows = c.fetchall()
    for r in rows:
        for i in r:
            print(i,end=" ")
    conn.commit()
    conn.close()
    return render_template("get_emi.html",rows=rows)


@app.route("/receive_emi",methods=["GET", "POST"])
def receive_emi():
    conn = sqlite3.connect("project.db")
    c = conn.cursor()
    c.execute(
            "SELECT g.cpf_no,g.loan_id,c.firstname,c.lastname,g.due_date,g.emi,c.emailid,c.phonenumber FROM generate_emi g INNER JOIN customer_details c ON g.cpf_no=c.cpf_no ORDER BY g.due_date ")
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return render_template("receive_emi.html",rows=rows)


@app.route("/payment",methods=["GET", "POST"])
def payment():
    return render_template("payment.html")


# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)

db.connections.close_all()