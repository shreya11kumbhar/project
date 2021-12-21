from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route("/")
def homepage():
    return render_template("homepage.html")


# New Loan
@app.route("/new_loan/shortLoan", methods=["GET", "POST"])
def shortLoan():
    msg = ""
    v = ""
    if request.method == "POST":
        if request.form["cpf_no"] != "" and request.form["loan_amt"] != "" and request.form["int_rate"] != "" and request.form["no_int"] != "" and request.form["principal_amt"] != "" and request.form["out_loan_amt"] != "" and request.form["loan_disb_date"] != "":
            cpf_no = request.form["cpf_no"]
            loan_amt = request.form["loan_amt"]
            int_rate = request.form["int_rate"]
            no_int = request.form["no_int"]
            principal_amt = request.form["principal_amt"]
            out_loan_amt = request.form["out_loan_amt"]
            loan_disb_date = request.form["loan_disb_date"]
            loan_type = "short term"
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute("""SELECT cpf_no FROM customer_details WHERE cpf_no=?""", (cpf_no,))
            result = c.fetchone()
            if result:
                c.execute(
                    "INSERT INTO loan_details VALUES('" + cpf_no + "' , '" + loan_amt + "' ,'" + int_rate + "','" + no_int + "' , '" + principal_amt + "' ,'" + out_loan_amt + "' , '" + loan_disb_date + "','" + loan_type + "')")
                v = "valid"
            else:
                v = "invalid"


            conn.commit()
            conn.close()

    return render_template("new_loan.html", msg=msg,v=v)


# New Loan
@app.route("/new_loan/longLoan", methods=["GET", "POST"])
def longLoan():
    msg = ""
    if request.method == "POST":
        if request.form["cpf_no"] != "" and request.form["loan_amt"] != "" and request.form["int_rate"] != "" and request.form["no_int"] != "" and request.form["principal_amt"] != "" and request.form["out_loan_amt"] != "" and request.form["loan_disb_date"] != "":
            cpf_no = request.form["cpf_no"]
            loan_amt = request.form["loan_amt"]
            int_rate = request.form["int_rate"]
            no_int = request.form["no_int"]
            principal_amt = request.form["principal_amt"]
            out_loan_amt = request.form["out_loan_amt"]
            loan_disb_date = request.form["loan_disb_date"]
            loan_type = "long term"
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO loan_details VALUES('" +  cpf_no + "' , '"+ loan_amt+"' ,'" + int_rate+ "','" +  no_int + "' , '"+ principal_amt+"' ,'" +  out_loan_amt + "' , '"+ loan_disb_date+"','"+loan_type+"')")
            msg = "Your account is created"
            conn.commit()
            conn.close()

    return render_template("new_loan.html", msg=msg)


# Customer Details
@app.route("/customer_details", methods=["GET", "POST"])
def details():
    msg = ""
    if request.method == "POST":
        if request.form["firstname"] != "" and request.form["middlename"] != "" and request.form["lastname"] != "" and \
                request.form["cpf_no"] != "" and request.form["DOB"] != "" and request.form["phonenumber"] != "" and \
                request.form["emailid"] != "" and request.form["DOJ"] != "" and request.form["DOE"] != "" and \
                request.form["total_share_amt"] != "" and request.form["total_lt_out"] != "" and request.form["total_st_out"] != "":
            firstname = request.form["firstname"]
            middlename = request.form["middlename"]
            lastname = request.form["lastname"]
            cpf_no = request.form["cpf_no"]
            DOB = request.form["DOB"]
            phonenumber = request.form["phonenumber"]
            emailid = request.form["emailid"]
            DOJ = request.form["DOJ"]
            DOE = request.form["DOE"]
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO customer_details VALUES('" + firstname + "', '" + middlename + "' , '" + lastname + "', '" + cpf_no + "', '" + DOB + "',  '" + phonenumber + "', '" + emailid + "', '" + DOJ + "',  '" + DOE + "')")
            msg = "Your account is created"
            conn.commit()
            conn.close()

    return render_template("customer_details.html", msg=msg)


@app.route("/customer_details/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cpf_no = request.form["cpf_no"]
        conn = sqlite3.connect("project.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("select * from customer_details WHERE cpf_no = '" + cpf_no + "'")
        rows = c.fetchall()
        c.close()
        for r in rows:
            print(r)

        return render_template("customer_details.html", rows=rows)


# Register and Login page
@app.route("/index/register", methods=["GET", "POST"])
def register():
    msg = ""
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
            msg = "Your account is created"
            conn.commit()
            conn.close()

    return render_template("index.html", msg=msg)


@app.route("/index/login", methods=["GET", "POST"])
def login():
    msg = ""
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
            else:
                msg = "Please Enter Valid Userid,Emailid and Password"
    return render_template("index.html", msg=msg)


@app.route("/after_login")
def after_login():
    return render_template("after_login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
