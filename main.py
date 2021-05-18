from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from chess import chess, initiate_session
players_log = []

class Input(FlaskForm) :
    input = SelectField('Moves', choices=[])
    sub = SubmitField("Confirm")


app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = "excuse_me_mam,_ur_boobies_are_poggers"


@app.route('/')
def index() :
    x = "shiss"
    return render_template("html.htm", title=x)


@app.route('/shiss', methods=["GET", "POST"])
def shiss() :
    form = Input()
    if form.input.data is None :
        players_log.append(initiate_session())
    else :
        players_log.append(chess(players_log[-1], form))
    if len(players_log[-1][0].legal_moves) > 0 :
        form.input.choices = players_log[-1][0].legal_moves
        return render_template('shiss.html', players=players_log[-1], nput=form, rng=range(8))
    else :
        return render_template('game_over.html')

if __name__ == '__main__' :
    app.run(debug=True)
