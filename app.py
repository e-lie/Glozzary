import os, csv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/csv-import/<csvname>')
def import_data(csvname):

    with open(csvname) as csvfile:
        reader = csv.DictReader(csvfile)
        francais = Language(name = 'Français', abbr = 'fr')
        english = Language(name = 'English', abbr = 'eng')
        #db.session.add_all([francais, english])
        #db.session.commit()
        return render_template('index.html', csvname=csvname, reader=reader)

    


if __name__ == '__main__':
    app.run()
