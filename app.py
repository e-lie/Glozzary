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
        db.session.add_all([francais, english])
        db.session.commit()

        lexicals = []
        for row in reader:
           meto = Lexical(content=row['fr_meto'],language=francais)
           obj = Lexical(content=row['fr_obj'],language=francais)
           meto.translations = []
           meto.translations.append(obj)
           obj.translations = []
           obj.translations.append(meto)
           lexicals.append(meto)
           lexicals.append(obj)

        db.session.add_all(lexicals)
        db.session.commit()

    return "{} Imported !".format(csvname)

@app.route('/query_lexicals')
def query_lexicals():

    qlexicals = []
    for content, language in db.session.query(Lexical.content, Lexical.language):
        print(language)
        qlexicals.append(content)
        
    return render_template('index.html', qlexicals=qlexicals)



if __name__ == '__main__':
    app.run()
