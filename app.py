from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():

    # User reached by POST
    if request.method = "POST":
    
    # User reached by GET
    else:

        return render_template("index.html")