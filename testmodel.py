"""
    script to test model with standalone sqlalchemy rather than flask_sqlalchemy etc.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, CheckConstraint, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
translations = Table("translations", Base.metadata,
    Column("source_lexical_id", Integer, ForeignKey("lexicals.id"), primary_key=True),
    Column("dest_lexical_id", Integer, ForeignKey("lexicals.id"), primary_key=True)
)

class Lexical(Base):
    __tablename__ = 'lexicals'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    language = relationship("Language")

    translations = relationship("Lexical",
                        secondary="translations",
                        primaryjoin="Lexical.id==translations.c.source_lexical_id",
                        secondaryjoin="Lexical.id==translations.c.dest_lexical_id",
                        backref="sources"
    )

    def __repr__(self):
       return "<Word (content='%s')>" % (self.content)



class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)


if __name__ == "__main__":
    engine = create_engine("postgresql://localhost/test_glozz_model1", echo=False)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    francais = Language(name = 'Français', abbr = 'fr')
    english = Language(name = 'English', abbr = 'eng')

    session.add_all([francais, english])
    session.commit()

    respectEng = Lexical(content='respect', language_id=2)
    respectFr = Lexical(content='respect', language_id=1)
    response = Lexical(content='response', language_id=2)
    reponse = Lexical(content='réponse', language_id=1)
    reaction = Lexical(content='réaction', language_id=1)
    
    respectEng.translations.append(respectFr)
    respectFr.translations.append(respectEng)
    
    response.translations.append(reponse)
    reponse.translations.append(response)
    
    response.translations.append(reaction)
    reaction.translations.append(response)

    session.add_all([respectFr, respectEng, response, reponse, reaction])
    session.commit()

    for lexical in session.query(Lexical).order_by(Lexical.id):
        print(lexical.id, lexical.content, lexical.translations)


    
