from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from chess import chess, initiate_session
from wtforms.validators import InputRequired
import datetime


class Input(FlaskForm) :
    input = SelectField('Moves', choices=[])
    sub = SubmitField("Confirm")


class Time(FlaskForm) :
    mins = IntegerField('Minutes', default=15, validators=[InputRequired()])
    secs = IntegerField('Seconds', default=0, validators=[InputRequired()])
    sub = SubmitField("Confirm")



app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = "plz don't hack me"


@app.route('/', methods=["GET", "POST"])
def index() :
    time = Time()
    if time.validate_on_submit() :
        return redirect(url_for("shiss", mins=time.mins.data, secs=time.secs.data, _external=True, _scheme='http'))
    return render_template("index.html", time=time)


@app.route('/shiss/<int:mins>/<int:secs>', methods=["GET", "POST"])
def shiss(mins, secs) :
    form = Input()
    if form.input.data is None :
        global players_log
        players_log = initiate_session(mins, secs)
    else :
        x = chess(players_log, form)
        players_log = x
    if (len(players_log[0].legal_moves) > 0) | (players_log[0].time > datetime.timedelta(seconds=0)) :
        form.input.choices = players_log[0].legal_moves
        return render_template('shiss.html', players=players_log, nput=form, rng=range(8))
    else :
        return render_template('game_over.html')

@app.route('/drag_and_dorp')
def drag_and_dorp():
    return render_template('drag_and_dorp.html')


if __name__ == '__main__' :
    app.run(debug=True)
