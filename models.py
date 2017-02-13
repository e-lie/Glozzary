from app import db


translations = db.Table("translations", db.Model.metadata,
    db.Column("source_lexical_id", db.Integer, db.ForeignKey("lexicals.id"), primary_key=True),
    db.Column("dest_lexical_id", db.Integer, db.ForeignKey("lexicals.id"), primary_key=True)
)

class Lexical(db.Model):
    __tablename__ = 'lexicals'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    language = db.relationship("Language")
    translations = db.relationship("Lexical",
                        secondary="translations",
                        primaryjoin="Lexical.id==translations.c.source_lexical_id",
                        secondaryjoin="Lexical.id==translations.c.dest_lexical_id",
                        backref="sources"
    )


    def __repr__(self):
       return "<Word (content='%s')>" % (self.content)


class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    abbr = db.Column(db.Unicode)

    def __init__(self, name, abbr):
        self.name = name
        self.abbr = abbr

