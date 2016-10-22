from flask import Flask
from flask import render_template
import numpy as np
import pandas as pd

app = Flask(__name__)





@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/dashboard/<path:roomid>')
def room_details(roomid):
    """fetch room details for <roomid>"""

    return render_template('room_details.html')


if __name__ == '__main__':
    app.run()
