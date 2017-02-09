from app import db

class Lexical(db.Model):
    __tablename__ = 'lexicals'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Unicode())
    language = db.Column(db.Integer, nullable=True, db.ForeignKey('languages.id'))
    #nature = 
    translation = db.relationship('Translation',
            foreign_keys=[Translation.follower_id],
            backref=db.backref('follower', lazy='joined'),
            lazy='dynamic',
            cascade='all, delete-orphan')

    def __repr__(self):
        return '<id {}>'.format(self.id)

#table for self referenced many-to-many relationship
class Translation(db.Model):
    __tablename__ = 'translations'
    source_id = db.Column(db.Integer, primary_key=True)
    dest_id = db.Column(db.Integer, primary_key=True)


