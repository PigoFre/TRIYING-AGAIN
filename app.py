from flask import Flask, render_template, request, redirect, url_for
from your_gpt_script import process_user_input

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    authenticated = False  # Variable to track if the user is authenticated
    error_message = None
    response = ""

    if request.method == "POST":
        if 'password' in request.form:
            password = request.form['password']
            correct_password = '15399'  # Replace with your actual password

            if password == correct_password:
                authenticated = True
            else:
                error_message = "Incorrect password, try again."

        elif 'user_input' in request.form:
            user_input = request.form["user_input"]
            response = process_user_input(user_input)

    return render_template("index.html", authenticated=authenticated, error=error_message, response=response)

if __name__ == "__main__":
    app.run(debug=True)
