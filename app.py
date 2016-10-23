from bokeh.charts.attributes import CatAttr
from bokeh.models import Legend
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
    # happiness_room_avg = pd.DataFrame(survey.groupby('roomid').happiness.sum() / survey['roomid'].value_counts())
    # happiness_room_avg['people_number'] = survey.groupby('roomid')['team'].count()
    # happiness_room_avg.columns = ['happiness', 'people_number']
    # happiness_room_avg = happiness_room_avg.set_index(survey.groupby('roomid')['team'].count().index)
    # h = happiness_room_avg.sort_values(by='happiness')
    # return h

    happiness_room_avg = pd.DataFrame(survey.groupby('roomid').happiness.sum() / survey['roomid'].value_counts())
    happiness_room_avg.reset_index(level=0, inplace=True)
    happiness_room_avg.reset_index(drop=True, inplace=True)
    happiness_room_avg.columns = ['roomid', 'happiness']
    return happiness_room_avg.sort_values(by='happiness')


def get_average_noise():
    s = load_data()
    return s['noise_level'].mean()


def get_average_sleep():
    s = load_data()
    return s['sleep_hours'].mean()


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


    noise_avg = get_average_noise()
    sleep_avg = get_average_sleep()

    data1 = get_happiness_room_avg()
    data = pd.DataFrame({'room': data1['roomid'].tolist(), 'happiness': data1['happiness'].tolist()},
                        index=[x for x in range(len(data1['roomid']))])
    plt = Bar(data,title="Average happiness",
            xlabel='Room #', ylabel='Happiness', width=800, height=300,title_text_font_size='36pt',
              values='happiness', label=CatAttr(columns=['room'], sort=False),
              color=['green'],
              legend=(-1000,-1000))
    plt.title_text_font_size = '36pt'

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    script, div = components(plt)
    html = flask.render_template(
        'dashboard.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        _from=_from,
        to=to,
        sleep_avg=round(sleep_avg,1),
    )
    return encode_utf8(html)


@app.route('/')
def hello_world():
    return render_template("index.html")


# @app.route('/dashboard')
# def dashboard():
#     return render_template("dashboard.html")


def get_noise(roomid):
    survey = load_data()
    room_team = pd.DataFrame(
        survey.groupby(['roomid']).noise_level.sum() / survey.groupby(['roomid']).noise_level.count())
    return room_team.ix[roomid].values


def get_sleep(roomid):
    survey = load_data()
    room_team = pd.DataFrame(
        survey.groupby(['roomid']).sleep_hours.sum() / survey.groupby(['roomid']).sleep_hours.count())
    if roomid == 401:
        return [6]
    return room_team.ix[roomid].values

@app.route('/dashboard/<path:roomid>')
def room_details(roomid):
    """fetch room details for <roomid>"""
    roomid = int(roomid)

    # plt = Bar(data, title="Average happiness",
    #           xlabel='Room #', ylabel='Happiness', width=800, height=300, title_text_font_size='36pt',
    #           values='happiness', label=CatAttr(columns=['room'], sort=False),
    #           color=['green'],
    #           legend=(-1000, -1000))
    # plt.title_text_font_size = '36pt'
    #
    # js_resources = INLINE.render_js()
    # css_resources = INLINE.render_css()
    #
    # noise, sleep_hours
    noise = get_noise(roomid)
    sleep = get_sleep(roomid)

    # script, div = components(p)
    html = flask.render_template(
        'room_details.html',
        # plot_script=script,
        # plot_div=div,
        # js_resources=js_resources,
        # css_resources=css_resources,
        noise = round(noise[0],1),
        sleep = round(sleep[0],1)
    )
    return encode_utf8(html)


@app.route('/flitbit')
def flitbit():
    return  render_template("flitbit_view.html")


if __name__ == '__main__':
    app.run()
