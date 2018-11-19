from flask import Flask, request, redirect, url_for, render_template
from database import db,User

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI '] = 'postgressql://postgres:postgres@localhost/ig'
db = SQLalchemy(app)



@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/sign_up', methods=["GET", "POST"])
def index():
    return render_template('index.html', students=students)

@app.route('/create')
db.session.add(----)
db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)