from flask import Flask
from flask import render_template
import numpy as np
import pandas as pd
from bokeh.charts import Bar, output_file, show
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import flask

app = Flask(__name__)
colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}

def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]


def load_data():
    survey = pd.read_csv('participants_survey.csv', delimiter=";")
    return survey.drop('time_record', axis=1)

def get_happiness_room_avg():
    """Report main bar chart. Rooms versus happiness and people number"""
    survey = load_data()
    happiness_room_avg = pd.DataFrame(survey.groupby('roomid').happiness.sum() / survey['roomid'].value_counts())
    happiness_room_avg['people_number'] = survey.groupby('roomid')['team'].count()
    happiness_room_avg.columns = ['happiness', 'people_number']
    happiness_room_avg = happiness_room_avg.set_index(survey.groupby('roomid')['team'].count().index)
    return happiness_room_avg.sort_values(by='happiness')


@app.route("/dashboard")
def dashboard():
    """ Very simple embedding of a polynomial chart
    """
    ## TODO: don't visualize number of people!


    # Grab the inputs arguments from the URL
    args = flask.request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    # Create a polynomial line graph with those arguments
    # x = list(range(_from, to + 1))
    # fig = figure(title="Polynomial")
    # fig.line(x, [i ** 2 for i in x], color=color, line_width=2)
    p = Bar(get_happiness_room_avg(), title="Average happiness", xlabel='Room #', ylabel='Happiness', width=800, height=400)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(p)
    html = flask.render_template(
        'dashboard.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color=color,
        _from=_from,
        to=to
    )
    return encode_utf8(html)


@app.route('/')
def hello_world():
    return render_template("index.html")


# @app.route('/dashboard')
# def dashboard():
#     return render_template("dashboard.html")


@app.route('/dashboard/<path:roomid>')
def room_details(roomid):
    """fetch room details for <roomid>"""

    return render_template('room_details.html')


if __name__ == '__main__':
    app.run()
