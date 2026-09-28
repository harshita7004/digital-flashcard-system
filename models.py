from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Flashcard {self.question}>'