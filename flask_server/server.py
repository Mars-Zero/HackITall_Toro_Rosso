from flask import Flask, request, render_template, redirect
import os
import json

# Note: static folder means all files from there will be automatically served over HTTP
app = Flask(__name__, static_folder="public")
app.secret_key = "miau".encode("utf-8")

# Task 04: database filename
DATABASE_FILE = "database.json"
UPLOAD_FOLDER = "./public/images/profile"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
session = {"authenticated": False, "username": ""}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/second")
def second():
    return render_template("second.html")


# Update the read and write functions to work with JSON
def read_database(filename):
    """ Reads the user account details from a JSON file. """
    with open(filename, "r") as f:
        return json.load(f)


def write_database(filename, data):
    """ Writes the user account details to a JSON file. """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/account-details", methods=["GET", "POST"])
def save_account():
    if request.method == "GET":
        if  session['authenticated']:
            res = {
                "Username": session["username"]
            }
        else:
            return render_template("login.html", error_msg="Not authenticated")
    elif request.method == "POST":
        res = {
            "Username": request.form.get("usr")
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
    return render_template("/account-details.html", fname=res['Username'],
                           user_image=full_filename)


@app.route("/login", methods=["GET", "POST"])
def login():
    error_msg = ""
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not username or not password:
            error_msg = "Username and password are required"
            return render_template("login.html", error_msg=error_msg)

        if action == "login":

            # Read user data from JSON file

            users_data = read_database(DATABASE_FILE)

            # Verify credentials
            for user_data in users_data:
                if user_data["user"] == username and user_data["pass"] == password:
                    # Authentication successful
                    session['authenticated'] = True
                    session["username"] = username
                    return redirect("/account-details")  # Redirect to home page after successful login

            # If the loop completes without finding a matching user, authentication fails
            error_msg = "Invalid username or password"

        # If action is "create", create a new user
        elif action == "create":

            # Read existing users from JSON file
            with open(DATABASE_FILE, 'r') as file:
                users_data = json.load(file)

            # Check if the username already exists
            for user_data in users_data:
                if user_data["user"] == username:
                    error_msg = "Username already exists"
                    return render_template("login.html", error_msg=error_msg)

            # Add the new user to the list of users
            users_data.append({"user": username, "pass": password})

            # Write the updated list of users back to the JSON file
            write_database(DATABASE_FILE, users_data)
            # with open(DATABASE_FILE, 'w') as file:
            #     json.dump(users_data, file, indent=4)

            # Optionally, you can automatically login the new user after creating the account
            session['authenticated'] = True
            session["username"] = username
            return redirect("/")  # Redirect to home page after creating account and login
    return render_template("login.html", error_msg=error_msg)


@app.route("/logout")
def logout():
    session['authenticated'] = False
    return redirect("/")


@app.context_processor
def inject_template_vars():
    return {
        "todo_var": "TODO_inject_common_template_variables"
    }


@app.errorhandler(404)
def error404(code):
    # bonus: make it show a fancy HTTP 404 error page, with red background and bold message ;)
    return "HTTP Error 404 - Page Not Found"


# Run the webserver (port 5000 - the default Flask port)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
