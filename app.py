from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obituaries.db'
db = SQLAlchemy(app)

class Obituary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Obituary {self.name}>'

@app.route('/')
def index():
    # Customize this template to display obituaries
    return render_template('index.html')

@app.route('/view')
def view_obituaries():
    obituaries = Obituary.query.all()  # Retrieve all obituaries from the database
    return render_template('view_obituaries.html', obituaries=obituaries)


@app.route('/submit_obituary', methods=['POST'])
def submit_obituary():
    name = request.form['name']
    date_of_birth = request.form['date_of_birth']
    date_of_death = request.form['date_of_death']
    content = request.form['content']
    author = request.form['author']
    slug = request.form['slug']
    new_obituary = Obituary(
        name=name,
        date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date(),
        date_of_death=datetime.strptime(date_of_death, '%Y-%m-%d').date(),
        content=content,
        author=author,
        slug=slug
    )
    db.session.add(new_obituary)
    db.session.commit()
    return 'Obituary submitted!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
