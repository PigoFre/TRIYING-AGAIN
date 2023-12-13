from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from your_gpt_script import process_user_input

app = Flask(__name__)
app.secret_key = '1355'  # Set a secret key for session management

@app.route("/", methods=["GET", "POST"])
def home():
    if 'authenticated' not in session:
        session['authenticated'] = False

    if request.method == "POST":
        if 'password' in request.form:
            password = request.form['password']
            correct_password = '15399'  # Replace with your actual password

            if password == correct_password:
                session['authenticated'] = True
                return redirect(url_for('home'))
            else:
                return render_template('index.html', error="Incorrect password, try again.")

        elif 'user_input' in request.form and session.get('authenticated'):
            user_input = request.form["user_input"]
            response = process_user_input(user_input)
            return jsonify({'response': response})

    return render_template("index.html", authenticated=session['authenticated'])

if __name__ == "__main__":
    app.run(debug=True)
