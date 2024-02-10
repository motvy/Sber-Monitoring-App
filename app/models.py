from app import db


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    datetime = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.link
