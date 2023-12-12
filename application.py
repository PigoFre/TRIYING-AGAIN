from flask import Flask, render_template, request
from flask import Flask, request, jsonify 
from your_gpt_script import process_user_input  # Import the function from your GPT script
from tavily import TavilyClient
application = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = process_user_input(user_input)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)
