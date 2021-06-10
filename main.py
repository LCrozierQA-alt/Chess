from flask import Flask, render_template
from flask.globals import request
from chess import chesspy, initiate_session
import datetime
players_log=[]


app = Flask(__name__, static_url_path='/static')
app.config["SECRET_KEY"] = "plz don't hack me"


@app.route('/', methods=["GET", "POST"])
def index() :
    return render_template("index.html")


@app.route('/chess', methods=["GET","POST"])
def chess() :
    return render_template('chess_backdrop.html')

@app.route('/shiss2', methods=["GET", "POST"])
def shiss2() :
    global players_log
    if len(players_log)>0 :
        if request.method == "POST":
            data = list(request.form.to_dict(flat=False).keys())[0]
            x = chesspy(players_log, data)
            players_log = x
    else:
        players_log = initiate_session()
    if (len(players_log[0].legal_moves) > 0) | (players_log[0].time > datetime.timedelta(seconds=0)) :
        return render_template('shiss2.html', players=players_log, rng=range(8))
    else :
        return render_template('game_over.html')   




if __name__ == '__main__' :
    app.run(debug=True)
