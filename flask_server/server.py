from flask import Flask, request, render_template, redirect
import os
import json

# Note: static folder means all files from there will be automatically served over HTTP
app = Flask(__name__, static_folder="public")
app.secret_key = "miau".encode("utf-8")

# TODO Task 02: you can use a global variable for storing the auth session
# e.g., add the "authenticated" (boolean) and "username" (string) keys.
session = {"authenticated": False, "username": ""}

# you can use a dict as user/pass database
ALLOWED_USERS = {
    "test": "test123",
    "admin": "n0h4x0rz-plz",
}

# Task 04: database filename
DATABASE_FILE = "database.json"
UPLOAD_FOLDER = "./public/images/profile"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/second")
def second():
    return render_template("second.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Read user data from JSON file
        with open(DATABASE_FILE, 'r') as file:
            users_data = json.load(file)

        # Verify credentials
        print(username)
        print(password)
        for user_data in users_data:
            if user_data["user"] == username and user_data["pass"] == password:
                # Authentication successful
                session['authenticated'] = True
                session["username"] = username
                return redirect("/")
        error_msg = "Invalid username or password"

    return render_template("login.html", error_msg=error_msg)


@app.route("/logout")
def logout():
    session["authenticated"] = False
    return redirect("/")

@app.context_processor
def inject_template_vars():
    return {
        "todo_var": "TODO_inject_common_template_variables"
    }


# You can use this as a starting point for Task 04
# (note: you need a "write" counterpart)
def read_database(filename):
    """ Reads the user account details database file (line by line). """
    with open(filename, "rt") as f:
        line1 = f.readline()
        line2 = f.readline()
        age = int(f.readline())
        return {
            "first_name": line1,
            "last_name": line2,
            "age": age,
        }

def write_database(filename, object):
    """ Reads the user account details database file (line by line). """
    with open(filename, "wt") as f:
        f.write(object["first_name"] + '\n')
        f.write(object["last_name"] + '\n')
        f.write(str(object["age"]) + '\n')

# TODO Task 04: Save Account Details
@app.route("/account-details", methods=["GET", "POST"])
def save_account():
    # Hint: if method == "GET", read the data from the database and pass it to the template
    # otherwise (when POST), replace the database with the user-provided data.
    if request.method == "GET":
        res = read_database(DATABASE_FILE)
    elif request.method == "POST":
        res = {
            "first_name": request.form.get('fname'),
            "last_name": request.form.get('lname'),
            "age": int(request.form.get('age'))
        }
        write_database(DATABASE_FILE, res)
        print(request.files)
        
        if 'pic' in request.files:
            file = request.files['pic']
            print(request.files)
            if file:
                print(os.path.join(app.config['UPLOAD_FOLDER'], "pic.jpg"))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], "pic.jpg"))
            
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'pic.jpg')
    return render_template("/account-details.html", fname=res['first_name'], 
                               lname=res['last_name'], age=res['age'], user_image=full_filename)
    

@app.errorhandler(404)
def error404(code):
    # bonus: make it show a fancy HTTP 404 error page, with red background and bold message ;) 
    return "HTTP Error 404 - Page Not Found"


# Run the webserver (port 5000 - the default Flask port)
if __name__ == "__main__":
    app.run(debug=True, port=5000)

