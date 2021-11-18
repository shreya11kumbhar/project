from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"
#conn = sqlite3.connect("project.db")
#c = conn.cursor()
#c.execute("DROP TABLE IF EXISTS customer_details")
#c.execute("CREATE TABLE  customer_details(firstname VARCHAR(45), middlename VARCHAR(45), lastname VARCHAR(45), cpf_no VARCHAR(45), DOB DATE, phonenumber CHAR(10), emailid VARCHAR(50), DOJ DATE, DOE DATE, total_share_amt INT, total_lt_out INT, total_st_out INT)")
#conn.commit()
#conn.close()


@app.route("/homepage")
def homepage():
    return render_template("homepage.html")


@app.route("/customer_details", methods=["GET", "POST"])
def details():
    msg = ""
    if request.method == "POST":
        if request.form["firstname"] != "" and request.form["middlename"] != "" and request.form["lastname"] != "" and request.form["cpf_no"] != "" and request.form["DOB"] != "" and request.form["phonenumber"] != "" and  request.form["emailid"] != "" and request.form["DOJ"] != "" and request.form["DOE"] != "" and request.form["total_share_amt"] != "" and request.form["total_lt_out"] != "" and request.form["total_st_out"] != "":
            firstname = request.form["firstname"]
            middlename = request.form["middlename"]
            lastname = request.form["lastname"]
            cpf_no = request.form["cpf_no"]
            DOB = request.form["DOB"]
            phonenumber = request.form["phonenumber"]
            emailid = request.form["emailid"]
            DOJ = request.form["DOJ"]
            DOE = request.form["DOE"]
            total_share_amt = request.form["total_share_amt"]
            total_lt_out = request.form["total_lt_out"]
            total_st_out = request.form["total_st_out"]
            conn = sqlite3.connect("project.db")
            c = conn.cursor()
            c.execute(
                 "INSERT INTO customer_details VALUES('" + firstname + "', '" + middlename + "' , '" + lastname + "', '" + cpf_no + "', '" +  DOB  + "',  '" + phonenumber + "', '"+ emailid +"', '" +  DOJ + "',  '" +  DOE + "','" + total_share_amt + "', '" +  total_lt_out + "',  '" +  total_st_out + "')")
            msg = "Your account is created"
            conn.commit()
            conn.close()

    return render_template("customer_details.html",msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    if request.method == "POST":
        if request.form["userid"] != "" and request.form["emailid"] != "" and request.form["password"] != "" and request.form["firstname"] != "" and request.form["lastname"] != "" and request.form["status"] != "" and request.form["types"] != ""  and request.form["doj"] != ""   and  request.form["phonenumber"] != "" :
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
            c.execute("INSERT INTO user_login VALUES('" + userid + "', '"+ emailid + "' , '" + password + "', '"+ firstname +"', '"+ lastname +"', '"+ status +"', '"+ types +"',  '"+ doj +"',  '"+ phonenumber +"')")
            msg = "Your account is created"
            conn.commit()
            conn.close()

    return render_template("index.html", msg=msg)


@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == 'POST':
        userid = request.form["userid"]
        emailid = request.form["emailid"]
        password = request.form["password"]
        conn = sqlite3.connect("project.db")
        c = conn.cursor()
        c.execute("SELECT userid, emailid, password FROM user_login WHERE userid = '"+userid+"' and emailid = '"+emailid+"' and password = '"+password+"'")
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