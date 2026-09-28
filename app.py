from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db, Flashcard
from forms import FlashcardForm
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.config['DEBUG'] = True

csrf = CSRFProtect(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    flashcards = Flashcard.query.all()
    return render_template('index.html', flashcards=flashcards)

@app.route('/create', methods=['GET', 'POST'])
def create_flashcard():
    form = FlashcardForm()
    if form.validate_on_submit():
        flashcard = Flashcard(question=form.question.data, answer=form.answer.data)
        db.session.add(flashcard)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_flashcard.html', form=form)

@app.route('/study')
def study():
    flashcards = Flashcard.query.all()
    return render_template('study.html', flashcards=flashcards)

if __name__ == '__main__':
    app.run(debug=True)