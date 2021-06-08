from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, IntegerField
from chess import chess, initiate_session
from wtforms.validators import InputRequired
import datetime
checklist = []

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
        return redirect(url_for("shiss", _external=True, _scheme='http'))
    return render_template("index.html", time=time)


@app.route('/shiss', methods=["GET", "POST"])
def shiss() :
    form = Input()
    global players_log
    print(request.form)
    if len(checklist)>0 :
        if request.method == "POST":
            data = list(request.form.to_dict(flat=False).keys())[0]
            x = chess(players_log, data)
            players_log = x
    else:
        players_log = initiate_session()
        checklist.append('val')
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
