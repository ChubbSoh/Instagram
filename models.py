class User(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), unique=True)
    age = db.Column(db.Integer, unique=True)

    def __init__(self,username,email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

