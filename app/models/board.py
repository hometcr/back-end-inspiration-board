from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    owners_name = db.Column(db.String)
    # cards = db.relationship("Card", back_populates="board")