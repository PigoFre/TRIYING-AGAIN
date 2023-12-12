from flask import Flask, render_template, request
from flask import Flask, request, jsonify 
from flask import Flask, render_template, request, redirect, url_for
from your_gpt_script import process_user_input  # Import the function from your GPT script
from tavily import TavilyClient
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = process_user_input(user_input)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate_password', methods=['POST'])
def validate_password():
    password = request.form['password']
    correct_password = 'yourSecurePassword'  # Your actual password

    if password == correct_password:
        return redirect(url_for('main_content'))
    else:
        return render_template('index.html', error="Incorrect password, try again.")

@app.route('/main')
def main_content():
    return render_template('main_content.html')  # Your main content page

