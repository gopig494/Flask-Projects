from flask import Flask,render_template,request,flash,g,session,redirect,url_for
import os
import pandas as pd
from static.python.db import Db 
import string
import random
import sqlite3

app = Flask(__name__)
app.secret_key = "12345"
app.config['folder_path'] = "static/files"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods = ["GET","POST"])
def register():
    if request.method == "POST":
        session_id = ''.join(random.choices(string.ascii_uppercase +string.digits,k=6))
        username = request.form.get('user_name')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm_password = request.form.get('confirm_password')
        if confirm_password != password:
            flash("Password and Confirm Passowrd must be same",'failed')
            return redirect(url_for('register'))
        db_obj = Db()
        try:
            cursor,connection = db_obj.connect_db()
            query = f""" INSERT INTO 'Users Registration' (sid,name,email,password)  
                            VALUES('{session_id}','{username}','{email}','{password}') """
            cursor.execute(query)
            connection.commit()
        except sqlite3.IntegrityError:
            flash("Email already registered.Please use differnet email to register.","failed")
            return redirect(url_for('register'))
        except Exception as e:
            connection.rollback()
            flash("Something went wrong.","failed")
            query = db_obj.get_log_query(f"Registration failed - {email}",e)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for('register'))
        finally:
            g.user_id = email
            g.session_id = session_id
            session["session_id"] =  session_id
            connection.close()
        flash("Registration Successfully..! You can log in Here..!","Register")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('user_name')
        password = request.form.get('password')
        try:
            db_obj = Db()
            cursor,connection = db_obj.connect_db()
            query = f""" SELECT sid,name,email,role
                            FROM 'Users Registration'  WHERE email = '{username}'
                        AND password = '{password}' """ 
            cursor.execute(query)
            user_info = cursor.fetchone()
            if user_info:
                session['session_id'] = user_info[0]
                g.session_id = user_info[0]
                g.name = user_info[1]
                g.role = user_info[3]
                flash("Logged in successfully..!","failed")
            else:
                flash("User email or password is invalid..!","failed")
                return redirect(url_for('login'))    
        except Exception:
            flash("Something went wrong",'failed')
            return redirect(url_for('login'))
        finally:
            connection.close()
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout Successfully.","success")
    return redirect(url_for("login"))

@app.route("/addfiles")
def add_files():
    return render_template("upload.html")


@app.route("/uploadfiles",methods=["POST"])
def up_files():
    if request.method == "POST":
        file = request.files.get('all_files')
        file.save(os.path.join(app.config['folder_path'],file.filename))
        flash(f"{file.filename} uploaded successfully",'success')
        return render_template("upload.html")
    
@app.route("/uploadfilesexcel",methods=["POST"])
def up_filesexcel():
    if request.method == "POST":
        file = request.files.get('excel_file')
        file.save(os.path.join(app.config['folder_path'],file.filename))
        readed_data = pd.read_csv(os.path.join(app.config['folder_path'],file.filename))
        return render_template("upload.html",data = readed_data.to_html())

@app.before_request
def before_request():
    if request.path !='/logout' and request.path != "/" and request.path != "/login" and request.path != "/register" and '/static' not in request.path:
        if session and g and 'session_id' in g:
            session_found = False
            for sess in session:
                if sess.session_id == g.session_id:
                    session_found = True
            if not session_found:
                session.clear()
                flash("Your session was expired.Please login again.",'failed')
                return redirect(url_for("login"))    
        else:
            session.clear()
            flash("Your session was expired.Please login again.",'failed')
            return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)
 
