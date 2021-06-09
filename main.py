from flask import Flask, render_template
from flask.globals import request
from chess import chess, initiate_session
import datetime
players_log=[]

app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = "plz don't hack me"


@app.route('/', methods=["GET", "POST"])
def index() :
    return render_template("index.html")


@app.route('/shiss', methods=["GET", "POST"])
def shiss() :
    global players_log
    if len(players_log)>0 :
        if request.method == "POST":
            data = list(request.form.to_dict(flat=False).keys())[0]
            x = chess(players_log, data)
            players_log = x
    else:
        players_log = initiate_session()
    if (len(players_log[0].legal_moves) > 0) | (players_log[0].time > datetime.timedelta(seconds=0)) :
        return render_template('shiss.html', players=players_log, rng=range(8))
    else :
        return render_template('game_over.html')

@app.route('/drag_and_dorp')
def drag_and_dorp():
    return render_template('drag_and_dorp.html')


if __name__ == '__main__' :
    app.run(debug=True)
